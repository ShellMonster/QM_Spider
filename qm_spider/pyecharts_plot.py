from qm_spider import *
from pyecharts.faker import Faker
from pyecharts import options as opts
from pyecharts.charts import Bar, Grid, Line, Page, Pie, Timeline, Boxplot
from pyecharts.commons.utils import JsCode
from pyecharts.globals import ThemeType
from pyecharts.render import make_snapshot
from snapshot_selenium import snapshot


# 画图基础通用参数；
class Pyecharts_Var:
    def __init__(self, title, x_value, y_name, y_value, *args, subtitle='', is_symbol_show=False, line_width=2, is_show=False, color_list=['#00b088', '#f76b61', '#ffb55d', '#8470ff', '#00a2ff', '#ffe400', '#11d2c2', '#c263f9']):
        self.subtitle = subtitle
        self.is_symbol_show = is_symbol_show
        self.line_width = line_width
        self.is_show = is_show
        self.color_list = color_list
        self.args = args
        self.title = title
        self.x_value = x_value
        self.y_name = y_name
        self.y_value = y_value

    def render_to_png(self, c):
        make_snapshot(snapshot, c.render(), "./%s.png" %(self.title))

# 折线图、面积图；
class Line_Py(Pyecharts_Var):
    def __init__(self, title, x_value, y_name, y_value, *args):
        Pyecharts_Var.__init__(self, title, x_value, y_name, y_value, *args)

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
        )
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
            legend_opts=opts.LegendOpts(pos_left="center", pos_top='bottom', legend_icon='circle'),
            yaxis_opts=opts.AxisOpts(
                type_="value",
                max_='dataMax',
                boundary_gap=True,  # 封闭坐标轴，左右都有顶上的刻度线；
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
                boundary_gap=True,
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
class Bar_Py(Pyecharts_Var):
    def __init__(self, title, x_value, y_name, y_value):
        Pyecharts_Var.__init__(self, title, x_value, y_name, y_value)

    def bar_render_air(self):
        c = Bar()
        c.add_xaxis(self.x_value)
        c.add_yaxis(self.y_name, self.y_value)
        c.set_global_opts(
            title_opts=opts.TitleOpts(title=self.title, subtitle=self.subtitle),
        )
        for agr_data in self.args:
            c.add_yaxis(agr_data[0], agr_data[1])
        self.c_render = c
        return c