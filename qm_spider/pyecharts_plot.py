from qm_spider import *
from pyecharts.faker import Faker
from pyecharts import options as opts
from pyecharts.charts import Bar, Grid, Line, Page, Pie, Timeline, Boxplot, WordCloud, Graph, Scatter
from pyecharts.commons.utils import JsCode
from pyecharts.globals import ThemeType, SymbolType
from pyecharts.render import make_snapshot
from snapshot_selenium import snapshot
from collections import Counter


# 画图基础通用参数；
# class Pyecharts_Var:
#     def __init__(self, title, x_value, y_name, y_value, *args, subtitle='', is_symbol_show=False, line_width=2, is_show=False, color_list=['#00b088', '#f76b61', '#ffb55d', '#8470ff', '#00a2ff', '#ffe400', '#11d2c2', '#c263f9']):
#         self.subtitle = subtitle
#         self.is_symbol_show = is_symbol_show
#         self.line_width = line_width
#         self.is_show = is_show
#         self.color_list = color_list
#         self.args = args
#         self.title = title
#         self.x_value = [str(i) for i in x_value]
#         self.y_name = y_name
#         self.y_value = [float(i) for i in y_value]
#
#     def render_to_png(self, c):
#         make_snapshot(snapshot, c.render(), "./%s.png" %(self.title))

# 折线图、面积图；
class Line_Py:
    def __init__(self, title, x_value, y_name, y_value, *args, pos_top='top', is_zoom=False, boundary_gap=False, is_orient='horizontal', y_is_inverse=False, x_is_inverse=False, legend_icon='roundRect', subtitle='', is_symbol_show=False, line_width=2, is_show=False, color_list=['#00b088', '#f76b61', '#ffb55d', '#8470ff', '#00a2ff', '#ffe400', '#11d2c2', '#c263f9']):
        """
            * 若是有args传参，参数示例：*[['1', '2', '3'], [[136,176, 177], [209, 163, 223], [244, 235, 321]]；
            * 第一个列表是Y轴的数据名称列表，第二个列表是每个Y轴对应的数据；
        """
        self.pos_top = pos_top
        self.legend_icon = legend_icon
        self.is_zoom = is_zoom
        self.is_orient = is_orient
        self.subtitle = subtitle
        self.is_symbol_show = is_symbol_show
        self.line_width = line_width
        self.is_show = is_show
        self.color_list = color_list
        self.args = args
        self.title = title
        self.x_value = [str(i) for i in x_value]
        self.y_name = y_name
        self.y_value = [float(i) for i in y_value]
        self.y_is_inverse = y_is_inverse
        self.x_is_inverse = x_is_inverse
        self.boundary_gap = boundary_gap
        if self.y_is_inverse == True:
            self.y_min = 1
            self.y_max = None
        else:
            self.y_min = None
            self.y_max = 'dataMax'
        if self.x_is_inverse == True:
            self.x_min = 1
        else:
            self.x_min = None

    def render_to_png(self, c):
        make_snapshot(snapshot, c.render(), "./%s.png" %(self.title))

    def line_render_air(self):
        c = Line()
        c.add_xaxis(self.x_value)
        c.add_yaxis(
            series_name=self.y_name,
            y_axis = self.y_value,
            is_symbol_show=self.is_symbol_show,
            linestyle_opts=opts.LineStyleOpts(width=self.line_width),
            label_opts=opts.LabelOpts(is_show=self.is_show)
        )
        c.set_global_opts(
            title_opts=opts.TitleOpts(title=self.title, subtitle=self.subtitle),
            tooltip_opts=opts.TooltipOpts(trigger="axis"),
            legend_opts=opts.LegendOpts(pos_left="center", pos_top=self.pos_top, legend_icon=self.legend_icon),
            datazoom_opts=opts.DataZoomOpts(
                is_show=self.is_zoom,
                range_start=0,
                range_end=100,
                orient=self.is_orient  # 表示横轴可滑动还是纵轴可滑动；
            ),
            yaxis_opts=opts.AxisOpts(
                type_="value",
                max_=self.y_max,
                min_=self.y_min,
                boundary_gap=self.boundary_gap,  # 封闭坐标轴，左右都有顶上的刻度线；
                axislabel_opts=opts.LabelOpts(color="#7D7D7D"),
                axisline_opts=opts.AxisLineOpts(
                    linestyle_opts=opts.LineStyleOpts(width=1.5, color="#A0A7B3")
                ),
                axistick_opts=opts.AxisTickOpts(is_show=True, is_inside=True),
                splitline_opts=opts.SplitLineOpts(
                    is_show=True, linestyle_opts=opts.LineStyleOpts(color="#E2E2E2")
                ),  # 设置网格线；
            ),
            xaxis_opts=opts.AxisOpts(
                type_="category",
                min_=self.x_min,
                boundary_gap=self.boundary_gap,
                axislabel_opts=opts.LabelOpts(color="#7D7D7D"),
                axisline_opts=opts.AxisLineOpts(
                    linestyle_opts=opts.LineStyleOpts(width=1.5, color="#A0A7B3")
                ),
                axistick_opts=opts.AxisTickOpts(is_show=True, is_inside=True),
                splitline_opts=opts.SplitLineOpts(
                    is_show=True, linestyle_opts=opts.LineStyleOpts(color="#E2E2E2")
                ),
            ),
        )
        if len(self.args) > 0:
            for num in range(len(self.args[0])):
                c.add_yaxis(
                    series_name = self.args[0][num],
                    y_axis = self.args[1][num],
                    is_symbol_show=self.is_symbol_show,
                    linestyle_opts=opts.LineStyleOpts(width=self.line_width),
                    label_opts=opts.LabelOpts(is_show=self.is_show)
                )
        self.c_render = c
        return c

    def line_render_qimai(self):
        c = Line(init_opts=opts.InitOpts(width="1200px", height="400px"))
        # c = Line()
        c.add_xaxis(self.x_value)
        c.add_yaxis(
            series_name=self.y_name,
            y_axis=self.y_value,
            is_symbol_show=self.is_symbol_show,  # 线上不用点标记
            color=self.color_list[0],
            linestyle_opts=opts.LineStyleOpts(width=self.line_width),  # 线条加粗
            label_opts=opts.LabelOpts(is_show=self.is_show)
        )
        c.set_global_opts(
            title_opts=opts.TitleOpts(
                title=self.title,
                pos_top="2%",  # 距离顶层2%
                pos_left="center",
                title_textstyle_opts=opts.TextStyleOpts(
                    color="#666", font_size=16, font_weight='normal', font_family='Microsoft YaHei'
                ),
            ),
            tooltip_opts=opts.TooltipOpts(trigger="axis"),
            # legend_opts=opts.LegendOpts(pos_left="center", pos_top=self.pos_top, legend_icon='circle'),
            legend_opts=opts.LegendOpts(pos_left="center", pos_top='bottom', legend_icon='circle'),
            yaxis_opts=opts.AxisOpts(
                type_="value",
                max_=self.y_max,
                min_=self.y_min,
                is_inverse=self.y_is_inverse,  # 反向Y轴；
                boundary_gap=self.boundary_gap,  # 封闭坐标轴，左右都有顶上的刻度线；
                axislabel_opts=opts.LabelOpts(color="#7D7D7D"),
                axisline_opts=opts.AxisLineOpts(
                    linestyle_opts=opts.LineStyleOpts(width=1.5, color="#A0A7B3")
                ),
                axistick_opts=opts.AxisTickOpts(is_show=True, is_inside=True),
                splitline_opts=opts.SplitLineOpts(
                    is_show=True, linestyle_opts=opts.LineStyleOpts(color="#E2E2E2")
                ),  # 设置网格线；
            ),
            xaxis_opts=opts.AxisOpts(
                type_="category",
                min_=self.x_min,
                boundary_gap=self.boundary_gap,
                is_inverse=self.x_is_inverse,  # 反向X轴；
                axislabel_opts=opts.LabelOpts(color="#7D7D7D"),
                axisline_opts=opts.AxisLineOpts(
                    linestyle_opts=opts.LineStyleOpts(width=1.5, color="#A0A7B3")
                ),
                axistick_opts=opts.AxisTickOpts(is_show=True, is_inside=True),
                splitline_opts=opts.SplitLineOpts(
                    is_show=True, linestyle_opts=opts.LineStyleOpts(color="#E2E2E2")
                ),
            ),
            graphic_opts=[
                opts.GraphicGroup(
                    graphic_item=opts.GraphicItem(
                        rotation=JsCode("Math.PI / 500"),
                        bounding="raw",
                        right=700,
                        bottom=150,
                        z=100,
                    ),
                    children=[
                        opts.GraphicRect(
                            graphic_item=opts.GraphicItem(
                                left="center", top="center", z=100
                            ),
                            graphic_shape_opts=opts.GraphicShapeOpts(
                                width=400, height=50
                            ),
                            graphic_basicstyle_opts=opts.GraphicBasicStyleOpts(
                                fill="rgba(0,0,0,0)"
                            ),
                        ),
                        opts.GraphicText(
                            graphic_item=opts.GraphicItem(
                                left="center", top="center", z=100
                            ),
                            graphic_textstyle_opts=opts.GraphicTextStyleOpts(
                                text="七麦数据",
                                # font="bold 26px Microsoft YaHei",
                                font="26px Microsoft YaHei",
                                graphic_basicstyle_opts=opts.GraphicBasicStyleOpts(
                                    fill="#D5D5D5"
                                ),
                            ),
                        ),
                    ],
                )
            ],
            # 下方为图片水印代码；
            #             graphic_opts=[
            #                 opts.GraphicImage(
            #                     graphic_item=opts.GraphicItem(
            #                         id_="logo",
            #                         left='142',
            #                         z='10',
            #                         # 距离上边界距离
            #                         top='340',
            #                         # 负数则显示在图表下层
            #                         z_level=-1
            #                     ),
            #                     graphic_imagestyle_opts=opts.GraphicImageStyleOpts(
            #                         # 指定图片地址，最好选用png
            #                         image="https://tva1.sinaimg.cn/large/008eGmZEly1gmfcjqkwrkj302q00mq2q.jpg",
            #                         # 长设置
            #                         width=100,
            #                         height=23,
            #                         opacity=1,
            #                     ),
            #                 ),
            #             ]
        )
        # 插入其他y线条；
        if len(self.args) > 0:
            for num in range(len(self.args[0])):
                if num+1 > len(self.color_list)-1:
                    color_str = ''
                else:
                    color_str = self.color_list[num+1]
                c.add_yaxis(
                    series_name=self.args[0][num],
                    y_axis=self.args[1][num],
                    is_symbol_show=self.is_symbol_show,  # 线上不用点标记
                    color=color_str,
                    linestyle_opts=opts.LineStyleOpts(width=self.line_width),  # 线条加粗
                    label_opts=opts.LabelOpts(is_show=self.is_show),
                )
        self.c_render = c
        return c

# 柱状图；
class Bar_Py:
    def __init__(self, title, x_value, y_name, y_value, *args, reversal_axis=True, pos_top='top', is_zoom=False, boundary_gap=False, is_orient='horizontal', legend_icon='roundRect', subtitle='', is_show=False):
        self.reversal_axis = reversal_axis
        self.pos_top = pos_top
        self.legend_icon = legend_icon
        self.is_zoom = is_zoom
        self.is_orient = is_orient
        self.subtitle = subtitle
        self.is_show = is_show
        self.args = args
        self.title = title
        self.x_value = [str(i) for i in x_value]
        self.y_name = y_name
        self.y_value = [float(i) for i in y_value]
        self.boundary_gap = boundary_gap
        # , is_symbol_show = False, line_width = 2, color_list = ['#00b088', '#f76b61', '#ffb55d', '#8470ff', '#00a2ff', '#ffe400', '#11d2c2', '#c263f9']
        # self.color_list = color_list
        # self.is_symbol_show = is_symbol_show
        # self.line_width = line_width

    def render_to_png(self, c):
        make_snapshot(snapshot, c.render(), "./%s.png" %(self.title))

    def bar_render_general(self):
        c = Bar()
        c.add_xaxis(self.x_value)
        c.add_yaxis(
            self.y_name,
            self.y_value,
            label_opts=opts.LabelOpts(is_show=self.is_show)
        )
        if self.reversal_axis==True:
            c.reversal_axis()
        c.set_series_opts(label_opts=opts.LabelOpts(position="right"))
        c.set_global_opts(
            title_opts=opts.TitleOpts(title=self.title, subtitle=self.subtitle),
            tooltip_opts=opts.TooltipOpts(trigger="axis"),
            legend_opts=opts.LegendOpts(pos_left="center", pos_top=self.pos_top, legend_icon=self.legend_icon),
        )
        if len(self.args) > 0:
            for num in range(len(self.args[0])):
                c.add_yaxis(
                    series_name = self.args[0][num],
                    y_axis = self.args[1][num],
                    label_opts=opts.LabelOpts(is_show=self.is_show)
                )
        return c

    def bar_render_air(self):
        c = Bar()
        c.add_xaxis(self.x_value)
        c.add_yaxis(
            self.y_name,
            self.y_value,
            label_opts=opts.LabelOpts(is_show=self.is_show)
        )
        c.set_global_opts(
            title_opts=opts.TitleOpts(title=self.title, subtitle=self.subtitle),
            tooltip_opts=opts.TooltipOpts(trigger="axis"),
            legend_opts=opts.LegendOpts(pos_left="center", pos_top=self.pos_top, legend_icon=self.legend_icon),
            datazoom_opts=opts.DataZoomOpts(
                is_show=self.is_zoom,
                range_start=0,
                range_end=100,
                orient=self.is_orient  # 表示横轴可滑动还是纵轴可滑动；
            ),
            yaxis_opts=opts.AxisOpts(
                type_="value",
                max_='dataMax',
                boundary_gap=self.boundary_gap,  # 封闭坐标轴，左右都有顶上的刻度线；
                axislabel_opts=opts.LabelOpts(color="#7D7D7D"),
                axisline_opts=opts.AxisLineOpts(
                    linestyle_opts=opts.LineStyleOpts(width=1.5, color="#A0A7B3")
                ),
                axistick_opts=opts.AxisTickOpts(is_show=True, is_inside=True),
                splitline_opts=opts.SplitLineOpts(
                    is_show=True, linestyle_opts=opts.LineStyleOpts(color="#E2E2E2")
                ),  # 设置网格线；
            ),
            xaxis_opts=opts.AxisOpts(
                type_="category",
                boundary_gap=self.boundary_gap,
                axislabel_opts=opts.LabelOpts(color="#7D7D7D"),
                axisline_opts=opts.AxisLineOpts(
                    linestyle_opts=opts.LineStyleOpts(width=1.5, color="#A0A7B3")
                ),
                axistick_opts=opts.AxisTickOpts(is_show=True, is_inside=True),
                splitline_opts=opts.SplitLineOpts(
                    is_show=True, linestyle_opts=opts.LineStyleOpts(color="#E2E2E2")
                ),
            )
        )
        if len(self.args) > 0:
            for num in range(len(self.args[0])):
                c.add_yaxis(
                    series_name = self.args[0][num],
                    y_axis = self.args[1][num],
                    label_opts=opts.LabelOpts(is_show=self.is_show)
                )
        # for agr_data in self.args:
        #     c.add_yaxis(agr_data[0], agr_data[1])
        return c

# 饼图；
class Pie_Py:
    def __init__(self, title, x_value, y_name, y_value, *args, reversal_axis=True, pos_left="right", legend_icon='roundRect', subtitle='', is_show=False):
        self.reversal_axis = reversal_axis
        self.pos_left = pos_left
        self.legend_icon = legend_icon
        self.subtitle = subtitle
        self.is_show = is_show
        self.args = args
        self.title = title
        self.x_value = [str(i) for i in x_value]
        self.y_name = y_name
        self.y_value = [float(i) for i in y_value]
        self.inner_data_pair = [list(z) for z in zip(self.x_value, self.y_value)]  # 合并参数；
        if len(self.args) > 0: # 先判断是否需要画多图，再判断是2个还是3个；
            if len(self.args[0]) > 1:
                self.outer_data_pair = [list(z) for z in zip(self.args[0][0], self.args[2][0])]  # 合并参数；
                self.max_data_pair = [list(z) for z in zip(self.args[0][1], self.args[2][1])]  # 合并参数；
            else:
                self.outer_data_pair = [list(z) for z in zip(self.args[0][0], self.args[2][0])]  # 合并参数；

    def pie_render_genre(self):
        c = Pie()
        c.add(
            self.y_name,
            self.inner_data_pair,
            center=["35%", "50%"]
        )
        c.set_global_opts(
            title_opts=opts.TitleOpts(title=self.title),
            legend_opts=opts.LegendOpts(
                pos_left=self.pos_left,
                orient="vertical"
            )
        )
        c.set_series_opts(
            tooltip_opts=opts.TooltipOpts(
                trigger="item", formatter="{a} <br/>{b}: {c} ({d}%)"
            ),
            label_opts=opts.LabelOpts(formatter="{b}: {d}%")
        )
        return c

    def pie_render_air(self):
        """
            * 实心圆一个，仅支持一份参数；
        """
        # c = Pie(init_opts=opts.InitOpts(width="1600px", height="800px"))
        c = Pie()
        c.add(
            series_name=self.y_name,
            # radius=["40%", "55%"], # 半圆的尺寸；
            radius=[0, "55%"],
            data_pair=self.inner_data_pair,
            label_opts=opts.LabelOpts(
                position="outside",
                formatter="{a|{a}}{abg|}\n{hr|}\n {b|{b}: }{c}  {per|{d}%}  ",
                background_color="#eee",
                border_color="#aaa",
                border_width=1,
                border_radius=4,
                rich={
                    "a": {"color": "#999", "lineHeight": 22, "align": "center"},
                    "abg": {
                        "backgroundColor": "#e3e3e3",
                        "width": "100%",
                        "align": "right",
                        "height": 22,
                        "borderRadius": [4, 4, 0, 0],
                    },
                    "hr": {
                        "borderColor": "#aaa",
                        "width": "100%",
                        "borderWidth": 0.5,
                        "height": 0,
                    },
                    "b": {"fontSize": 16, "lineHeight": 33},
                    "per": {
                        "color": "#eee",
                        "backgroundColor": "#334455",
                        "padding": [2, 4],
                        "borderRadius": 2,
                    },
                },
            ),
        )
        c.set_global_opts(
            title_opts=opts.TitleOpts(title=self.title),
            legend_opts=opts.LegendOpts(
                pos_left=self.pos_left,
                orient="vertical"
            )
        )
        c.set_series_opts(
            tooltip_opts=opts.TooltipOpts(
                trigger="item", formatter="{a} <br/>{b}: {c} ({d}%)"
            )
        )
        return c

    def pie_render_pro(self):
        """
            * 空心圆包含实心圆的饼图；
            * 支持两份百分比值数据，使用*args传参三个，分别为x数据列、y轴名、y数据列；
        """
        # c = Pie(init_opts=opts.InitOpts(width="1600px", height="800px"))
        c = Pie()
        c.add(
            series_name=self.y_name,
            data_pair=self.inner_data_pair,
            radius=[0, "30%"],
            label_opts=opts.LabelOpts(position="inner"),
        )
        c.add(
            series_name=self.args[1][0],
            radius=["40%", "55%"],
            data_pair=self.outer_data_pair,
            label_opts=opts.LabelOpts(
                position="outside",
                formatter="{a|{a}}{abg|}\n{hr|}\n {b|{b}: }{c}  {per|{d}%}  ",
                background_color="#eee",
                border_color="#aaa",
                border_width=1,
                border_radius=4,
                rich={
                    "a": {"color": "#999", "lineHeight": 22, "align": "center"},
                    "abg": {
                        "backgroundColor": "#e3e3e3",
                        "width": "100%",
                        "align": "right",
                        "height": 22,
                        "borderRadius": [4, 4, 0, 0],
                    },
                    "hr": {
                        "borderColor": "#aaa",
                        "width": "100%",
                        "borderWidth": 0.5,
                        "height": 0,
                    },
                    "b": {"fontSize": 16, "lineHeight": 33},
                    "per": {
                        "color": "#eee",
                        "backgroundColor": "#334455",
                        "padding": [2, 4],
                        "borderRadius": 2,
                    },
                },
            ),
        )
        c.set_global_opts(legend_opts=opts.LegendOpts(pos_left="left", orient="vertical"))
        c.set_series_opts(
            tooltip_opts=opts.TooltipOpts(
                trigger="item", formatter="{a} <br/>{b}: {c} ({d}%)"
            )
        )
        return c

    def pie_render_plus(self):
        """
            * 空心圆包含实心圆的饼图(总计3个饼图一起)；
            * 支持两份百分比值数据，使用*args传参三个，分别为x数据列、y轴名、y数据列；
        """
        c = Pie()
        c.add(
            series_name=self.y_name,
            data_pair=self.inner_data_pair,
            radius=[0, "30%"],
            label_opts=opts.LabelOpts(position="inner"),
        )
        c.add(
            series_name=self.args[1][0],
            radius=["40%", "55%"],
            data_pair=self.outer_data_pair,
            label_opts=opts.LabelOpts(
                position="outside",
                formatter="{a|{a}}{abg|}\n{hr|}\n {b|{b}: }{c}  {per|{d}%}  ",
                background_color="#eee",
                border_color="#aaa",
                border_width=1,
                border_radius=4,
                rich={
                    "a": {"color": "#999", "lineHeight": 22, "align": "center"},
                    "abg": {
                        "backgroundColor": "#e3e3e3",
                        "width": "100%",
                        "align": "right",
                        "height": 22,
                        "borderRadius": [4, 4, 0, 0],
                    },
                    "hr": {
                        "borderColor": "#aaa",
                        "width": "100%",
                        "borderWidth": 0.5,
                        "height": 0,
                    },
                    "b": {"fontSize": 16, "lineHeight": 33},
                    "per": {
                        "color": "#eee",
                        "backgroundColor": "#334455",
                        "padding": [2, 4],
                        "borderRadius": 2,
                    },
                },
            ),
        )
        c.add(
            series_name=self.args[1][1],
            radius=["65%", "80%"],
            data_pair=self.max_data_pair,
            label_opts=opts.LabelOpts(
                position="outside",
                formatter="{a|{a}}{abg|}\n{hr|}\n {b|{b}: }{c}  {per|{d}%}  ",
                background_color="#eee",
                border_color="#aaa",
                border_width=1,
                border_radius=4,
                rich={
                    "a": {"color": "#999", "lineHeight": 22, "align": "center"},
                    "abg": {
                        "backgroundColor": "#e3e3e3",
                        "width": "100%",
                        "align": "right",
                        "height": 22,
                        "borderRadius": [4, 4, 0, 0],
                    },
                    "hr": {
                        "borderColor": "#aaa",
                        "width": "100%",
                        "borderWidth": 0.5,
                        "height": 0,
                    },
                    "b": {"fontSize": 16, "lineHeight": 33},
                    "per": {
                        "color": "#eee",
                        "backgroundColor": "#334455",
                        "padding": [2, 4],
                        "borderRadius": 2,
                    },
                },
            ),
        )
        c.set_global_opts(legend_opts=opts.LegendOpts(pos_left="left", orient="vertical"))
        c.set_series_opts(
            tooltip_opts=opts.TooltipOpts(
                trigger="item", formatter="{a} <br/>{b}: {c} ({d}%)"
            )
        )
        return c

class Scatter_Py:
    def __init__(self, title, x_value, y_name, y_value, *args, pos_left="center", legend_icon='roundRect', subtitle='', is_show=False):
        self.is_show = is_show
        self.pos_left = pos_left
        self.legend_icon = legend_icon
        self.subtitle = subtitle
        self.args = args
        self.title = title
        self.x_value = [str(i) for i in x_value]
        self.y_name = y_name
        self.y_value = [float(i) for i in y_value]
        self.inner_data_pair = [list(z) for z in zip(self.y_value, self.x_value)]  # 合并参数；
        if len(self.args) > 0:  # 先判断是否需要画多图，再判断是2个还是3个；
            if len(self.args[0]) > 1:
                self.outer_data_pair = [list(z) for z in zip(self.args[0][0], self.args[2][0])]  # 合并参数；
                self.max_data_pair = [list(z) for z in zip(self.args[0][1], self.args[2][1])]  # 合并参数；
            else:
                self.outer_data_pair = [list(z) for z in zip(self.args[0][0], self.args[2][0])]  # 合并参数；

    def scatter_render_air(self):
        c = Scatter()
        c.add_xaxis(self.x_value)
        c.add_yaxis(
            series_name=self.y_name,
            y_axis=self.inner_data_pair,
            label_opts=opts.LabelOpts(
                is_show=self.is_show,
                formatter=JsCode(
                    "function(params){return params.value[2] +' : '+ params.value[1];}"
                )
            )
        )
        c.set_global_opts(
            title_opts=opts.TitleOpts(title=self.title, subtitle=self.subtitle),
            # tooltip_opts=opts.TooltipOpts(
            #     formatter=JsCode(
            #         "function (params) {return params.name + ' : ' + params.value[2];}"
            #     )
            # ),
            visualmap_opts=opts.VisualMapOpts(
                type_="color", max_=150, min_=20, dimension=1
            ),
            legend_opts=opts.LegendOpts(
                pos_left=self.pos_left,
                legend_icon=self.legend_icon
            )
        )
        return c

# 人物/事件关系图；
class Graph_Py:
    def __init__(self, title, data_json={}, is_show=False, run_df_data=pd.DataFrame({}), pos_top='bottom'):
        self.title = title
        self.is_show = is_show
        self.data_json = data_json
        self.run_df_data = run_df_data
        self.pos_top = pos_top

    def json_format_graph(self, calc_num=100):
        # 格式化字符串；
        if len(self.run_df_data) > 0:
            graph_format_json = [[], [], []]
            self.run_df_data.columns = ['起点', '终点', '关系值']
            start_name_list = self.run_df_data['起点'].drop_duplicates().tolist()
            for start_name in start_name_list:
                name_df_data = self.run_df_data[self.run_df_data['起点'] == start_name]
                name_value = name_df_data.shape[0]
                run_value = int(name_value / calc_num)
                if run_value < 0:
                    run_value = 1
                graph_format_json[0].append({
                    "name": start_name,
                    "symbolSize": run_value,
                    "draggable": "False",
                    "value": name_value,
                    "category": start_name,
                    "label": {
                        "normal": {
                            "show": "True"
                        }
                    }
                })
                # 计算第二个词典；
                for start_name, end_name, calc_value in name_df_data.values:
                    graph_format_json[1].append({
                            'source': start_name,
                            'target': end_name
                        }
                    )
            # 加入最后的；
            graph_format_json[2] = json.loads(pd.DataFrame(start_name_list).reset_index(drop=True).rename(columns={0: 'name'}).to_json(orient='records'))

            return graph_format_json
        else:
            print('当前引入df文件异常，请重试')
            exit()

    def render_ball_air(self, calc_num=100):
        if len(self.data_json) > 0:
            nodes, links, categories = self.data_json
        else:
            data_json = self.json_format_graph(calc_num=calc_num)
            nodes, links, categories = data_json
        # 开始绘图；
        c = (
            Graph()
                .add(
                    "",
                    nodes,
                    links,
                    categories,
                    repulsion=50,
                    linestyle_opts=opts.LineStyleOpts(curve=0.2),
                    label_opts=opts.LabelOpts(is_show=self.is_show),
                )
                .set_global_opts(
                    legend_opts=opts.LegendOpts(is_show=self.is_show, pos_top=self.pos_top),
                    title_opts=opts.TitleOpts(title=self.title)
            )
        )
        return c

# 时间线动态图表；
class TimeLine_Py:
    def __init__(self, data_list, render_type='Bar_Py', play_interval=1000, control_position='right'):
        self.data_list = data_list
        self.play_interval = play_interval
        self.reder_type = render_type
        self.control_position = control_position

    def render_time_air(self, reversal_axis=True, pos_top='top'):
        time_line = Timeline()  # 创建 Timeline对象

        # 开始准备画图；
        for run_data in self.data_list:
            title_text = str(run_data[0]) + '_数据展示'
            run_date = run_data[0]
            x_value = [str(i) for i in run_data[1]]
            y_title = run_data[2]
            y_value = [float(i) for i in run_data[3]]
            if self.reder_type.lower() == 'Bar_Py'.lower():
                c = Bar_Py(title_text, x_value, y_title, y_value, reversal_axis=reversal_axis, pos_top=pos_top).bar_render_general()
            else:
                c = Line_Py(title_text, x_value, y_title, y_value, pos_top=pos_top).line_render_air()

            time_line.add(c, run_date)
        # 画好的图加入时间线；
        time_line.add_schema(
            symbol='arrow',  # 设置标记时间；
            # orient = 'vertical',
            is_auto_play=True,
            symbol_size=2,  # 标记大小;
            play_interval=self.play_interval,  # 播放时间间隔；
            control_position=self.control_position,  # 控制位置;
            # linestyle_opts=opts.LineStyleOpts(
            #     width=5,
            #     type_='dashed',
            #     color='rgb(255,0,0,0.5)'
            # ),
            # label_opts=opts.LabelOpts(
            #     color='rgb(0,0,255,0.5)',
            #     font_size=15,
            #     font_style='italic',
            #     font_weight='bold',
            #     font_family='Time New Roman',
            #     position='left',
            #     interval=20
            # )
        )
        return time_line


# 词云图；
class WordCloud_Py:
    def __init__(self, title, *args, is_show=False, pos_top='bottom'):
        self.title = title
        self.is_show = is_show
        self.pos_top = pos_top
        self.args = args

    def render_to_png(self, c):
        make_snapshot(snapshot, c.render(), "./%s.png" %(self.title))

    def jieba_cut(self, length_num=0):
        if type(self.args[0]) == list:
            word_data = ''.join(self.args[0])
        else:
            word_data = re.sub('\W*', '', self.args[0])
        word_list = jieba.cut(word_data)
        self.word_cut_result = ','.join(word_list).split(',')
        counter = Counter(self.word_cut_result)
        if length_num > 0:
            for key_info in list(counter.keys()):
                if len(key_info) <= length_num:
                    counter.pop(key_info)
        self.word_dictionary = dict(counter)
        self.word_tuple_result = counter.most_common()
        return self.word_cut_result, self.word_dictionary, self.word_tuple_result

    def wordcloud_render(self, length_num=0):
        self.jieba_cut(length_num)
        c = WordCloud()
        c.add('', self.word_tuple_result, shape=SymbolType.DIAMOND)
        c.set_global_opts(
            title_opts=opts.TitleOpts(title=self.title),
            legend_opts=opts.LegendOpts(is_show=self.is_show)
        )
        return c