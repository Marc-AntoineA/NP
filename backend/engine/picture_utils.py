
from .models import Picture
from PIL import Image
import imagehash

def update_all_hashes():
    pictures = Picture.objects.all()
    for picture in pictures:
        path = '/var/www/static.phographe.marc-antoinea.fr/thumbnail/{}.jpg'.format(picture.id)
        hash = str(imagehash.whash(Image.open(path)))
        picture.hash = hash
        try:
            picture.save()
        except:
            print('Double hash')
            same_picture = Picture.objects.filter(hash=hash)
            print(same_picture)
            print(picture.id)
