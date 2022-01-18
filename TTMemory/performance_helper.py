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
    def map_vc_events_to_marklines(cls, vc_events: list, white_list: list = VC_EVENTS_WHITE_LIST) -> list[opts.MarkLineItem]:
        marklines = []

        mlt_name = ''

        vc_events = [v for v in vc_events if v['name'] in white_list]

        for i in range(0, len(vc_events)):
            vc_event = vc_events[i]
            name = vc_event['name']
            index = vc_event['index']
            event_type = TTVCEventType(vc_event['event'])

            mlt_name += name + ' ' + event_type.toStr() + ' '

            if i < len(vc_events) - 1 and index == vc_events[i+1]['index']:
                continue

            marklines.append(opts.MarkLineItem(
                x=index,
                name=mlt_name,
                symbol='none',
            ))
            mlt_name = ''

        return marklines

    @classmethod
    def map_memory_json_to_line(cls, json_path: str) -> Line:
        line = Line()
        
        # 添加图表数据
        with open(json_path) as f:
            res = json.loads(f.read())
            # %.2f MB
            memory_usage = list(map(lambda x: round(x / 1024.0 / 1024.0, 2), res['memory_usage']))

            # 添加横坐标, 时间轴
            line.add_xaxis(range(0, len(memory_usage)))
            line.add_yaxis(
                y_axis=memory_usage,

                series_name='memory',
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
            cpu_usage = res['cpu_usage']
            line.add_yaxis(
                y_axis=cpu_usage,
                yaxis_index=1,

                series_name='cpu',
                symbol='none',

                itemstyle_opts=opts.ItemStyleOpts(color='#ff3d77'),
                label_opts=opts.LabelOpts(is_show=True),
                linestyle_opts=opts.LineStyleOpts(width=2),
                areastyle_opts=opts.AreaStyleOpts(
                    opacity=0.5,
                    color='#ff3d77'
                )
            )

        # 添加关键点
        marklines = PerformanceHelper.map_vc_events_to_marklines(res['vc_events'])
        line.set_series_opts(
            markline_opts=opts.MarkLineOpts(
                data=marklines,
                symbol='none',
            )
        )

        line.extend_axis(yaxis=opts.AxisOpts())

        # 设置图表信息
        line.set_global_opts(
            title_opts=opts.TitleOpts(title="内存分析"),
            tooltip_opts=opts.TooltipOpts(
                trigger="item", 
                axis_pointer_type="cross",
            ),
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
                opts.DataZoomOpts(range_start=0, range_end=20),
                opts.DataZoomOpts(type_='inside', range_start=0, range_end=20),
            ]
        )

        return line.dump_options_with_quotes()