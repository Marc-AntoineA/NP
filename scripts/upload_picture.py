import requests
import os
import sys

api_url = 'http://localhost:8000/picture/upload'

def send_data_to_server(image_filename):
    name_img= os.path.basename(image_filename)
    files = {'picture': (name_img, open(image_filename, 'rb'), 'multipart/form-data') }
    #print(open(image_filename, 'rb').readlines())
    response = requests.post(api_url, files=files)
    return response.status_code

if __name__ == '__main__':
    dir = sys.argv[1]
    images = os.listdir(dir)
    for image in images:
        if not '.' in image:
            print(image)
            continue
        response = send_data_to_server(image_filename=dir + image)
        print(response)
