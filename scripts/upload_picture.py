import requests
import os
import sys

api_url = 'http://localhost:8000/test/upload'

def send_data_to_server(image_filename):
    name_img= os.path.basename(image_filename)
    files = {'picture': (name_img, open(image_filename, 'rb'), 'multipart/form-data') }
    #print(open(image_filename, 'rb').readlines())
    response = requests.post(api_url, files=files)
    print(response)
    return response.status_code

if __name__ == '__main__':
    arg_image = sys.argv[1]
    print(arg_image)
    #for arg_image in range(1, 82):
    print(send_data_to_server(image_filename='../frontend/public/data/images_full/{}.jpg'.format(arg_image)))
