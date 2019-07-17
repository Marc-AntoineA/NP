from .models import *
from django.db.models import Count, Min, Max
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
            dist += 1./freq + 0.1*random()

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

def compute_neighbors_to(picture_id, nb_neighbors=5, frequencies=None):
    distances = compute_distances_to(picture_id, frequencies)
    to_pictures_id = get_neighbors_from_distances(distances)
    neighbors = Neighbors.objects.get(from_picture__id=picture_id)
    neighbors.to_pictures.clear()
    for to_picture_id in to_pictures_id:
        print(to_picture_id)
        neighbors.to_pictures.add(Picture.objects.get(id=to_picture_id))
    neighbors.save()

def has_to_be_computed_again(picture_id):
    try:
        neighbors = Neighbors.objects.get(from_picture__id=picture_id)
        last_uploaded_image_date = Picture.objects.all().aggregate(Max('created_at'))['created_at__max']
        return last_uploaded_image_date > neighbors.updated_at or len(neighbors.to_pictures.all()) == 0

    except Neighbors.DoesNotExist:
        neighbors = Neighbors(from_picture=Picture.objects.get(id=picture_id))
        neighbors.save()
        return True
