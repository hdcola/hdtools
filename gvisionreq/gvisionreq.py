# -*- coding: utf-8 -*-

from base64 import b64encode
from os import makedirs
from os.path import join, basename
from sys import argv
import json
import requests
import getopt
import sys

ENDPOINT_URL = 'https://vision.googleapis.com/v1/images:annotate'
RESULTS_DIR = 'jsons'
makedirs(RESULTS_DIR, exist_ok=True)

def make_image_data_list(image_filename):
    img_requests = []
    with open(image_filename, 'rb') as f:
        ctxt = b64encode(f.read()).decode()
        img_requests.append({
                'image': {'content': ctxt},
                'features': [{
                    'type': 'TEXT_DETECTION',
                    'maxResults': 1
                }]
        })
    return img_requests

def make_image_data(image_filename):
    """Returns the image data lists as bytes"""
    imgdict = make_image_data_list(image_filename)
    return json.dumps({"requests": imgdict }).encode()


def request_ocr(api_key, image_filename):
    response = requests.post(ENDPOINT_URL,
                             data=make_image_data(image_filename),
                             params={'key': api_key},
                             headers={'Content-Type': 'application/json'})
    return response


def help():
    print('gvisionreq.py -t -c -k <apikey> image_files...')
    return


if __name__ == '__main__':
    api_key = ''
    only_text = False
    read_cache = False

    try:
        opts, image_filenames = getopt.getopt(sys.argv[1:],"hk:tc",["key=","text","cache"])
    except getopt.GetoptError:
        help()
        sys.exit(2)

    for opt, arg in opts:
        if opt == '-h':
            help()
            sys.exit()
        elif opt in ("-k","--key"):
            api_key = arg
        elif opt in ("-t","--text"):
            only_text = True
        elif opt in ("-c","--cache"):
            read_cache = True
    
    if api_key == "" or len(image_filenames) == 0 :
        help()
        sys.exit()

    for image_filename in image_filenames :
        # cache file
        jpath = join(RESULTS_DIR, basename(image_filename) + '.json')

        datatxt = ""

        if read_cache :
            try:
                with open(jpath, 'r') as f:
                    resp = json.load(f)
                    datatxt = json.dumps(resp, indent=2)
            except FileNotFoundError:
                read_cache = False

        if datatxt == "" :
            response = request_ocr(api_key, image_filename)
            if response.status_code != 200 or response.json().get('error'):
                sys.stderr.write(response.text)
            else:
                for idx, resp in enumerate(response.json()['responses']):
                    # save to JSON file
                    with open(jpath, 'w') as f:
                        datatxt = json.dumps(resp, indent=2)
                        f.write(datatxt)

        t = resp['textAnnotations'][0]

        if not only_text :
            print("Wrote", len(datatxt), "bytes to", jpath)
            print("---------------------------------------------")
            print("    Bounding Polygon:")
            print(t['boundingPoly'])
            print("    Text:")

        print(t['description'])
