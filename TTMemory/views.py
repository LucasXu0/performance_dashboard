from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse, JsonResponse
from rest_framework.views import APIView

from pyecharts.charts import Bar
from pyecharts import options as opts

import json
from random import randrange

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

def json_error(error_string='error', code=500, **kwargs):
    data = {
        'code': code,
        'msg': error_string,
        'data': {},
    }
    data.update(kwargs)
    return response_as_json(data)

JsonResponse = json_response
JsonError = json_error

def bar_base() -> Bar:
    c = (
        Bar()
        .add_xaxis(["衬衫", "羊毛衫", "雪纺衫", "裤子", "高跟鞋", "袜子"])
        .add_yaxis("商家A", [randrange(0, 100) for _ in range(6)])
        .add_yaxis("商家B", [randrange(0, 100) for _ in range(6)])
        .set_global_opts(title_opts=opts.TitleOpts(title="Bar-基本示例", subtitle="我是副标题"))
        .dump_options_with_quotes()
    )
    return c

def index(request):
    return HttpResponse("Hello World!")

def ChartViewGet(request):
    bb = json.loads(bar_base())
    return JsonResponse(bb)

def IndexViewGet(request):
    return HttpResponse(content=open('./templates/index.html').read())

# class ChartView(APIView):
#     def get(self, requeset, *arg, **kwargs):
#         return JsonResponse(json.loads())

# class IndexView(APIView):
#     def get(self, requeset, *arg, **kwargs):
#         return HttpResponse(content=open('./templates/index.html').read())