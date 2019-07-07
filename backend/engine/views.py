from django.shortcuts import render, get_object_or_404
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework import status
from django.http import Http404, HttpResponse
#from .models import *
#from .serializers import *
from rest_framework.renderers import TemplateHTMLRenderer
from django.db.models import F
from django.db import IntegrityError
from django.template import loader
from django.http import HttpResponse, Http404
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import FileSystemStorage

import numpy as np
import hashlib
# todo rm utils
from .utils import load_database, compute_distances
from .models import *
import paramiko
from PIL import Image
import json

class AllNeighborsOfNode(APIView):
    """
    List all neighbors available for a given node
    """

    def get(self, request, image_id, format=None):
        image_id = int(image_id) - 1 # todo index <-> id
        (header, images) = load_database('engine/database.csv')
        distances = compute_distances(header, images)
        n_images = len(images)

        n_closest = 3
        neighbors = []
        for k in range(n_closest):
            # todo (+1) useful because images indexes start from 1
            closest = np.argmax(distances[image_id]) + 1
            # todo check if order
            (from_image, to_image) = (str(closest), str(image_id + 1)) if closest < image_id else (str(image_id + 1), str(closest))
            neighbors.append({
                'id': from_image + '_' + to_image,
                'from': from_image,
                'to': to_image,
                'width': 10*distances[image_id][closest - 1] # voir ou on fait ça. Ptet pas top ici non plus
                });
            distances[image_id][closest - 1] *= -1
        return Response(neighbors)

# todo warning.
@csrf_exempt
def testUploadPicture(request):
    if (not request.method) or ('picture' not in request.FILES):
        raise Http404


    picture_image = request.FILES['picture']
    hash = hashlib.sha224(picture_image.read()).hexdigest()
    print(hash)

    # todo check format (jpg only)
    picture = Picture(hash=hash)
    try:
        picture.save()
    except IntegrityError:
        # 409: Conflict
        return HttpResponse('Already uploaded image (same hash)', status='409')

    picture_id = str(picture.id)
    fs = FileSystemStorage()
    fs.save('{}.jpg'.format(picture_id), picture_image)

    image = Image.open(picture_id + '.jpg')
    size = (364, 364)
    image.thumbnail(size)
    image.save(picture_id + '_thumbnail.jpg')


    settings = fs.open('settings_sftp.json', 'r')
    settings = settings.read()
    settings = json.loads(settings)

    transport = paramiko.Transport((settings['SFTP_HOST'], settings['SFTP_PORT']))
    transport.connect(username=settings['SFTP_USER'], password=settings['SFTP_PASSWORD'])

    sftp = paramiko.SFTPClient.from_transport(transport)

    filepath = 'full/{}.jpg'.format(picture.id)
    localpath = '{}.jpg'.format(picture.id)
    transfert_failed = False
    try:
        sftp.put(picture_id + '.jpg', 'full/' + picture_id + '.jpg')
        sftp.put(picture_id + '_thumbnail.jpg', 'thumbnails/' + picture_id + '.jpg')
    except:
        transfert_failed = True

    sftp.close()
    transport.close()

    fs.delete(picture_id + '_thumbnail.jpg')
    fs.delete(picture_id + '.jpg')

    if transfert_failed:
        picture.delete()
        return HttpResponse('Error in transfert. Nothing done.', status='504')
    else:
        return HttpResponse('Image uploaded successfully', status='201')
