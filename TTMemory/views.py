from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse, JsonResponse
from rest_framework.views import APIView

from pyecharts.charts import Bar
from pyecharts.charts import Line
from pyecharts import options as opts
from pyecharts.commons.utils import JsCode

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

JsonResponse = json_response

def bar_base() -> Bar:
    c = (
        Bar()
        .add_xaxis(["衬衫", "羊毛衫", "雪纺衫", "裤子", "高跟鞋", "袜子"])
        .add_yaxis("商家A", [randrange(0, 100) for _ in range(6)])
        #.add_yaxis("商家B", [randrange(0, 100) for _ in range(6)])
        .set_global_opts(title_opts=opts.TitleOpts(title="Bar-基本示例", subtitle="我是副标题"))
        .dump_options_with_quotes()
    )
    return c

def memorys() -> Line:
    line = Line()
    
    with open('./jsons/raw_memory_records.json') as f:
        res = json.loads(f.read())
        memorys = list(map(lambda x: round(x / 1024.0 / 1024.0, 2), res['memorys']))
        line.add_xaxis(range(1, len(memorys)))
        line.add_yaxis(
            series_name='memory',
            y_axis=memorys,
            itemstyle_opts=opts.ItemStyleOpts(
                color='#2860a0'
            ),
            symbol='none',
            label_opts=opts.LabelOpts(is_show=True),
            linestyle_opts=opts.LineStyleOpts(width=2),
            areastyle_opts=opts.AreaStyleOpts(
                opacity=0.5,
                color='#2860a0'
            )
        )

        # markareas = list(map(lambda event: opts.MarkAreaItem(name=event['name'] + str(event['event']), x=(event['index'], event['index'] + 1), itemstyle_opts=opts.ItemStyleOpts(color='red', opacity=0.2)), res['vc_events']))
        # line.set_series_opts(
        #     markarea_opts=opts.MarkAreaOpts(
        #         data=markareas
        #     )
        # )
        
        marklines = list(map(lambda event: opts.MarkLineItem(x=event['index'], symbol='none', name=event['name']), res['vc_events']))
        line.set_series_opts(
            markline_opts=opts.MarkLineOpts(
                data=marklines,
                symbol='none',
            )
        )

    line.set_global_opts(
        title_opts=opts.TitleOpts(title="内存分析"),
        tooltip_opts=opts.TooltipOpts(trigger="item", axis_pointer_type="cross"),
        xaxis_opts=opts.AxisOpts(
            type_='category',
            boundary_gap=False,
        ),
        yaxis_opts=opts.AxisOpts(
            type_='value', 
            axistick_opts=opts.AxisTickOpts(is_show=True),
            splitline_opts=opts.SplitLineOpts(is_show=True),
        ),
        datazoom_opts=[
            opts.DataZoomOpts(range_start=0, range_end=10),
            opts.DataZoomOpts(type_='inside', range_start=0, range_end=10),
        ]
    )

    return (line.dump_options_with_quotes())

def fetch_memory(request):
    return JsonResponse(json.loads(memorys()))

def show_memory(request):
    return HttpResponse(content=open('./templates/index.html').read())