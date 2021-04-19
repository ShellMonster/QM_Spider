import pandas as pd
from qm_spider import *
from pyecharts.faker import Faker
from pyecharts import options as opts
from pyecharts.charts import Bar, Grid, Line, Page, Pie, Timeline, Boxplot, WordCloud, Graph
from pyecharts.commons.utils import JsCode
from pyecharts.globals import ThemeType, SymbolType
from pyecharts.render import make_snapshot
from snapshot_selenium import snapshot
from collections import Counter


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
        self.x_value = [str(i) for i in x_value]
        self.y_name = y_name
        self.y_value = [float(i) for i in y_value]

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
        )
        if len(self.args) > 0:
            for num in range(len(self.args[0])):
                print(2)
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
    def __init__(self, title, x_value, y_name, y_value, reversal_axis=True):
        Pyecharts_Var.__init__(self, title, x_value, y_name, y_value)
        self.reversal_axis = reversal_axis

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
            legend_opts=opts.LegendOpts(pos_left="center", pos_top='bottom', legend_icon='circle'),
        )
        for agr_data in self.args:
            c.add_yaxis(agr_data[0], agr_data[1])
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
            )
        )
        for agr_data in self.args:
            c.add_yaxis(agr_data[0], agr_data[1])
        return c

# 人物/事件关系图；
class Graph_Py:
    def __init__(self, title, data_json={}, is_show=False, run_df_data=pd.DataFrame({})):
        self.title = title
        self.is_show = is_show
        self.data_json = data_json
        self.run_df_data = run_df_data

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
            data_json = self.json_format_graph(calc_num=100)
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
                legend_opts=opts.LegendOpts(is_show=self.is_show),
                title_opts=opts.TitleOpts(title=self.title),
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

    def render_time_air(self, reversal_axis=True):
        time_line = Timeline()  # 创建 Timeline对象

        # 开始准备画图；
        for run_data in self.data_list:
            title_text = run_data[0] + '_数据展示'
            run_date = run_data[0]
            x_value = [str(i) for i in run_data[1]]
            y_title = run_data[2]
            y_value = [float(i) for i in run_data[3]]
            if self.reder_type.lower() == 'Bar_Py'.lower():
                c = Bar_Py(title_text, x_value, y_title, y_value, reversal_axis=reversal_axis).bar_render_general()
            else:
                c = Line_Py(title_text, x_value, y_title, y_value).line_render_air()

            time_line.add(c, run_date)
        # 画好的图加入时间线；
        time_line.add_schema(
            symbol='arrow',  # 设置标记时间；
            # orient = 'vertical',
            is_auto_play=True,
            symbol_size=2,  # 标记大小;
            play_interval=self.play_interval,  # 播放时间间隔；
            control_position=self.control_position,  # 控制位置;
            linestyle_opts=opts.LineStyleOpts(
                width=5,
                type_='dashed',
                color='rgb(255,0,0,0.5)'
            ),
            label_opts=opts.LabelOpts(
                color='rgb(0,0,255,0.5)',
                font_size=15,
                font_style='italic',
                font_weight='bold',
                font_family='Time New Roman',
                position='left',
                interval=20
            )
        )
        return time_line


# 词云图；
class WordCloud_Py:
    def __init__(self, title, *args):
        self.title = title
        self.args = args

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
        c.set_global_opts(title_opts=opts.TitleOpts(title=self.title))
        return c