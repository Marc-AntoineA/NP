from .models import *
from django.db.models import Count, Min
from random import random
import numpy as np

def compute_distances_to(picture_id, frequencies=None):
    if frequencies is None:
        frequencies = Tag.objects.all().annotate(count=Count('picture'))
    main_picture = Picture.objects.get(id=picture_id)
    main_tags = main_picture.tags.all()

    distances = {}
    pictures = Picture.objects.all()

    for picture in pictures:
        if str(picture.id) == picture_id:
            distances[str(picture_id)] = 0
            continue

        common_tags = main_tags.intersection(picture.tags.all())
        dist = 0
        for tag in common_tags:
            freq = frequencies.get(tag=tag.tag).count
            dist += 1./freq + 0.01*random()

        distances[str(picture.id)] = dist
    return distances

def get_neighbors_from_distances(distances, nb_neighbors=5):
    neighbors = []
    values = list(distances.values())
    for k in range(nb_neighbors):
        closest_index = np.argmax(values)
        dist = values[closest_index]
        closest_id = str(list(distances.keys())[closest_index])
        neighbors.append(closest_id)
        values[closest_index] *= -1
    return neighbors
