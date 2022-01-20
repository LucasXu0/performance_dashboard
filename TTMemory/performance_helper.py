from datetime import timedelta
from sqlite3 import Timestamp
import time
from pyecharts import options as opts
from pyecharts.charts import Line

from enum import IntEnum

import json


class TTVCEventType(IntEnum):
    TTVCEventTypeInit = 1,
    TTVCEventTypeViewDidLoad = 2,
    TTVCEventTypeViewWillAppear = 3,
    TTVCEventTypeViewDidAppear = 4,
    TTVCEventTypeViewWillDisAppear = 5,
    TTVCEventTypeViewDidDisAppear = 6,
    TTVCEventTypeDealloc = 7,

    def toStr(self) -> str:
        if self == TTVCEventType.TTVCEventTypeInit:
            return 'init'
        elif self == TTVCEventType.TTVCEventTypeViewDidLoad:
            return 'viewDidLoad'
        elif self == TTVCEventType.TTVCEventTypeViewWillAppear:
            return 'viewWillAppear'
        elif self == TTVCEventType.TTVCEventTypeViewDidAppear:
            return 'viewDidAppear'
        elif self == TTVCEventType.TTVCEventTypeViewWillDisAppear:
            return 'viewWillDisAppear'
        elif self == TTVCEventType.TTVCEventTypeViewDidDisAppear:
            return 'viewDidDisAppear'
        elif self == TTVCEventType.TTVCEventTypeDealloc:
            return 'dealloc'


class PerformanceHelper:

    VC_EVENTS_WHITE_LIST = [
        'SSZMCameraViewController',
        'SSZMECommonSelectMediaViewController',
        'SSZMEditViewController',
        'SSZMEMagicViewController',
    ]

    # 1. 过滤无用vc
    # 2. 聚合同一时间点数据
    @classmethod
    def map_events_to_marklines(cls, events: list, filter_type = 1, white_list = VC_EVENTS_WHITE_LIST) -> list:

        if filter_type != 1:
            white_list = []
        
        marklines = []

        mlt_name = ''

        events = [v for v in events if 'type' not in v.keys() or ('type' in v.keys() and v['type'] != filter_type)]
        events = [v for v in events if v['name'] in white_list]

        for i in range(0, len(events)):
            event = events[i]
            name = event['name']
            index = event['index']

            mlt_name += name + ' '

            if 'ext_type' in event.keys():
                ext_type = TTVCEventType(event['ext_type'])
                mlt_name += ext_type.toStr() + ' '

            if i < len(events) - 1 and index == events[i+1]['index']:
                continue

            marklines.append(opts.MarkLineItem(
                x=index,
                name=mlt_name,
                symbol='none',
            ))
            mlt_name = ''

        return marklines

    @classmethod
    def map_memory_json_to_line(cls, json_path: str, filter_type) -> Line:
        memroy_line = Line()
        cpu_line = Line()
        
        app_name = ''
        bundle_id = ''
        version = ''
        build_number = ''
        begin = ''
        end = ''

        # 添加图表数据
        with open(json_path) as f:
            res = json.loads(f.read())

            # basic info
            app_name = res['app_name']
            bundle_id = res['bundle_id']
            version = res['version']
            build_number = res['build_number']
            begin = time.strftime('%Y-%m-%d %H:%M', time.localtime(res['begin'] + 60 * 60 * 8))
            end = time.strftime('%Y-%m-%d %H:%M', time.localtime(res['end'] + 60 * 60 * 8))

            # %.2f MB
            memory_usage = list(map(lambda x: round(x / 1024.0 / 1024.0, 2), res['memory_usage']))

            # 添加横坐标, 时间轴
            memroy_line.add_xaxis(range(0, len(memory_usage)))
            memroy_line.add_yaxis(
                y_axis=memory_usage,

                series_name='memory usage',
                symbol='none',
                
                itemstyle_opts=opts.ItemStyleOpts(color='#2860a0'),
                label_opts=opts.LabelOpts(is_show=True),
                linestyle_opts=opts.LineStyleOpts(width=2),
                areastyle_opts=opts.AreaStyleOpts(
                    opacity=0.5,
                    color='#2860a0'
                )
            )

            # 
            cpu_usage = list(map(lambda x: round(x, 2), res['cpu_usage']))
            cpu_line.add_xaxis(range(0, len(cpu_usage)))
            cpu_line.add_yaxis(
                y_axis=cpu_usage,
                yaxis_index=1,

                series_name='cpu usage',
                symbol='none',

                itemstyle_opts=opts.ItemStyleOpts(color='#ff3d77'),
                label_opts=opts.LabelOpts(
                    is_show=True,
                    formatter='{@[1]}%'
                ),
                linestyle_opts=opts.LineStyleOpts(width=2),
                areastyle_opts=opts.AreaStyleOpts(
                    opacity=0.5,
                    color='#ff3d77'
                ),
            )

        # 添加关键点
        if not filter_type:
            filter_type = 1
        marklines = PerformanceHelper.map_events_to_marklines(res['vc_events'], filter_type)
        memroy_line.set_series_opts(
            markline_opts=opts.MarkLineOpts(
                data=marklines,
                symbol='none',
                linestyle_opts=opts.LineStyleOpts(
                    color='black',
                    type_='dashed'
                )
            )
        )

        memroy_line.extend_axis(yaxis=opts.AxisOpts(
            axislabel_opts=opts.LabelOpts(
                formatter='{value}%'
            )
        ))

        # 设置图表信息
        memroy_line.set_global_opts(
            title_opts=opts.TitleOpts(title='性能分析(内测版) - {}'.format(app_name), subtitle='{} ~ {}\n{}-{}\n{}'.format(begin, end, version, build_number, bundle_id)),
            tooltip_opts=opts.TooltipOpts(
                trigger="item", 
                axis_pointer_type="cross",
            ),
            xaxis_opts=opts.AxisOpts(
                type_='category',
                boundary_gap=True,
            ),
            yaxis_opts=opts.AxisOpts(
                type_='value', 
                axistick_opts=opts.AxisTickOpts(is_show=True),
                splitline_opts=opts.SplitLineOpts(is_show=True),
            ),
            datazoom_opts=[
                opts.DataZoomOpts(range_start=0, range_end=20),
                opts.DataZoomOpts(type_='inside', range_start=0, range_end=20),
            ]
        )

        return memroy_line.overlap(cpu_line).dump_options_with_quotes()