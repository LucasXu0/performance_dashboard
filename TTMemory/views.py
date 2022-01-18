from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse, JsonResponse
import json
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
    return JsonResponse(json.loads(PH.map_memory_json_to_line('./jsons/raw_memory_records.json')))

def show_memory(request):
    return HttpResponse(content=open('./templates/index.html').read())