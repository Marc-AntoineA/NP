from .models import *
from django.db.models import Count, Min, Max, Sum
from random import random
import numpy as np
import time
from math import inf, exp


def compute_distances_to(picture_id, frequencies=None):
    if frequencies is None:
        frequencies = Tag.objects.all().annotate(count=Count('picture'))
    main_picture = Picture.objects.get(id=picture_id)
    main_tags = main_picture.tags.all()

    distances = {}
    pictures = Picture.objects.all()
    start = time.time()

    nb_0 = 0
    time_0 = 0
    for picture in pictures:
        start_int = time.time()
        if str(picture.id) == picture_id:
            distances[str(picture_id)] = 99999999
            continue
        common_tags = main_tags.intersection(picture.tags.all())
        dist = 0
        nb_tags = 0
        for tag in common_tags:
            freq = frequencies.get(tag=tag.tag).count
            dist += 1./freq + 0.01*random()
            nb_tags += 1
        end_int = time.time()
        if dist < 0.3:
            nb_0 += 1
            time_0 += end_int - start_int
        distances[str(picture.id)] = 1/dist if dist != 0 else 999999
    end = time.time()
    print('compute distances to : {} ms'.format(end - start))
    print('nb0 {}, time0 {}'.format(nb_0, time_0))
    return distances

def has_to_be_computed(picture_id, nb_neighbors=20):
    neighbors = Neighbors.objects.filter(from_picture__id=picture_id)
    if 0 in [n.distance for n in neighbors]:
        return True
    if len(neighbors) < nb_neighbors:
        return True
    last_uploaded_image_date = Picture.objects.all().aggregate(Max('created_at'))['created_at__max']
    return last_uploaded_image_date > neighbors[0].updated_at == 0


def compute_neighbors(picture_id, frequencies=None, nb_neighbors=20):
    distances_to = compute_distances_to(picture_id, frequencies)
    list_distances = [(id, distance) for (id, distance) in distances_to.items()]
    list_distances.sort(key=lambda x: x[1])
    neighbors = list_distances[:nb_neighbors]

    from_picture = Picture.objects.get(id=picture_id)
    neighbors_db = Neighbors.objects.filter(from_picture=from_picture).delete()
    for (neighbor_id, distance) in neighbors:
        to_picture = Picture.objects.get(id=neighbor_id)
        neighbor_db = Neighbors(from_picture=from_picture, to_picture=to_picture, distance=distance)
        neighbor_db.save()


def get_neighbors(picture_id, nb_neighbors=5, frequencies=None):
    if has_to_be_computed(picture_id, nb_neighbors):
        compute_neighbors(picture_id, nb_neighbors=nb_neighbors*5, frequencies=frequencies)

    neighbors = Neighbors.objects.filter(from_picture__id=picture_id).order_by('distance')
    sum_cum_weights = [0]
    for neighbor in neighbors:
        sum_cum_weights.append(sum_cum_weights[-1] + 1./neighbor.distance)
    print(sum_cum_weights)

    n = neighbors.count()
    selected_neighbors = set()
    while len(selected_neighbors) < nb_neighbors:
        random_value = sum_cum_weights[-1]*random()
        print(random_value)
        for picture_index in range(n):
            if random_value < sum_cum_weights[picture_index + 1]:
                for k in range(picture_index, n):
                    sum_cum_weights[k + 1] -= sum_cum_weights[picture_index + 1]
                neighbor = neighbors[picture_index]
                selected_neighbors.add((str(neighbor.to_picture.id), neighbor.distance))
                break
        else:
            assert False
    return list(selected_neighbors)
