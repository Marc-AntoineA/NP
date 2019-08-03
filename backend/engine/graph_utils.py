from .models import *
from django.db.models import Count, Min, Max, Sum
from random import random
import numpy as np
import time
from math import inf

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
            distances[str(picture_id)] = 0
            continue
        common_tags = main_tags.intersection(picture.tags.all())
        dist = 0
        nb_tags = 0
        for tag in common_tags:
            freq = frequencies.get(tag=tag.tag).count
            dist += 1./freq + 0.1*random()
            nb_tags += 1
        end_int = time.time()
        if dist < 0.3:
            print(common_tags)
            nb_0 += 1
            time_0 += end_int - start_int
        # print('{} int {}'.format(dist, end_int - start_int))
        # dist /= nb_tags if nb_tags != 0 else 1
        distances[str(picture.id)] = dist#1./dist if dist != 0 else inf
    end = time.time()
    print('compute distances to : {} ms'.format(end - start))
    print('nb0 {}, time0 {}'.format(nb_0, time_0))
    return distances

def get_neighbors_from_distances(distances, nb_neighbors=20):
    list_distances = [(id, distance) for (id, distance) in distances.items()]
    list_distances.sort(key=lambda x: -x[1])
    return list_distances[:nb_neighbors]

def compute_neighbors_to(picture_id, nb_neighbors=20, frequencies=None):
    distances = compute_distances_to(picture_id, frequencies)
    neighbors = get_neighbors_from_distances(distances)

    from_picture = Picture.objects.get(id=picture_id)
    neighbors_db = Neighbors.objects.filter(from_picture=from_picture).delete()
    for (neighbor_id, distance) in neighbors:
        to_picture = Picture.objects.get(id=neighbor_id)
        neighbor_db = Neighbors(from_picture=from_picture, to_picture=to_picture, distance=distance)
        neighbor_db.save()

def has_to_be_computed_again(picture_id):
    try:
        neighbors = Neighbors.objects.get(from_picture__id=picture_id)
        last_uploaded_image_date = Picture.objects.all().aggregate(Max('created_at'))['created_at__max']
        return last_uploaded_image_date > neighbors.updated_at or len(neighbors.to_pictures.all()) == 0

    except Neighbors.DoesNotExist:
        neighbors = Neighbors(from_picture=Picture.objects.get(id=picture_id))
        neighbors.save()
        return True

def get_random_neighbors(picture_id, nb_neighbors=5):
    neighbors = Neighbors.objects.filter(from_picture__id=picture_id)
    sum_distances = neighbors.aggregate(Sum('distance'))['distance__sum']
    selected_neighbors = set()
    distances = [neighbor.distance for neighbor in neighbors]
    sum_cum_distances = np.cumsum(distances)
    n = len(sum_cum_distances)
    while len(selected_neighbors) < nb_neighbors:
        random_number = random()*sum_cum_distances[-1]
        print(selected_neighbors)
        for index in range(0, n - 1):
            if sum_cum_distances[index] < random_number < sum_cum_distances[index + 1]:
                id = str(neighbors[index].to_picture.id)
                selected_neighbors.add(id)
                break
        else:
            id = str(neighbors[n - 1].to_picture.id)
            selected_neighbors.add(id)
            pass

    return list(selected_neighbors)

def compute_matrix():
    tags = [tag.tag for tag in Tag.objects.all()]
    file = open('tmp.txt', 'w')
    pictures = Picture.objects.all()
    matrix = []
    file.write(','.join(tags) + '\n')
    for picture in pictures:
        picture__tags = picture.tags.all()
        picture__tags = [tag.tag for tag in picture__tags]
        tmp = ['1' if tag in picture__tags else '0' for tag in tags]
        matrix.append(tmp)
        file.write(','.join(tmp) + '\n')
