from django.shortcuts import render, get_object_or_404
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework import status
from django.http import Http404, HttpResponse, HttpResponseForbidden
from rest_framework.renderers import TemplateHTMLRenderer
from django.db.models import F
from django.db import IntegrityError
from django.template import loader
from django.http import HttpResponse, Http404
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import FileSystemStorage
from django.db.models import Count, Min
from rest_framework_simplejwt.authentication import JWTAuthentication

import hashlib
from .models import *
import paramiko
from PIL import Image
import json
from random import random, randint
from .graph_utils import get_neighbors

class AllGraph(APIView):
    def get(self, request, format=None):
        graph = {}
        pictures = Picture.objects.all()
        frequencies = Tag.objects.all().annotate(count=Count('picture'))
        for picture in pictures:
            graph[str(picture.id)] = [id for (id, distance) in get_neighbors(picture.id, nb_neighbors=5, frequencies=frequencies)]
        return Response(graph)

class AllNeighborsOfNode(APIView):
    """
    List all neighbors available for a given node
    """

    # todo optim l'algo
    def get(self, request, picture_id, format=None):

        neighbors = get_neighbors(picture_id)#, nb_neighbors=5)
        neighbors_result = []
        for (neighbor_id, distance) in neighbors:
            # todo check if order
            (from_image, to_image) = (neighbor_id, picture_id) if neighbor_id < picture_id else (picture_id, neighbor_id)
            neighbors_result.append({
                'id': from_image + '__' + to_image,
                'from': from_image,
                'to': to_image,
                'tags_new_node': [tag.tag for tag in Picture.objects.get(id=neighbor_id).tags.all()],
                'distance': distance
                });
        return Response(neighbors_result)


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

        return Response({ 'id': random_picture.id, 'tags': [tag.tag for tag in random_picture.tags.all()] })


# todo warning.
@csrf_exempt
def test_upload_picture(request):
    if (not request.method) or ('picture' not in request.FILES):
        raise Http404


    picture_image = request.FILES['picture']
    hash = hashlib.sha224(picture_image.read()).hexdigest()

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

def delete_picture(request, picture_id):
    Picture.objects.get(id=picture_id).delete()
    return HttpResponse('done')


class ListPicturesLessTags(APIView):
    def get(self, request, nb_pictures, format=None):
        pictures = Picture.objects.annotate(nb_tags=Count('tags')).order_by('nb_tags')
        response = [{ 'id': picture.id, 'nb_tags': picture.nb_tags} for picture in pictures[:nb_pictures]]
        return Response(response)

def preview_private_picture(request, type, picture_id):
    try:
        token = request.GET.get('access_token')
        jWTAuthentication = JWTAuthentication()
        validated_token = jWTAuthentication.get_validated_token(raw_token=token)
        user = jWTAuthentication.get_user(validated_token=validated_token)

        picture = Picture.objects.get(id=picture_id)
        response = HttpResponse(content_type='image/jpg')
        response['X-Sendfile'] = '/var/www/static.phographe.marc-antoinea.fr/{}/{}.jpg'.format(type, picture_id)
        return response
    except:
        return HttpResponseForbidden()

def visualize_neighbors(request, picture_id):

    response = '<ul>'
    neighbors = get_neighbors(picture_id, 5)
    for (picture_id, distance) in neighbors:
        response += '<li> <img src="http://localhost/thumbnail/{}.jpg"></img>{} </li>'.format(picture_id, distance)

    response += '</ul>'

    return HttpResponse(response)
