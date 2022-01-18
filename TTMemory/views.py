from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
import json
from random import randrange

from .performance_helper import PerformanceHelper as PH
from django.views.decorators.csrf import csrf_exempt

from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.shortcuts import redirect

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
    return JsonResponse(json.loads(PH.map_memory_json_to_line('./jsons/performance.json')))

def show_memory(request):
    return HttpResponse(content=open('./templates/index.html').read())

def index(request):
    return HttpResponse(content=open('./templates/upload.html').read())

@csrf_exempt
def upload_performance_json(request):
    performance_json = request.FILES.get('performance_json')
    default_storage.delete('./jsons/performance.json')
    default_storage.save('./jsons/performance.json', ContentFile(performance_json.read()))
    return HttpResponse(JsonResponse({}))