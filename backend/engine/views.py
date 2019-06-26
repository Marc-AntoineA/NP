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
from django.template import loader

import numpy as np
# todo rm utils
from .utils import load_database, compute_distances

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
                'width': 10*distances[image_id][closest - 1]
                });
            distances[image_id][closest - 1] *= -1
        return Response(neighbors)
