import numpy as np
from matplotlib import pyplot as plt
from random import random


def load_database(filename):
    with open(filename, 'r') as f:
        lines = f.readlines()
        header = lines[0].strip().split(',')
        images = [line.strip().split(',') for line in lines[1:]]
        images = [[int(image[0])] + image[1:] for image in images]
        images.sort(key = lambda image: image[0])
        return (header, images)


def compute_distances(header, images):
    tags = header[2:]
    images_tags = [image[2:] for image in images]
    tags_frequencies = []
    for tag_index in range(len(tags)):
        tags_frequencies.append(0)
        for image_tags in images_tags:
            if image_tags[tag_index] != 'x':
                continue
            tags_frequencies[tag_index] += 1

    distances = []
    n_images = len(images_tags)
    n_tags = len(tags)
    for from_image_index in range(n_images):
        dist_to_images = [0]*n_images
        from_image = images_tags[from_image_index]
        for to_image_index in range(n_images):
            if to_image_index == from_image_index:
                continue
            to_image = images_tags[to_image_index]

            for tag_index in range(n_tags):
                if from_image[tag_index] == '':
                    continue
                if to_image[tag_index] == from_image[tag_index]:
                    dist_to_images[to_image_index] += 1./tags_frequencies[tag_index] + 0.01*random()
        distances.append(dist_to_images)
    return distances
