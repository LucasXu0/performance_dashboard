from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.shortcuts import redirect

import json
import time
import os

from random import randrange
from .performance_helper import PerformanceHelper as PH

def response_as_json(data):
    json_str = json.dumps(data)
    resp = HttpResponse(json_str, content_type='application/json',)
    resp['Access-Control-Allow-Origin'] = '*'
    return resp

def json_response(data, code=200):
    data = {
        'code': code,
        'msg': 'success',
        'data': data,
    }
    return response_as_json(data)

JsonResponse = json_response

def fetch_memory(request):
    path = request.GET.get('path')
    filter_type = request.GET.get('filter_type')
    return JsonResponse(json.loads(PH.map_memory_json_to_line(path, filter_type)))

def show_memory(request):
    return HttpResponse(content=open('./templates/show.html').read())

def index(request):
    return HttpResponse(content=open('./templates/index.html').read())

@csrf_exempt
def upload_performance_json(request):
    performance_json = request.FILES.get('performance_json')
    now = int(round((time.time() + 60 * 60 * 8) * 1000))
    path = './jsons/performance_' + time.strftime('%Y_%m_%d_%H_%M_%S', time.localtime(now / 1000)) + '.json'
    default_storage.save(path, ContentFile(performance_json.read()))
    return HttpResponse(JsonResponse({
        'path': path
    }))

def fetch_performance_files(request):
    file_names = []
    for fn in os.listdir('./jsons'):
        if not fn.endswith('.json'):
            continue
        file_names.append({
            'file_name': './jsons/' + fn
        })
    return HttpResponse(json.dumps(file_names))