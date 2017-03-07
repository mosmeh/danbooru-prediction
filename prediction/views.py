from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader

from models import Classifier

import os
import base64
import urllib
from PIL import Image

def index(request):
    context = {
        'num_characters': Classifier.num_characters(),
        'num_tags': Classifier.num_tags(),
    }
    return render(request, 'index.html', context)

def result(request):
    if 'img' in request.FILES:
        with open('image', 'wb') as destination:
            for chunk in request.FILES['img'].chunks():
                destination.write(chunk)
    else:
        urllib.urlretrieve(request.POST['url'], 'image')

    img = Image.open('image')
    res = Classifier.predict(img)[:50]

    os.system('convert -resize 500x500 image resized.png')
    context = {
        'img': 'data:image/png;base64,' + base64.b64encode(open('resized.png', 'rt').read()),
        'top_prediction': res[0],
        'predictions': res[1:]
    }
    return render(request, 'result.html', context)
