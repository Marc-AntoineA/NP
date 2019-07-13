from django.shortcuts import render, get_object_or_404
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework import status
from django.http import Http404, HttpResponse
from rest_framework.renderers import TemplateHTMLRenderer
from django.db.models import F
from django.db import IntegrityError
from django.template import loader
from django.http import HttpResponse, Http404
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import FileSystemStorage
from django.db.models import Count, Min

import numpy as np
import hashlib
# todo rm utils
from .utils import load_database, compute_distances
from .models import *
import paramiko
from PIL import Image
import json
from random import random, randint

class AllNeighborsOfNode(APIView):
    """
    List all neighbors available for a given node
    """

    # todo optim l'algo
    def get(self, request, picture_id, format=None):
        frequencies = Tag.objects.all().annotate(count=Count('picture'))
        main_picture = Picture.objects.get(id=picture_id)
        main_tags = main_picture.tags.all()

        distances = {}
        pictures = Picture.objects.all()

        for picture in pictures:
            if str(picture.id) == picture_id:
                distances[picture_id] = 0
                continue

            common_tags = main_tags.intersection(picture.tags.all())
            dist = 0
            for tag in common_tags:
                freq = frequencies.get(tag=tag.tag).count
                dist += 1./freq + 0.01*random()

            distances[str(picture.id)] = dist

        n_closest = 5
        neighbors = []
        values = list(distances.values())
        for k in range(n_closest):
            closest_index = np.argmax(values)
            dist = values[closest_index]
            closest_id = str(list(distances.keys())[closest_index])

            # todo check if order
            (from_image, to_image) = (closest_id, picture_id) if closest_id < picture_id else (picture_id, closest_id)
            neighbors.append({
                'id': from_image + '__' + to_image,
                'from': from_image,
                'to': to_image,
                'width': 10*dist # voir ou on fait ça. Ptet pas top ici non plus
                });
            values[closest_index] *= -1
        return Response(neighbors)


class TagsView(APIView):

    def get(self, request, picture_id, format=None):
        tags = Picture.objects.get(id=picture_id).tags.all()
        response = [tag.tag for tag in tags]
        return Response(response)

    def post(self, request, picture_id, format=None):
        data_tags = request.data
        picture = Picture.objects.get(id=picture_id)
        picture.tags.clear()
        for data_tag in data_tags:
            tag = Tag.objects.get_or_create(tag=data_tag)[0]
            picture.tags.add(tag)
        return Response(data_tags)


class AllTagsView(APIView):
    def get(self, request, format=None):
        tags = Tag.objects.all()
        response = [tag.tag for tag in tags]
        return Response(response)

class GetRandomPicture(APIView):
    def get(self, request, format=None):
        count = Picture.objects.count()
        random_picture = Picture.objects.all()[randint(0, count - 1)]

        return Response({ 'id': random_picture.id })


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

def listPicturesLessTags(request):
    # todo. pour le moment, uniquement les photos sans tags
    pictures = Picture.objects.annotate(count_tags=Count('tags'))
    count_tags_min = pictures.aggregate(Min('count_tags'))['count_tags__min']
    pictures = pictures.filter(count_tags=count_tags_min)

    response = ''
    for index, picture in enumerate(pictures):
        response += "<a href='http://localhost:8080/edit/{}' target='_blank'>Image {}</a><br/>".format(picture.id, index)

    return HttpResponse(response)
