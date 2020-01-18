from PIL import Image

full_path = '/var/www/static.phographe.marc-antoinea.fr/full/'
save_path = './copy/'

import os

files = os.listdir(full_path)
# print(files)
# picture_id = 'a836b778-9525-4ca2-b20b-2e7458749901'

for picture_id in files:
    image = Image.open(full_path + picture_id)
    size = (1080, 1080)
    image.thumbnail(size)
    image.save(save_path + picture_id)
