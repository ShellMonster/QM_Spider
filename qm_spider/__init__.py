import requests, datetime, time, warnings, json, calendar, math, os, re, jieba, jieba.analyse, random, string
from datetime import date
from dateutil.relativedelta import relativedelta
from pandas.io.json import json_normalize
from urllib.parse import quote
import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
from scipy.stats import norm, mstats
from urllib.parse import quote
from urllib.parse import unquote
warnings.filterwarnings("ignore")
from requests.adapters import HTTPAdapter

# 基本参数；
push_token = 'https://oapi.dingtalk.com/robot/send?access_token=f3a590b8c5f4c4777fe0f217067f15132091bff53e2a2143a5daa981d795159d'

'''
=====目录区=====
1. 计算七麦外的其他备用工具；
2. 计算七麦内的备用工具；
3. 常用的自定义参数；
4. 获取基础信息相关数据；
5. 获取产品榜单相关数据；
6. 获取产品开发商相关数据；
7. 获取产品关键词的相关数据；
8. 获取产品的关键词相关数据；
9. 获取产品评论的相关接口；
10. 获取清榜列表相关数据；
11. 获取清词列表相关数据；
12. 获取下架产品列表相关数据；
13. 获取预订App列表；
14. 获取产品被精品推荐及上热搜情况列表；
15. 获取App不同状态列表；
16. 封装指数排行榜接口；
17. 封装关键词落词列表接口；
18. 获取免费、付费、畅销榜单产品列表；
19. 获取产品预估下载量数据；
20. iOS 13、iOS 12热搜数据；
21. 榜单上升下降较快产品；
22. 各类关键词覆盖榜单；

'''

# 保持会话；
session = requests.session()
session.mount('http://', HTTPAdapter(max_retries=3))
session.mount('https://', HTTPAdapter(max_retries=3))
today_date = datetime.date.today()
one_day = datetime.timedelta(days=1)

# 请求头；
headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 11_2_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.182 Safari/537.36 Edg/88.0.705.81"
}

# 登录检查；
def qm_auth_check(func):
    def wrapper(*args, **kwargs):
        for cookie_info in list(session.cookies):
            if 'qimai.cn' in str(cookie_info):
                return func(*args, **kwargs)
        else:
            print('尚未使用"Sing_Qimai"类登录七麦数据')
            exit()
    # 当函数被装饰的时候, 返回装饰器内闭包函数的引用
    return wrapper

# 运行时间统计；
def run_time_calc(func):
    def wrapper(*args, **kwargs):
        begin_time = time.time()
        retc = func(*args, **kwargs)
        end_time = time.time()
        Run_time = end_time - begin_time
        print("【%s】函数运行时间为：%s秒" %(func.__name__, str(round(Run_time, 2))))
        return retc
    # 当函数被装饰的时候, 返回装饰器内闭包函数的引用
    return wrapper

# # 运行进度条；
# def progress_bar(func):
#     def wrapper(*args, **kwargs):
#         # 使用进度条运行；
#         for num in tqdm(range(len(keyword_list))):
#             keyword = keyword_list[num]
#         return func(*args, **kwargs)
#     return wrapper

# 钉钉推送；
class DingDing_Push:
    """
        * 钉钉推送区；
        * 可以自己修改推送token及标题等；
        * 同时附带万能推送脚本，使用*args自定义；
    """
    def __init__(self, push_title, *args, push_status='执行成功', now_time=str(datetime.datetime.now())[:19], push_url=push_token):
        self.push_title = push_title
        self.push_status = push_status
        self.now_time = now_time
        self.push_url = push_url
        self.other_var = args
        self.headers = {
            "Content-Type": "application/json",
            "Charset": "UTF-8"
        }

    def status_push(self):
        """
            * 状态告知推送：
            一般用于报错或执行成功推送，\n
            默认状态为成功，若修改指定即可；
        """
        payload = {
            "msgtype": "markdown",
            "markdown": {
                "title": "【%s】%s" %(self.now_time[:10], self.push_title),
                "text": "**推送事件**：%s\n\n**推送时间**：%s\n\n**推送状态**：%s" %(self.push_title, self.now_time, self.push_status)
            }
        }
        payload = json.dumps(payload)
        res = requests.post(self.push_url, data=payload, headers=self.headers)
        return res.json()

    def app_args_markdown_push(self):
        """
            * 万能推送-markdown：
            推送内容自己写为Markdown形式即可；
        """
        payload = {
            "msgtype": "markdown",
            "markdown": {
                "title": "%s" %(self.push_title),
                "text": "%s" %(self.other_var[0])
            }
        }
        payload = json.dumps(payload)
        res = requests.post(self.push_url, data=payload, headers=self.headers)
        return res.json()

    def app_args_text_push(self):
        payload = {
            "msgtype": "text",
            "text": {
                "content": "%s" %(self.other_var[0])
            }
        }
        payload = json.dumps(payload)
        res = requests.post(self.push_url, data=payload, headers=self.headers)
        return res.json()

# 自动登录；
class Sing_Qimai:
    """
        * 自动登录区；
        * 目前仅支持七麦数据自动登录；
    """
    def __init__(self, user_id, user_pwd):
        self.user_id = user_id
        self.user_pwd = user_pwd

    def login_qm(self):
        """
            * 自动登录七麦数据：
            账号密码需要在类中指定；
        """
        url = 'https://api.qimai.cn/account/signinForm'
        payload = "username=%s&password=%s" %(self.user_id, self.user_pwd)
        headers = {
            'Content-Type': "application/x-www-form-urlencoded",
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.87 Safari/537.36"
        }
        res = session.post(url, headers=headers, data=payload)

# 计算七麦外的其他备用工具；
class Qimai_Outside_Tool:
    """
        * 七麦接口外部的自定义工具区；
        * 举例①：自动匹配是否包含中文；
        * 举例②：自动匹配开发者账号是公司还是个人；
    """
    def __init__(self, *args):
        self.data_info = args

    def match_str_chinese(self):
        """
            * 匹配字符串内是否为纯中文；
        """
        for ch in self.data_info[0]:
            if u'\u4e00' <= ch <= u'\u9fff':
                return True
        return False

    def match_publisher_company(self):
        """
            * 匹配开发者是否为公司账号(自带匹配库)；
        """
        company_str_list = ['公司', 'Technology', 'Beijing', '(', ')', '（', '）', 'Ltd', '.', 'Inc', 'china', '互联网', '科技', '网络', '计算机', 'LLC', '-', 'Company', 'games', '工作室', 'Tech', '信息', 'online', 'Network', '互动', '移动', '游戏', '技术', 'LIMITED', '株式会社', 'Tov', 'USA', 'UK', '银行', '组织', '机构']
        for company_str in company_str_list:
            if company_str.lower() in self.data_info[0].lower() or len(self.data_info[0])>20:
                return True
        return False

    def match_fillna_value(self):
        """
            * 针对列表中的异常值使用平均值补充，方便在不改变字符位置情况下计算最大最小值及位置；
        """
        df_list = pd.DataFrame(self.data_info[0])
        df_list.fillna(np.mean(df_list[0]), inplace=True)
        return df_list[0].tolist()

    def get_week_day(self):
        """
            * 获取今日星期几：
        """
        week_day = {
            '0': '星期一',
            '1': '星期二',
            '2': '星期三',
            '3': '星期四',
            '4': '星期五',
            '5': '星期六',
            '6': '星期日'
        }
        if len(str(self.data_info[0])) == 1:
            return week_day[str(self.data_info[0])]
        elif len(str(self.data_info[0])) == 10:
            day = datetime.datetime.fromisoformat(str(self.data_info[0])).weekday()  # weekday()可以获得是星期几
            return week_day[day]
        elif len(str(self.data_info[0])) == 19:
            day = datetime.datetime.strptime(str(self.data_info[0])[:19], '%Y-%m-%d %H:%M:%S').weekday()  # weekday()可以获得是星期几
            return week_day[day]
        else:
            day = self.data_info[0].weekday()  # weekday()可以获得是星期几
            return week_day[day]

    def get_index_list_num(self):
        """
            * 定位列表内字符串位置：
            * 返回列表；
        """
        run_list_num = []
        if '' in self.data_info[0]:
            for x, i in enumerate(self.data_info[0]):
                if i == '':  # 判断字符串
                    run_list_num.append(x - 1)
            # 把最后一列加入，排版完毕后删除空值；
            run_list_num.append(len(self.data_info[0]) - 1)
            for x, i in enumerate(run_list_num):
                run_list_num[x] = i - x
        else:
            run_list_num.append(len(self.data_info[0]) - 1)
        return run_list_num

    def json_to_df(self):
        """
            * json转为pandas的表格形式；
            返回dataframe格式；
        """
        self.json_df = json_normalize(self.data_info[0])
        return self.json_df

    def list_to_df(self):
        """
            * 列表转为pandas的表格形式；
            返回dataframe格式；
        """
        self.list_df = pd.DataFrame(self.data_info[0])
        return self.list_df

    def unix_time(self):
        """
            * 世界时间转换北京时间；
        """
        # 世界标准时间
        date_now = datetime.datetime.strptime(self.data_info[0], '%Y-%m-%d %H:%M:%S')
        # 北京时间UTC+8
        cst_time = date_now.astimezone(datetime.timezone(datetime.timedelta(hours=-8))).strftime("%Y-%m-%d %H:%M:%S")
        return cst_time

    def timeStr_to_datetime(self):
        """
            * 字符串格式时间，支持纯日期或携带时分秒的格式；
        """
        if len(str(self.data_info[0])) == 10:
            datetime_str = str(self.data_info[0]) + ' 00:00:00'
            date_time = datetime.datetime.strptime(datetime_str, '%Y-%m-%d %H:%M:%S')
        elif len(str(self.data_info[0])) >= 19:
            date_time = datetime.datetime.strptime(str(self.data_info[0])[:19], '%Y-%m-%d %H:%M:%S')
        else:
            print('请给出日期长度的数据，或给出带时分秒的数据')
            date_time = self.data_info[0]
            exit()
        return date_time

    def time_to_date(self):
        """
            * 时间戳转换年月日时分秒；
        """
        if len(str(self.data_info[0])) == 13:
            self.run_time = int(self.data_info[0]/1000)
        else:
            self.run_time = self.data_info[0]
        timeArray = time.localtime(self.run_time)
        otherStyleTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
        return otherStyleTime

    def date_to_time(self):
        """
            * 日期转换时间戳；
        """
        if len(str(self.data_info[0])) == 10:
            self.run_date = self.data_info[0] + ' 00:00:00'
        timeArray = time.strptime(self.run_date, "%Y-%m-%d %H:%M:%S")
        timeStamp = int(time.mktime(timeArray))
        return timeStamp

    def get_month_time(self):
        """
            * 根据时间获取月头月尾的日期；
        """
        day_start = datetime.date.fromisoformat(str(self.data_info[0]))
        day_end = datetime.date.fromisoformat(str(self.data_info[1]))
        # monthRange_start = calendar.monthrange(day_start.year, day_start.month)
        monthRange_end = calendar.monthrange(day_end.year, day_end.month)
        start_time = str(day_start)[:8] + str('01')
        end_time = str(day_end)[:8] + str(monthRange_end[1])
        return start_time, end_time

    def calc_interval_time(self):
        """
            * 计算间隔时间；
            返回间隔的小时分钟秒；
        """
        spider_time_datetime = datetime.datetime.strptime(str(self.data_info[0]), '%Y-%m-%d %H:%M:%S')
        rank_out_datetime = datetime.datetime.strptime(str(self.data_info[1]), '%Y-%m-%d %H:%M:%S')
        interval_seconds = (rank_out_datetime - spider_time_datetime).total_seconds()
        m, s = divmod(interval_seconds, 60)
        h, m = divmod(m, 60)
        d, h = divmod(h, 24)
        if d > 0:
            interval_time = "%02d天%02d小时%02d分钟%02d秒" % (d, h, m, s)  # 计算间隔时间；
        else:
            interval_time = "%02d小时%02d分钟%02d秒" % (h, m, s)  # 计算间隔时间；
        return interval_time

    def second_conversion_time(self):
        """
            * 秒转换为天、时、分、秒；
        """
        m, s = divmod(self.data_info[0], 60)
        h, m = divmod(m, 60)
        d, h = divmod(h, 24)
        if d > 0:
            interval_time = "%02d天%02d小时%02d分钟%02d秒" % (d, h, m, s)  # 计算间隔时间；
        else:
            interval_time = "%02d小时%02d分钟%02d秒" % (h, m, s)  # 计算间隔时间；
        return interval_time

    def calc_overlap_days(self, s1, e1, s2, e2):
        """
            * 计算两段日期之间重复比例；
            返回间隔天数，各自重复比例；
        """
        latest_start = max(s1, s2)
        earliest_end = min(e1, e2)
        self.overlap = (earliest_end - latest_start).days + 1
        if self.overlap < 0:
            self.overlap = 0
        s1_days = (e1 - s1).days + 1
        s2_days = (e2 - s2).days + 1
        self.s1_scale = self.overlap / s1_days
        self.s2_scale = self.overlap / s2_days
        return self.overlap, self.s1_scale, self.s2_scale

    def trend_analysis(self):
        self.alpha = 0.05
        n = len(self.data_info[0])
        s = 0
        for k in range(n - 1):
            for j in range(k + 1, n):
                s += np.sign(self.data_info[0][j] - self.data_info[0][k])
        unique_x, tp = np.unique(self.data_info[0], return_counts=True)
        g = len(unique_x)
        if n == g:
            var_s = (n * (n - 1) * (2 * n + 5)) / 18
        else:  # there are some ties in data
            var_s = (n * (n - 1) * (2 * n + 5) - np.sum(tp * (tp - 1) * (2 * tp + 5))) / 18
        if s > 0:
            z = (s - 1) / np.sqrt(var_s)
        elif s < 0:
            z = (s + 1) / np.sqrt(var_s)
        else:  # s == 0:
            z = 0
        p = 2 * (1 - norm.cdf(abs(z)))  # two tail test
        h = abs(z) > norm.ppf(1 - self.alpha / 2)
        if (z < 0) and h:
            self.trend = '下降', p, g, z
        elif (z > 0) and h:
            self.trend = '上升', p, g, z
        else:
            self.trend = '无趋势', p, g, z
        return self.trend

    def main_kendall_Trend(self, column_name):
        """
            * 时间段内数据上升下降平稳趋势自动分析；
            * 返回不重复的多段时间及对应参数；
        """
        # 读取数据；
        run_value_dataframe = pd.DataFrame({})  # 使用dataframe存储数据；
        # df['日期'] = pd.to_datetime(df['日期'])
        df = self.data_info[0]
        df['日期'] = [datetime.date.fromisoformat(str(i)[:10]) for i in df['日期'].values]
        end_time = max(df['日期'].values)
        for i in range(30, 91):
            start_time = min(df['日期'].values)
            run_days = datetime.timedelta(days=i)
            while start_time <= end_time and (end_time - start_time) > run_days:
                run_time = start_time + run_days
                run_df = df[(df['日期'] >= start_time) & (df['日期'] <= run_time)][column_name]
                list_c = [int(i) for i in run_df.values]
                thrend_str = Qimai_Outside_Tool(list_c).trend_analysis()
                # if thrend_str[0] == '上升':
                # print('===========打印【%s】天的运行数据===========' %(run_days.days))
                run_value_dataframe = run_value_dataframe.append(pd.DataFrame({
                    'start_time': [start_time],
                    'end_time': [run_time],
                    'run_days': [run_days],
                    'thrend_str': [thrend_str[0]],
                    'p_value': [thrend_str[1]],
                    'g_value': [thrend_str[2]],
                    'z_value': [thrend_str[3]]
                }))

                # 时间往前加；
                start_time += run_days

        ##################【方案一 - 根据涨幅挑选2-3个区间】##################
        # 先排序，再根据排序后的值筛选出几个，需要避免重叠；
        trend_value_list = ['上升', '下降', '无趋势']
        df_dataframe_all = pd.DataFrame({})
        for trend_value in trend_value_list:
            run_value_now = run_value_dataframe[run_value_dataframe['thrend_str']==trend_value].sort_values('z_value', ascending=False)
            run_value_list = [list(i) for i in run_value_now.values]
            run_i = 0  # 便于重复检测；
            for i in run_value_list:
                if run_i + 1 < len(run_value_list):
                    run_x = 0
                    while True:
                        if run_x + 1 <= len(run_value_list):
                            # overlap, s1_scale, s2_scale = calc_overlap_days(i[0],i[1],x[0],x[1])
                            overlap, s1_scale, s2_scale = Qimai_Outside_Tool().calc_overlap_days(run_value_list[run_i][0], run_value_list[run_i][1], run_value_list[run_x][0], run_value_list[run_x][1])
                            if overlap > 0:
                                if run_value_list[run_i][6] > run_value_list[run_x][6]:  # 说明有重叠，保留前面的；
                                    run_value_list.remove(run_value_list[run_x])
                                    run_x -= 1
                                elif run_value_list[run_i][6] < run_value_list[run_x][6]:
                                    run_value_list.remove(run_value_list[run_i])
                                    run_i -= 1
                                    break
                                else:
                                    if run_value_list[run_i][2] < run_value_list[run_x][2]:
                                        run_value_list.remove(run_value_list[run_x])
                                        run_x -= 1
                                    elif run_value_list[run_i][2] > run_value_list[run_x][2]:
                                        run_value_list.remove(run_value_list[run_x])
                                        run_i -= 1
                                        break
                            run_x += 1
                        else:
                            # print('跳出', print('即将跳出', run_x, len(run_value_list)))
                            break
                    run_i += 1
                else:
                    break

            df_dataframe = pd.DataFrame(run_value_list)
            df_dataframe_all = pd.concat([df_dataframe_all, df_dataframe])
        df_dataframe_all.columns = ['开始时间', '结束时间', '持续天数', '趋势', 'p值', 'g值', 'z值']
        # return df_dataframe[['开始时间', '结束时间', '持续天数', 'z值']]
        return df_dataframe_all

# 计算七麦内的备用工具；
@qm_auth_check  # 登录检查；
class Qimai_Intside_Tool:
    """
        * 七麦接口内的一些通用处理规则；
        * 举例①：匹配产品对应的榜单是免费还是付费；
        * 举例②：匹配当前最新榜单榜位数值；
    """
    def __init__(self, data_info):
        self.data_info = data_info

    def rank_ios10_type(self):
        """
            * 根据价格判断iOS 10的榜单类型；
            返回“总榜(免费)”、“总榜(付费)”
        """
        if self.data_info == '0.00' or self.data_info == '免费':
            return '总榜(免费)'
        else:
            return '总榜(付费)'

    def old_rank_num(self, rank_name='总榜(免费)'):
        """
            * 根据iOS 10榜单类型获取时间段内第一次的榜单排名；
        """
        for app_rank in self.data_info['data']['list']:
            if app_rank['name'] == rank_name:
                return app_rank['data'][0][0]
        else:
            return 0

    def new_rank_num(self, rank_name='总榜(免费)'):
        """
            * 根据iOS 10榜单类型获取时间段内当前的榜单排名；
        """
        for app_rank in self.data_info['data']['list']:
            if app_rank['name'] == rank_name:
                return app_rank['data'][-1][0]
        else:
            return 0

    def get_match_keywordHints(self, columns_name='关键词'):
        """
            * 根据当前关键词表格(df)，自动匹配关键词当前指数；
            * 返回列表，自动使用到新列即可；
        """
        keyword_hints_list = []
        keyword_list = []
        for num, keyword in enumerate(self.data_info[0][columns_name].tolist()):
            print('正在获取第【%s】个关键词【%s】的热度，剩余【%s】行' %(num+1, keyword, self.data_info[0].shape[0]-(num+1)))
            if keyword not in keyword_list:
                keyword_hints = Get_Keyword_Info(keyword).get_keyword_hints()
                keyword_hints_list.append(keyword_hints)
                keyword_list.append(keyword)
            else:
                keyword_index = keyword_list.index(keyword)
                keyword_hints = keyword_hints_list[keyword_index]
                keyword_hints_list.append(keyword_hints)
                keyword_list.append(keyword)

        return keyword_hints_list

    def lost_keyword_calc(self, appid, start_date, end_date):
        """
            * 计算时间段内产品在某个词下掉词天数；
            从有排名那天开始算，第二天掉了算1天；
        """
        keyword_history_data = Get_App_Keyword(appid).get_keywordHistory_rank(self.data_info, start_date, end_date)
        lost_keyword_days = 0  # 掉词天数；
        if keyword_history_data['msg'] == '成功':
            for i in keyword_history_data['data']['list']:
                if i['name'] == '排名':
                    len_list_rank = []
                    for x in range(len(i['data'])):
                        if x != (len(i['data']) - 1):  # 最后一个是获取数据的时间，不要；
                            len_list_rank.append(str(i['data'][x][1]))
                    # 开始实际计算；
                    while len(len_list_rank) > 0:
                        if len_list_rank[0] == 'None':
                            del len_list_rank[0]
                        else:
                            # 排除了前面全无排名的情况；
                            for x in range(len(len_list_rank)):
                                # 开始判断排名；
                                if len_list_rank[x] == 'None':
                                    lost_keyword_days += 1
                            break  # 运行完跳出死循环；

        # 返回数据；
        # print('当前第【%s】个词【%s】在%s至%s落榜【%s】天' % (num, keyword, start_date, end_date, luo_keyword_time))
        return lost_keyword_days

#=============核心运行类区=============#
# 获取基础信息相关数据；
@qm_auth_check  # 登录检查；
class Get_App_Appinfo():
    def __init__(self, appid, country='cn'):
        self.appid = appid
        self.country = country

    def get_appinfo(self):
        """
            * 获取App的基本信息(无关联推荐版本信息)；
        """
        url = 'https://api.qimai.cn/app/appinfo?appid=%s&country=%s' %(self.appid, self.country)
        res = session.get(url, headers=headers)
        self.appinfo = res.json()
        return self.appinfo

    def get_subname(self):
        """
            * 获取App的名称(不含标题)；
        """
        self.get_appinfo()
        self.subname = self.appinfo['appInfo']['subname']
        return self.subname

    def get_publisher_name(self):
        """
            * 获取App归属的开发商名称(中文)
        """
        self.get_appinfo()
        self.publisher_name = self.appinfo['appInfo']['publisher']
        return self.publisher_name

    def get_developer_name(self):
        """
            * 获取App归属的开发商名称(英文)
        """
        self.get_appinfo()
        self.developer_name = self.appinfo['appInfo']['publisher_seller']
        return self.developer_name

    def get_purchases_num(self):
        self.get_appinfo()
        self.purchases_num = self.appinfo['appInfo']['purchases_num']
        return self.purchases_num

    def get_baseinfo(self):
        """
            * 获取App基础信息(包含开发商名称内购价格、关联推荐产品)
        """
        url = 'https://api.qimai.cn/app/baseinfo?country=%s&appid=%s' %(self.country, self.appid)
        res = session.get(url, headers=headers)
        self.app_baseinfo_data = res.json()
        return self.app_baseinfo_data

    def get_version(self, start_date='', end_date=''):
        """
            * 获取App的版本信息：
            * 可设定时间段，默认全部；
        """
        url = 'https://api.qimai.cn/app/version?country=%s&appid=%s&sdate=%s&edate=%s' %(self.country, self.appid, start_date, end_date)
        res = session.get(url, headers=headers)
        self.app_version_data = res.json()
        return self.app_version_data

    def get_version_info(self, start_date='', end_date=''):
        """
            * 获取App的版本信息：
            * 可设定时间段，默认全部；
            * 返回版本的版本号，版本时间等参数
        """
        self.get_version(start_date, end_date)
        if len(self.app_version_data['version']) >= 2:
            now_version_num = self.app_version_data['version'][0]['version']  # 当前版本号
            now_version_time = self.app_version_data['version'][0]['release_time']  # 当前版本号时间
            now_title = self.app_version_data['version'][0]['app_name']  # 当前版本App名称
            now_subtitle = self.app_version_data['version'][0]['subtitle']  # 当前版本副标题
            pre_version_num = self.app_version_data['version'][1]['version']
            pre_version_time = self.app_version_data['version'][1]['release_time']
            pre_title = self.app_version_data['version'][1]['app_name']
            pre_subtitle = self.app_version_data['version'][1]['subtitle']

            return [now_version_num, now_version_time, now_title, now_subtitle, pre_version_num, pre_version_time, pre_title, pre_subtitle]
        else:  # 不大于等于2则小于2，没有多的版本；
            now_version_num = self.app_version_data['version'][0]['version']  # 当前版本号
            now_version_time = self.app_version_data['version'][0]['release_time']  # 当前版本号时间
            now_title = self.app_version_data['version'][0]['app_name']  # 当前版本App名称
            now_subtitle = self.app_version_data['version'][0]['subtitle']  # 当前版本副标题
            pre_version_num = ''
            pre_version_time = ''
            pre_title = ''
            pre_subtitle = ''

            return [now_version_num, now_version_time, now_title, now_subtitle, pre_version_num, pre_version_time, pre_title, pre_subtitle]

    def get_baseinfo_parameter(self, user_type_name='支持网站'):
        """
            * 获取baseinfo接口下详细参数值，自行指定获取哪个：
            :param user_type_name: 需要获取的参数名，默认“支持网站”；
        """
        self.get_baseinfo()
        for base_info in self.app_baseinfo_data['appInfo']:
            type_name = base_info['name']
            if type_name == user_type_name:
                app_url = base_info['value']
                return app_url
        else:
            return '未找到'

# 获取榜单相关数据；
@qm_auth_check  # 登录检查；
class Get_App_Rank():
    """
        * 根据AppID及对应时间，获取产品榜单数值；
        * 可获取子分类榜单；
        day: 计量时间类型：默认按天，其他可选按分钟、小时\n
        rankType: 获取排名类型：默认每日排名，其他可选最高排名、全部排名\n
        brand: 价格类型：默认全部，其他可选例如免费、付费、畅销
    """
    def __init__(self, appid, start_date=today_date-datetime.timedelta(days=6), end_date=today_date, day=1, rankType='day', brand='all', appRankShow=1, subclass='all', simple=1, rankEchartType=1, country='cn', device='iphone'):
        self.appid = appid
        self.start_date = start_date
        self.end_date = end_date
        self.day = day
        self.rankType = rankType
        self.appRankShow = appRankShow
        self.subclass = subclass
        self.simple = simple
        self.rankEchartType = rankEchartType
        self.brand = brand
        self.country = country
        self.device = device

    def get_rank_data(self):
        """
            * 获取App的榜单数据：
        """
        url = 'https://api.qimai.cn/app/rankMore?appid=%s&country=%s&brand=%s&day=%s&appRankShow=%s&subclass=%s&simple=%s&sdate=%s&edate=%s&rankEchartType=%s&rankType=%s&device=%s' %(self.appid, self.country, self.brand, self.day, self.appRankShow, self.subclass, self.simple, self.start_date, self.end_date, self.rankEchartType, self.rankType, self.device)
        res = session.get(url, headers=headers)
        self.rank_data = res.json()
        return self.rank_data

    def get_all_rank_data(self):
        """
            * 获取所有榜单的数据列表；
            从json中获取并返回，可能为空；
        """
        self.get_rank_data()
        try:
            return self.rank_data['data']['list']
        except:
            return []

    def get_clear_rank_data(self):
        """
            * 获取清榜数据；
            从json中获取并返回，可能为空；
        """
        self.get_rank_data()
        try:
            return self.rank_data['data']['clear']
        except:
            return []

    def get_max_min_rank(self, app_type_list):
        """
            * 获取产品最高榜单时对应时间及对应总榜分类榜榜位；
            返回如下格式：{\n
            　　　　　　　　　　'榜单类型': rank_type_name,\n
            　　　　　　　　　　'平均排名': mean_rank_num,\n
            　　　　　　　　　　'最高排名': max_rank_num,\n
            　　　　　　　　　　'最高排名日期': max_rank_date,\n
            　　　　　　　　　　'出现次数': count_list_num\n
            　　　　　　　}
        """
        self.get_rank_data()
        rank_type_info = [{}, {}]
        if self.rank_data['msg'] == '成功':
            for rank_info in self.rank_data['data']['list']:
                rank_type_name = rank_info['name']
                if rank_type_name == app_type_list[0] or rank_type_name == app_type_list[1]:
                    rank_num_list = []
                    for num, num_info in enumerate(rank_info['data']):
                        rank_num_list.append(num_info[0])

                    # 列表异常值补充，避免出现位置偏移计算出错；
                    rank_num_list = Qimai_Outside_Tool(rank_num_list).match_fillna_value()

                    mean_rank_num = int(np.mean(rank_num_list))  # 平均排名
                    min_rank_num = int(np.max(rank_num_list))
                    max_rank_num = int(np.min(rank_num_list))
                    min_rank_index = rank_num_list.index(min_rank_num)
                    max_rank_index = rank_num_list.index(max_rank_num)
                    min_rank_date = today_date-datetime.timedelta(364) + datetime.timedelta(min_rank_index)
                    max_rank_date = today_date-datetime.timedelta(364) + datetime.timedelta(max_rank_index)

                    # 计算分类榜最高排名在榜单出现次数；
                    count_list_num = rank_num_list.count(max_rank_num)

                    # 加入列表；
                    if '应用' in rank_type_name:
                        rank_type_info[0] = {
                            '榜单类型': rank_type_name,
                            '平均排名': mean_rank_num,
                            '最高排名': max_rank_num,
                            '最高排名日期': max_rank_date,
                            '出现次数': count_list_num
                        }
                    else:
                        rank_type_info[1] = {
                            '榜单类型': rank_type_name,
                            '平均排名': mean_rank_num,
                            '最高排名': max_rank_num,
                            '最高排名日期': max_rank_date,
                            '出现次数': count_list_num
                        }
            # 返回数据；
            return rank_type_info
        else:
            print('获取错误，请重试')
            return rank_type_info

    def get_type_rankNum(self):
        """
            * 获取App的总榜、一级分类、一级分类榜单、二级分类、二级分类榜单；
            * 返回数据第1、2个为字符串，第3个为列表，对应总榜榜单、一级分类榜单、二级分类榜单；
        """
        one_type, two_type = Get_App_SamePubApp(appid).get_app_genName()
        two_rank_data = Get_App_Rank(appid, today_date, today_date).get_rank_data()
        app_rank_info = ['', '', '']
        if two_rank_data['msg'] == '成功':
            for i in two_rank_data['data']['list']:
                if i['name'] == one_type:
                    rank_num = i['data'][-1][0]
                    app_rank_info[1] = rank_num
                elif i['name'] == two_type:
                    rank_num = i['data'][-1][0]
                    app_rank_info[2] = rank_num
                elif '总榜' in i['name']:
                    rank_num = i['data'][-1][0]
                    app_rank_info[0] = rank_num
        else:
            return one_type, two_type, app_rank_info # 返回总榜、一级分类榜、二级分类榜榜单；
        # 返回数据；
        return one_type, two_type, app_rank_info  # 返回总榜、一级分类榜、二级分类榜榜单；

# 获取开发商相关数据；
@qm_auth_check  # 登录检查；
class Get_App_SamePubApp():
    """
        * 获取开发商相关数据；
        * 举例①：获取开发商名称；
        * 举例②：获取开发商权重评分(写死的打分规则)；
    """
    def __init__(self, appid, country='cn'):
        self.appid = appid
        self.country = country

    def get_samePubApp(self):
        """
            * 获取开发商下json数据中的实际参数(排除了接口状态等)；
        """
        url = 'https://api.qimai.cn/app/samePubApp?appid=%s&country=%s' %(self.appid, self.country)
        res = session.get(url, headers=headers)
        self.app_samePubApp = res.json()['samePubApps']
        return self.app_samePubApp

    def get_app_genName(self):
        """
            * 获取当前App的两个分类名称(中文)；
        """
        self.get_samePubApp()
        for info in self.app_samePubApp:
            if str(info['appInfo']['appId']) == str(self.appid):
                self.app_total_genid = info['total']['brand']
                self.app_class_genid = info['class']['brand']
                return self.app_total_genid, self.app_class_genid
            else:
                return '', ''

    def get_samePubApp_sorce(self):
        """
            * 获取开发商权重评分(自带算法)；
        """
        self.get_samePubApp()
        cp_quanzhong_list = []
        for x in self.app_samePubApp:
            all_rank_num = x['total']['ranking']
            all_rank_quanzhong = round(1 - int(all_rank_num) / 1500, 4)
            if all_rank_quanzhong == 1:
                cp_quanzhong_list.append(0)
            else:
                cp_quanzhong_list.append(all_rank_quanzhong)

        return max(cp_quanzhong_list)

# 获取关键词的相关数据；
@qm_auth_check  # 登录检查；
class Get_Keyword_Info():
    """
        * 获取关键词下相关数据；
        * 举例①：获取关键词下产品信息；
        * 举例②：获取关键词下联想词；
        search_type: 搜索类型：默认全部，其他可选例如App、开发者等
    """
    def __init__(self, keyword, start_date=today_date, end_date=today_date-one_day, search_type='all', country='cn', version='ios12', device='iphone', status=6):
        self.keyword = keyword
        self.start_date = start_date
        self.end_date = end_date
        self.search_type= search_type
        self.country = country
        self.device = device
        self.version = version
        self.status = status

    def get_keyword_search(self, page_num=1):
        """
            * 获取关键词下产品信息(第一页)：
            * 默认搜索版本为iOS 12；
        """
        url = 'https://api.qimai.cn/search/index?device=%s&country=%s&search=%s&date=%s&version=%s&search_type=%s&changeRateDate=&changeRateType=top10&sdate=%s&edate=%s&status=%s&page=%s' %(self.device, self.country, self.keyword, self.start_date, self.version, self.search_type, self.start_date, self.end_date, self.status, page_num)
        headers = {
            'origin': 'https://www.qimai.cn',
            'referer': 'https://www.qimai.cn/',
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_1_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36 Edg/88.0.705.63'
        }
        res = session.get(url, headers=headers)
        self.keyword_search_index = res.json()
        return self.keyword_search_index

    def get_keyword_search_list(self, max_index=1000000):
        """
            * 获取关键词下产品信息，带翻页：
            * 默认搜索版本为iOS 12；
        """
        self.keyword_search_more_list = []
        page_num = 1
        run_app_num = 50
        while True:
            url = 'https://api.qimai.cn/search/index?device=%s&country=%s&search=%s&date=%s&version=%s&search_type=%s&changeRateDate=&page=%s&changeRateType=top10&sdate=%s&edate=%s&status=%s' %(self.device, self.country, self.keyword, self.start_date, self.version, self.search_type, page_num, self.start_date, self.end_date, self.status)
            headers = {
                'origin': 'https://www.qimai.cn',
                'referer': 'https://www.qimai.cn/',
                'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_1_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36 Edg/88.0.705.63'
            }
            res = session.get(url, headers=headers)
            self.keyword_search_more_list.append(res.json())
            page_num += 1
            run_app_num += 50
            if run_app_num > max_index:
                break
        return self.keyword_search_more_list

    def get_keyword_wordinfo(self):
        """
            * 获取关键词下关键词相关信息:
            * 包含指数、结果数、WordID等；
        """
        url = 'https://api.qimai.cn/search/getWordInfo?device=%s&country=%s&search=%s&version=%s&date=%s&search_type=%s&status=%s' %(self.device, self.country, self.keyword, self.version, self.start_date, self.search_type, self.status)
        headers = {
            'origin': 'https://www.qimai.cn',
            'referer': 'https://www.qimai.cn/',
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_1_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36 Edg/88.0.705.63'
        }
        res = session.get(url, headers=headers)
        self.keyword_WordInfo = res.json()
        return self.keyword_WordInfo

    def get_keyword_ChangeRate(self, type='top10'):
        """
            * 获取关键词的变动率数据；
            * 默认T10变动率，且默认为昨日到今日的数据；
            :param type: 查看T10还是全部，例：top10
        """
        url = 'https://api.qimai.cn/search/keywordChangeRate?device=%s&word=%s&type=%s&version=%s&sdate=%s&edate=%s' %(self.device, self.keyword, type, self.version, self.start_date, self.end_date)
        res = session.get(url, headers=headers)
        self.keyword_ChangeRate = res.json()
        return self.keyword_ChangeRate

    def get_keywordHistory_hints(self):
        """
            * 获取时间段内关键词历史热度：
            start_date: 时间段开始日期\n
            end_date: 时间段结束日期
        """
        url = 'https://api.qimai.cn/app/searchHints'
        payload='device=%s&word[0]=%s&country=%s&sdate=%s&edate=%s' %(self.device, quote(self.keyword, 'utf-8'), self.country, self.start_date, self.end_date)
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.87 Safari/537.36"
        }
        res = session.post(url, data=payload, headers=headers)
        self.keywordHistory_hints = res.json()
        return self.keywordHistory_hints

    def get_hotSearch_data(self):
        """
            * 获取关键词热搜相关数据-默认90天内全部数据；
        """
        url = 'https://api.qimai.cn/engagement/historySearch?country=%s&version=%s&search_type=1&search=%s' %(self.country, self.version, self.keyword)
        res = session.get(url, headers=headers)
        self.keyword_hotSearch_data = res.json()
        return self.keyword_hotSearch_data

    def get_seven_hotSearch(self):
        """
            * 获取关键词近7日上热搜数据：
            * 返回第1个为次数，第2个为时长；
        """
        self.get_hotSearch_data()
        hot_search_all = ['', '']
        hot_search_data = self.keyword_hotSearch_data['data']['collect']['show_collect'][2]  # 近07日数据；
        for i in hot_search_data:
            title = i['title']
            if title == '近7日上榜次数':
                hot_search_all[0] = i['value']
            elif title == '近7日上榜时长':
                hot_search_all[1] = i['value']

        # 返回数据；
        return hot_search_all

    def get_thirty_hotSearch(self):
        """
            * 获取关键词近30日上热搜数据：
            * 返回第1个为次数，第2个为时长；
        """
        self.get_hotSearch_data()
        hot_search_all = ['', '']
        hot_search_data = self.keyword_hotSearch_data['data']['collect']['show_collect'][1]  # 近30日数据；
        for i in hot_search_data:
            title = i['title']
            if title == '近30日上榜次数':
                hot_search_all[0] = i['value']
            elif title == '近30日上榜时长':
                hot_search_all[1] = i['value']

        # 返回数据；
        return hot_search_all

    def get_ninety_hotSearch(self):
        """
            * 获取关键词近90日上热搜数据：
            * 返回第1个为次数，第2个为时长；
        """
        self.get_hotSearch_data()
        hot_search_all = ['', '']
        hot_search_data = self.keyword_hotSearch_data['data']['collect']['show_collect'][0]  # 近90日数据；
        for i in hot_search_data:
            title = i['title']
            if title == '近90日上榜次数':
                hot_search_all[0] = i['value']
            elif title == '近90日上榜时长':
                hot_search_all[1] = i['value']

        # 返回数据；
        return hot_search_all

    def get_keyword_extend(self, max_index=1000000, orderBy='', order=''):
        """
            * 关键词扩展助手接口：
            :param max_index: 最大获取扩展词数
            :param orderBy: 相关度排序，例：desc
            :param order: 搜索指数排序，例：desc
        """
        self.keyword_extend_list = []
        page_num = 1
        run_app_num = 100
        while True:
            url = 'https://api.qimai.cn/trend/keywordExtend?keyword=%s&page=%s&orderBy=%s&order=%s' %(self.keyword, page_num, orderBy, order)
            res = session.get(url, headers=headers)
            self.keyword_extend_list.append(res.json())
            page_num += 1
            run_app_num += 100
            if page_num > res.json()['maxPage'] or run_app_num > max_index:
                break
        return self.keyword_extend_list

    def get_keyword_extend_onePage(self, page_num=1, orderBy='', order=''):
        """
            * 关键词扩展助手接口：
            :param page_num: 页码数，默认获取第一页；
            :param orderBy: 相关度排序，例：desc
            :param order: 搜索指数排序，例：desc
        """
        url = 'https://api.qimai.cn/trend/keywordExtend?keyword=%s&page=%s&orderBy=%s&order=%s' % (self.keyword, page_num, orderBy, order)
        res = session.get(url, headers=headers)
        return res.json()

    def get_top_to_df(self, top_num=100):
        """
            * 关键词搜索后的产品列表转换为dataframe格式；
            * 此项会排除搜索结果中的专题、内购等；
            :param top_num: 限制获取的产品数量，例：3(前3个产品)
        """
        self.get_keyword_search()
        keyword_top_list = []
        run_num = 1
        for ky_search in self.keyword_search_index['appList']:
            if ky_search['kind'] == 'software' and run_num <= top_num:
                keyword_top_list.append(ky_search['appInfo'])
                run_num += 1
        self.keyword_top_df = Qimai_Outside_Tool(keyword_top_list).json_to_df()
        return self.keyword_top_df

    def get_keyword_hints(self):
        """
            * 单独获取关键词的指数：
            * 返回具体关键词指数数值；
        """
        self.get_keyword_wordinfo()
        self.hints = self.keyword_WordInfo['wordInfo']['hints']
        return self.hints

    def get_keyword_results(self):
        """
            * 获取关键词搜索结果数：
            * 返回具体关键词搜索结果数值；
        """
        self.get_keyword_wordinfo()
        self.results = self.keyword_WordInfo['wordInfo']['search_no']
        return self.results

    def get_keyword_wordID(self):
        """
            * 获取关键词的词ID：
            * 返回具体关键词词ID数值；
        """
        self.get_keyword_wordinfo()
        self.wordID = self.keyword_WordInfo['wordInfo']['word_id']
        return self.wordID

# 获取产品的关键词相关数据；
@qm_auth_check  # 登录检查；
class Get_App_Keyword():
    """
        * 获取App的关键词相关信息；
        * 举例①：获取App的对应时间覆盖数据(默认当日)；
        * 举例②：获取App不同日期的T3、T5数据；
    """
    def __init__(self, appid, run_time=today_date, country='cn', version='ios12', device='iphone'):
        self.appid = appid
        self.run_time = run_time
        self.country = country
        self.device = device
        self.version = version

    def get_keywordDetail(self):
        """
            * 获取产品在某日的所有覆盖词数据：
            * 默认获取日期为当日；
        """
        url = 'https://api.qimai.cn/app/keywordDetail?country=%s&appid=%s&version=%s&sdate=%s&device=%s&edate=' %(self.country, self.appid, self.version, self.run_time, self.device)
        res = session.get(url, headers=headers)
        self.app_keywordDetail = res.json()
        return self.app_keywordDetail

    def get_keywordSummary(self):
        """
            * 获取产品在某日的不同档位关键词数量：
            * 此项包含掉词数量及新增词数量；
            * 覆盖词上方的汇总表，默认获取日期为当日；
        """
        url = 'https://api.qimai.cn/app/keywordSummary?country=%s&appid=%s&version=%s&sdate=%s&device=%s&edate=' %(self.country, self.appid, self.version, self.run_time, self.device)
        res = session.get(url, headers=headers)
        self.app_keywordSummary = res.json()
        return self.app_keywordSummary

    def get_keyword_data(self):
        """
            * 返回产品的各项覆盖数据，例如>=4605的T3、T10、分别有多少个，新增多少个；
        """
        app_name = Get_App_Appinfo(self.appid).get_subname()
        self.get_keywordSummary()
        fugai_one_data_list = [app_name, '', '', '', '', '', '']
        fugai_two_data_list = [app_name, '', '', '', '', '', '']
        if self.app_keywordSummary['msg'] == '成功':
            for i in self.app_keywordSummary['keywordSummary']:
                if i['title'] == '合计':  # 总计覆盖情况；
                    # 第一个表的数据；
                    fugai_one_data_list[1] = int(i['all']['num'])
                    fugai_one_data_list[2] = int(i['top3']['num'])
                    fugai_one_data_list[3] = int(i['top10']['num'])
                elif i['title'] == '≥4605':  # 有效覆盖情况；
                    # 第一个表的数据；
                    fugai_one_data_list[4] = int(i['all']['num'])
                    fugai_one_data_list[5] = int(i['top3']['num'])
                    fugai_one_data_list[6] = int(i['top10']['num'])
                    # 第二个表的数据；
                    fugai_two_data_list[1] = int(i['top3']['num'])
                # 开始获取第二个表的数据；
                elif i['title'] == '4605～4999':
                    fugai_two_data_list[2] = int(i['top3']['num'])
                elif i['title'] == '5000～5999':
                    fugai_two_data_list[3] = int(i['top3']['num'])
                elif i['title'] == '6000～6999':
                    fugai_two_data_list[4] = int(i['top3']['num'])
                elif i['title'] == '7000～7999':
                    fugai_two_data_list[5] = int(i['top3']['num'])
                elif i['title'] == '≥8000':
                    fugai_two_data_list[6] = int(i['top3']['num'])

        return fugai_one_data_list, fugai_two_data_list

    def get_search_appKeyword(self, keyword, end_date, start_date=today_date):
        url = 'https://api.qimai.cn/app/searchAppKeywords?keywords=%s&country=%s&device=%s&version=%s&appid=%s&sdate=%s&edate=%s' %(keyword, self.country, self.device, self.version, self.appid, start_date, end_date)
        res = session.get(url, headers=headers)
        self.search_appKeyword_data = res.json()
        return self.search_appKeyword_data

    def get_AnalysisDataKeyword(self, start_date, end_date, keyword_hot_start=4605):
        """
            * 获取时间段内关键词覆盖数量历史：
            * 此项支持多个档位，具体参考官网区间；
            :param start_date: 开始日期
            :param end_date: 结束日期
            :param keyword_hot_start: 起始热度：默认4605
        """
        self.start_date = start_date
        self.end_date = end_date
        url = 'https://api.qimai.cn/account/getAnalysisDataKeyword?appid=%s&country=%s&device=%s&sdate=%s&edate=%s&version=%s&hints=%s' %(self.appid, self.country, self.device, self.start_date, self.end_date, self.version, keyword_hot_start)
        res = session.get(url, headers=headers)
        self.app_AnalysisDataKeyword = res.json()
        return self.app_AnalysisDataKeyword

    def get_keywordHistory_rank(self, keyword, start_date=today_date-datetime.timedelta(7), end_date=today_date, day=1, word_id=''):
        """
            * 获取时间段内关键词历史排名数据(word_id可无，函数自带获取方式)；
            * 可指定按分钟、小时、天，具体参考官网，默认按天；
            :param keyword: 关键词
            :param start_date: 开始日期
            :param end_date: 结束日期
        """
        if len(str(word_id)) == 0:
            word_id = Get_Keyword_Info(keyword).get_keyword_wordID()
        url = 'https://api.qimai.cn/app/keywordHistory?version=%s&device=%s&country=%s&appid=%s&day=%s&sdate=%s&edate=%s&word_id=%s&word=%s' %(self.version, self.device, self.country, self.appid, day, start_date, end_date, word_id, keyword)
        res = session.get(url, headers=headers)
        self.app_keywordHistor_data = res.json()
        return self.app_keywordHistor_data

    def get_match_keywordRank(self, keyword, start_date=today_date, end_date=today_date-one_day, day=1):
        """
            * 匹配App下某个关键词是否已掉词：
        """
        self.get_keywordHistory_rank(keyword, start_date, end_date, day)
        if self.app_keywordHistor_data['msg'] == '成功':
            for i in self.app_keywordHistor_data['data']['list']:
                if i['name'] == '排名':
                    today_rank = i['data'][-1][1]
                    if str(today_rank) == 'None':
                        return '掉词'
                    else:
                        return '有排名'
        else:
            return '掉词'

    def get_match_keywordLost(self, keyword, start_date=today_date, end_date=today_date-one_day, day=0):
        """
            * 匹配App下某个关键词是否未覆盖；
        """
        self.get_search_appKeyword(keyword, end_date, start_date)
        if self.search_appKeyword_data['msg'] == '成功':
            for i in self.search_appKeyword_data['wordinfo']:
                n_keyword = i['w']
                if n_keyword.lower() == keyword.lower():
                    if int(i['r']) == -1:
                        # 等于-1则为未覆盖；
                        return '未覆盖'
                    elif int(i['r']) == 0:
                        # 等于0则需要继续判断
                        n_keyword_status = Get_App_Keyword(self.appid).get_match_keywordRank(keyword, start_date, end_date, day)
                        if n_keyword_status == '掉词':
                            return '掉词'
                        else:
                            return '未知'
                    else:
                        return '未知'
        else:
            return '未知'

    def get_keywordDetail_to_df(self):
        """
            * 关键词覆盖数据转换dataframe格式：
            * 返回dataframe格式并重命名列；
        """
        self.get_keywordDetail()
        self.json_df = json_normalize(self.app_keywordDetail['data'])
        self.json_df.columns = ['关键词ID', '关键词', '排名', '变动前排名', '排名变动值', '指数', '结果数', '未知1', '未知2']
        return self.json_df

    def get_app_cover_regular(self, qualified_keyword_num=3000):
        """
            * 判断产品的覆盖数量是否合格(专用)：
            * 返回是否合格、总覆盖数、T3数、T10数；
            :param qualified_keyword_num: 大于等于多少的算合格，默认3000；
        """
        self.get_keywordSummary()
        for keywordSummary_info in self.app_keywordSummary['keywordSummary']:
            title = keywordSummary_info['title']
            if title == '合计':
                all_keyword = keywordSummary_info['all']['num']
                top3_keyword = keywordSummary_info['top3']['num']
                top10_keyword = keywordSummary_info['top10']['num']
                if int(all_keyword) >= qualified_keyword_num:
                    return ['覆盖合格', all_keyword, top3_keyword, top10_keyword]
                else:
                    return ['覆盖不合格', all_keyword, top3_keyword, top10_keyword]

# 获取产品评论的相关接口；
@qm_auth_check  # 登录检查；
class Get_App_Comment():
    """
        * 获取App的评论相关数据；
        * 举例①：获取App每天的新增评论数；
        * 举例②：获取App指定星级每天评论数据；
    """
    def __init__(self, appid, start_date=today_date-datetime.timedelta(days=29), end_date=today_date, country='cn'):
        self.appid = appid
        self.start_date = start_date
        self.end_date = end_date
        self.country = country

    def get_commentRate(self):
        """
            * 获取App当前的总评分、平均分等(返回json)，仅需appid参数；
        """
        url = 'https://api.qimai.cn/app/commentRate?appid=%s&country=%s' %(self.appid, self.country)
        res = session.get(url, headers=headers)
        return res.json()

    def get_commentRateNum(self, typec='day'):
        """
            * 获取1-5星每个星级每天的评论增删数量；
            :param typec: 评论计量时间单位：默认按天
        """
        url = 'https://api.qimai.cn/app/commentRateNum?appid=%s&country=%s&sdate=%s&edate=%s&typec=%s' %(self.appid, self.country, self.start_date, self.end_date, typec)
        res = session.get(url, headers=headers)
        self.app_commentRateNum = res.json()
        return self.app_commentRateNum

    def get_commentRateNum_add(self, typec='day'):
        """
            * 获取1-5星时间段内新增评论数；
            :param typec: 评论计量时间单位：默认按天
        """
        self.get_commentRateNum(typec)
        pinlun_num_list = []
        for i in self.app_commentRateNum['rateInfo']:
            pinlun_num_list.append(i['data'][0][1])  # 新增评论加进去

        return np.sum(pinlun_num_list)

    def get_commentNum(self, delete=-1):
        """
            * 获取每日已删除未删除评论数量；
            :param delete: 每日评论统计类型，默认全部评论，其他可选例如未删除评论、已删除评论
        """
        url = 'https://api.qimai.cn/app/commentNum?appid=%s&country=%s&delete=%s&sdate=%s&edate=%s' %(self.appid, self.country, delete, self.start_date, self.end_date)
        res = session.get(url, headers=headers)
        self.app_commentNum = res.json()
        return self.app_commentNum

    def get_comment(self, search_word='', star='five', orderType='time', commentType='default'):
        """
            * 获取详细每条评论内容：
            * 包含星级、用户昵称、评论内容等(默认5星)；
            :param star: 评论星级，默认5星
            :param orderType: 评论排序类型，默认最新评价，其他可选例如最优帮助、最高评价、最低评价
            :param commentType: 评论类型，默认全部评论，其他可选例如开发者回复、未删除、已删除
        """
        url = 'https://api.qimai.cn/app/comment?appid=%s&country=%s&sword=&sdate=%s+00:00:00&edate=%s+23:59:59&orderType=%s&commentType=%s&sword=%s&star=%s' %(self.appid, self.country, self.start_date, self.end_date, orderType, commentType, search_word, star)
        res = session.get(url, headers=headers)
        self.app_comment = res.json()
        return self.app_comment

    def get_all_commentRateNum(self, typec='day'):
        """
            * 获取所有1-5星评论数量汇总为1列：
            * 返回dataframe格式数据；
        """
        self.get_commentRateNum(typec)
        df = pd.DataFrame({})
        for comment_info in self.app_commentRateNum['rateInfo']:
            df_new = Qimai_Outside_Tool(comment_info['data']).list_to_df()
            df = pd.concat([df, df_new])
        df.columns = ['日期', '评论数']
        df['日期'] = df['日期'].apply(lambda x: Qimai_Outside_Tool(x).time_to_date())
        df = df.groupby('日期').sum()
        return df

    def get_Star_commentRateNum(self, star_value='五星', typec='day'):
        """
            * 获取指定星级的评论数量汇总：
            * 默认获取5星的，返回dataframe格式数据；
        """
        self.get_commentRateNum(typec)
        df = pd.DataFrame({})
        for comment_info in self.app_commentRateNum['rateInfo']:
            if comment_info['name'] == star_value:
                df_new = Qimai_Outside_Tool(comment_info['data']).list_to_df()
                df = pd.concat([df, df_new])
        df.columns = ['日期', '评论数']
        df['日期'] = df['日期'].apply(lambda x: Qimai_Outside_Tool(x).time_to_date())
        df = df.groupby('日期').sum()
        return df

    def get_commentRate_num(self):
        """
            * 获取App当前的总评分、平均分数值(返回2个值)，仅需appid参数；
        """
        res_json = self.get_commentRate()
        total_num = res_json['rateInfo']['current']['total']
        ratingAverage_rate = res_json['rateInfo']['current']['ratingAverage']
        return total_num, ratingAverage_rate

# 获取清榜列表相关数据；
@qm_auth_check  # 登录检查；
class Get_Clear_Rank_List():
    """
        * 获取清榜列表相关数据；
        * 举例①：获取当前清榜列表所有清榜产品相关数据；
        status_type: 清榜应用类型，默认全部，其他可选例如免费、付费\n
        clear_type: 清榜列表产品当前状态筛选，默认全部，其他可选清榜、已恢复
    """
    def __init__(self, start_date=today_date-datetime.timedelta(days=6), end_date=today_date, genre_type=36, status_type=3, clear_type=1):
        self.start_date = start_date
        self.end_date = end_date
        self.clear_type = clear_type
        self.status_type = status_type
        self.genre_type = genre_type

    def get_clear_rank(self):
        """
            * 获取时间段内清榜类目下产品相关信息：
            * 从类中指定开始结束时间；
            * 返回列表格式数据，列表中都是json；
        """
        self.clear_rank_list = []
        page_num = 1
        while True:
            url = 'https://api.qimai.cn/rank/clear?1=&sdate=%s&edate=%s&page=%s&type=%s&genre=%s&status=%s' %(self.start_date, self.end_date, page_num, self.clear_type, self.genre_type, self.status_type)
            res = session.get(url, headers=headers)
            self.clear_rank_list.append(res.json())
            page_num += 1
            if page_num > res.json()['maxPage']:
                break
        return self.clear_rank_list

    def get_clear_rank_onePage(self, page_num=1):
        """
            * 获取时间段内清榜类目下产品相关信息：
            * 从类中指定开始结束时间；
            :param page_num: 页码数，默认获取第一页；
        """
        url = 'https://api.qimai.cn/rank/clear?1=&sdate=%s&edate=%s&page=%s&type=%s&genre=%s&status=%s' %(self.start_date, self.end_date, page_num, self.clear_type, self.genre_type, self.status_type)
        res = session.get(url, headers=headers)
        return res.json()


# 获取清词列表相关数据；
@qm_auth_check  # 登录检查；
class Get_Clear_Keyword_List():
    """
        * 获取清词列表相关数据(清词的产品多所以按日展示的)；
        * 举例①：获取当前清词列表所有清词产品相关数据；
        filter: 清词产品类型，默认过滤下架应用，其他可选不过滤\n
        search_word: 清词产品，可搜索产品名，默认不搜索\n
        sort_field: 其他排序规则，默认清词前关键词数量\n
        sort_type: 清词前关键词数量排序规则，默认降序\n
    """
    def __init__(self, start_date=today_date, end_date=today_date, genre_type=36, filter='offline', search_word='', export_type='rank_clear_words', sort_field='beforeClearNum', sort_type='desc'):
        self.start_date = start_date
        self.end_date = end_date
        self.filter = filter
        self.search_word = search_word
        self.export_type = export_type
        self.sort_field = sort_field
        self.sort_type = sort_type
        self.genre_type = genre_type

    def get_clear_keyword(self):
        """
            * 获取时间段内清词列表产品相关信息：
            * 从类中指定开始结束时间；
            * 返回列表格式数据，列表中都是json；
        """
        self.clear_word_list = []
        page_num = 1
        while True:
            url = 'https://api.qimai.cn/rank/clearWords?edate=%s&page=%s&genre=%s&sdate=%s&filter=%s&export_type=%s&sort_field=%s&sort_type=%s&search=%s' %(self.end_date, page_num, self.genre_type, self.start_date, self.filter, self.export_type, self.sort_field, self.sort_type, self.search_word)
            res = session.get(url, headers=headers)
            self.clear_word_list.append(res.json())
            page_num += 1
            if page_num > res.json()['maxPage']:
                break
        return self.clear_word_list

    def get_clear_keyword_onePage(self, page_num=1):
        """
            * 获取时间段内清词列表产品相关信息：
            * 从类中指定开始结束时间；
            :param page_num: 页码数，默认获取第一页；
        """
        url = 'https://api.qimai.cn/rank/clearWords?edate=%s&page=%s&genre=%s&sdate=%s&filter=%s&export_type=%s&sort_field=%s&sort_type=%s&search=%s' %(self.end_date, page_num, self.genre_type, self.start_date, self.filter, self.export_type, self.sort_field, self.sort_type, self.search_word)
        res = session.get(url, headers=headers)
        return res.json()

# 获取上架、下架产品列表相关数据；
@qm_auth_check  # 登录检查；
class Get_App_ON_Offline_List():
    """
        * 获取上架、下架列表相关数据(上下架的产品多所以按日展示的)；
        * 举例①：获取当前下架列表所有下架产品相关数据；
        option: 上架、下架监控排序，默认按近期最高排名
    """
    def __init__(self, start_date=today_date, end_date=today_date, genre_type=36, country='cn', option=4, search_word=''):
        self.start_date = start_date
        self.end_date = end_date
        self.search_word = search_word
        self.option = option
        self.country = country
        self.genre_type =genre_type

    def get_app_offline(self):
        """
            * 获取时间段内下架列表产品相关信息：
            * 从类中指定开始结束时间；
            * 返回列表格式数据，列表中都是json；
        """
        self.app_offline_list = []
        page_num = 1
        while True:
            url = 'https://api.qimai.cn/rank/offline?date=%s_%s&country=%s&genre=%s&option=%s&search=%s&sdate=%s&edate=%s&page=%s' % (self.start_date, self.end_date, self.country, self.genre_type, self.option, self.search_word, self.start_date, self.end_date, page_num)
            res = session.get(url, headers=headers)
            self.app_offline_list.append(res.json())
            page_num += 1
            if page_num > res.json()['maxPage']:
                break
        return self.app_offline_list

    def get_app_offline_onePage(self, page_num=1):
        """
            * 获取时间段内下架列表产品相关信息：
            * 从类中指定开始结束时间；
            :param page_num: 页码数，默认获取第一页；
        """
        url = 'https://api.qimai.cn/rank/offline?date=%s_%s&country=%s&genre=%s&option=%s&search=%s&sdate=%s&edate=%s&page=%s' % (self.start_date, self.end_date, self.country, self.genre_type, self.option, self.search_word, self.start_date, self.end_date, page_num)
        res = session.get(url, headers=headers)
        return res.json()

    def get_app_release(self, is_preorder='all'):
        """
            * 获取时间段内上架列表产品相关信息：
            * 从类中指定开始结束时间；
            * 返回列表格式数据，列表中都是json；
        """
        self.app_online_list = []
        page_num = 1
        while True:
            url = 'https://api.qimai.cn/rank/release?date=%s_%s&country=%s&genre=%s&is_preorder=%s&search=%s&sdate=%s&edate=%s&page=%s' % (self.start_date, self.end_date, self.country, self.genre_type, is_preorder, self.search_word, self.start_date, self.end_date, page_num)
            res = session.get(url, headers=headers)
            self.app_online_list.append(res.json())
            page_num += 1
            if page_num > res.json()['maxPage']:
                break
        return self.app_online_list

    def get_app_release_onePage(self, page_num=1, is_preorder='all'):
        """
            * 获取时间段内上架列表产品相关信息：
            * 从类中指定开始结束时间；
            :param page_num: 页码数，默认获取第一页；
        """
        url = 'https://api.qimai.cn/rank/release?date=%s_%s&country=%s&genre=%s&is_preorder=%s&search=%s&sdate=%s&edate=%s&page=%s' % (self.start_date, self.end_date, self.country, self.genre_type, is_preorder, self.search_word, self.start_date, self.end_date, page_num)
        res = session.get(url, headers=headers)
        return res.json()

# 获取预订App列表；
@qm_auth_check  # 登录检查；
class Get_PreOrder_AppList():
    """
        * 获取预订App列表相关数据；
        * 举例①：获取当前预订列表所有预订产品相关数据；
    """
    def __init__(self,  genre_type=36, country='cn', preOrder_order=1, price_status=3):
        self.preOrder_order = preOrder_order
        self.price_status = price_status
        self.genre_type = genre_type
        self.country = country

    def get_preOrder_applist(self):
        """
            * 获取时间段内预订App列表产品相关信息；
            * 从类中指定开始结束时间；
            * 返回列表格式数据，列表中都是json；
            preOrder_order - 预订排序规则，默认按照发布日期；\n
            price_status - 预订产品价格筛选，默认全部，1为免费，0为付费，3为全部
        """
        self.preOrder_applist_list = []
        page_num = 1
        while True:
            url = 'https://api.qimai.cn/rank/preOrder?genre=%s&country=%s&order=%s&status=%s&page=%s' %(self.genre_type, self.country, self.preOrder_order, self.price_status, page_num)
            res = session.get(url, headers=headers)
            self.preOrder_applist_list.append(res.json())
            page_num += 1
            if page_num > res.json()['maxPage']:
                break
        return self.preOrder_applist_list

    def get_preOrder_applist_onePage(self, page_num=1):
        """
            * 获取时间段内预订App列表产品相关信息；
            * 从类中指定开始结束时间；
            :param page_num: 页码数，默认获取第一页；
            preOrder_order - 预订排序规则，默认按照发布日期；\n
            price_status - 预订产品价格筛选，默认全部，1为免费，0为付费，3为全部
        """
        url = 'https://api.qimai.cn/rank/preOrder?genre=%s&country=%s&order=%s&status=%s&page=%s' %(self.genre_type, self.country, self.preOrder_order, self.price_status, page_num)
        res = session.get(url, headers=headers)
        return res.json()

# 获取产品被精品推荐及上热搜情况列表；
@qm_auth_check  # 登录检查；
class Get_App_Recommend():
    """
        * 获取产品精品推荐及热搜列表相关数据；
        * 举例①：获取当前被精品推荐所有数据；
        * 举例②：获取当前被推荐上热搜的次数时间等；
    """
    def __init__(self, appid, country='cn'):
        self.appid = appid
        self.country = country

    def get_app_featured(self):
        """
            * 获取App被精品推荐列表信息(非首页)：
        """
        url = 'https://api.qimai.cn/app/featured?country=%s&appid=%s' %(self.country, self.appid)
        res = session.get(url, headers=headers)
        self.app_featured = res.json()
        return self.app_featured

    def get_app_engagement(self, start_date, end_date):
        """
            * 获取App上热搜推荐列表信息：
            * App信息页数据，不是热搜查询页；
            :param start_date: 开始日期
            :param end_date: 结束日期
        """
        url = 'https://api.qimai.cn/app/engagement'
        payload='app_id=%s&s_date=%s&e_date=%s' %(self.appid, start_date, end_date)
        res = session.post(url, data=payload, headers=headers)
        self.app_engagement = res.json()
        return self.app_engagement

    def get_featured_is_match(self):
        """
            * 上精品推荐匹配函数：
            * 匹配产品是否上过推荐；
        """
        self.get_app_featured()
        tuijian_num = len(self.app_featured['featured'])
        if tuijian_num > 0:
            return ['有推荐', tuijian_num]
        else:
            return ['无推荐', tuijian_num]

    def get_featured_type_match(self, match_type='Today'):
        """
            * 上精品推荐匹配函数：
            * 匹配上某个类型的次数、时长；
        """
        self.get_app_featured()
        match_num = 0
        continue_second = 0
        for featured_info in self.app_featured['featured']:
            featured_genre = featured_info['genre']
            if featured_genre == match_type:
                match_num += 1
                try:
                    continue_second += featured_info['sort_duration']
                except:
                    continue_second += featured_info['sort_edate']
        continue_time = Qimai_Outside_Tool(continue_second).second_conversion_time()
        return match_num, continue_time

# 获取App不同状态列表；
@qm_auth_check  # 登录检查；
class Get_App_Status():
    """
        * 获取App状态列表相关数据；
        * 举例①：获取当前App所有清榜情况；
        * 举例②：获取当前App所有下架情况；
        app_status_order: \n
        app_status_sort:
    """
    def __init__(self, appid, start_date='', end_date='', country='cn', app_status_order='', app_status_sort=''):
        self.appid = appid
        self.start_date = start_date
        self.end_date = end_date
        self.app_status_order = app_status_order
        self.app_status_sort = app_status_sort
        self.country = country

    def get_all_appStatusList(self):
        """
            * 获取所有状态信息：
            * 返回列表，列表中是所有json记录；
        """
        self.app_status_list = []
        page_num = 1
        while True:
            url = 'https://api.qimai.cn/app/appStatusList'
            payload='appid=%s&country=%s&status=all&sdate=%s&edate=%s&page=%s&order=%s&sort=%s' %(self.appid, self.country, self.start_date, self.end_date, page_num, self.app_status_order, self.app_status_sort)
            res = session.post(url, data=payload, headers=headers)
            self.app_status_list.append(res.json())
            page_num += 1
            if page_num > res.json()['maxPage']:
                break
        return self.app_status_list

    def get_all_appStatusList_onePage(self, page_num=1):
        """
            * 获取所有状态信息：
            :param page_num: 页码数，默认获取第一页；
        """
        url = 'https://api.qimai.cn/app/appStatusList'
        payload='appid=%s&country=%s&status=all&sdate=%s&edate=%s&page=%s&order=%s&sort=%s' %(self.appid, self.country, self.start_date, self.end_date, page_num, self.app_status_order, self.app_status_sort)
        res = session.post(url, data=payload, headers=headers)
        return res.json()

    def get_status_appStatusList(self, app_status_str='all'):
        """
            * 获取指定状态的所有状态信息：
            :param app_status_str: App状态，默认全部；
        """
        self.app_status_list = []
        page_num = 1
        while True:
            url = 'https://api.qimai.cn/app/appStatusList'
            payload='appid=%s&country=%s&status=%s&sdate=%s&edate=%s&page=%s&order=%s&sort=%s' %(self.appid, self.country, app_status_str, self.start_date, self.end_date, page_num, self.app_status_order, self.app_status_sort)
            headers = {
                'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.125 Safari/537.36',
                'content-type': 'application/x-www-form-urlencoded; charset=UTF-8'
            }
            res = session.post(url, data=payload, headers=headers)
            self.app_status_list.append(res.json())
            page_num += 1
            if page_num > res.json()['maxPage']:
                break
        return self.app_status_list

    def get_status_appStatusList_onePage(self, page_num=1, app_status_str='all'):
        """
            * 获取指定状态的所有状态信息：
            :param page_num: 页码数，默认获取第一页；
            :param app_status_str: App状态，默认全部；
        """
        url = 'https://api.qimai.cn/app/appStatusList'
        payload='appid=%s&country=%s&status=%s&sdate=%s&edate=%s&page=%s&order=%s&sort=%s' %(self.appid, self.country, app_status_str, self.start_date, self.end_date, page_num, self.app_status_order, self.app_status_sort)
        headers = {
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.125 Safari/537.36',
            'content-type': 'application/x-www-form-urlencoded; charset=UTF-8'
        }
        res = session.post(url, data=payload, headers=headers)
        return res.json()

    def get_new_status_info(self, app_status_str='all'):
        """
            * 获取指定状态最新的状态时间：
        """
        self.get_status_appStatusList(app_status_str)
        for status_list in self.app_status_list:
            if status_list['msg'] == '成功':
                if len(status_list['data']) > 0:
                    sdate_time = status_list['data'][0]['sdate']
                    return sdate_time
                else:
                    return ''
            return ''

    def get_old_status_info(self, app_status_str='all'):
        """
            * 获取指定状态最老的状态时间：
        """
        self.get_status_appStatusList(app_status_str)
        for status_list in self.app_status_list:
            if status_list['msg'] == '成功':
                if len(status_list['data']) > 0:
                    sdate_time = status_list['data'][-1]['sdate']
                    return sdate_time
                else:
                    return ''
            return ''

# 封装指数排行榜接口；
@qm_auth_check  # 登录检查；
class Get_Keyword_HintsRank():
    """
        * 获取指数排行榜列表相关数据；
        * 举例①：获取iPad指数排行榜数据；
        change_inc: \n
        minResult: 最小结果数\n
        maxResult: 最大结果数\n
        minHints: 最小指数\n
        maxHints: 最大指数\n
        minPopular: 最小流行度\n
        maxPopular: 最大流行度
    """
    def __init__(self, change_inc=0, run_time=today_date, minResult='', maxResult='', minHints='', maxHints='', minPopular='', maxPopular='', country='cn', device='iphone', genre_type=36):
        self.change_inc = change_inc
        self.minResult = minResult
        self.maxResult = maxResult
        self.minHints = minHints
        self.maxHints = maxHints
        self.minPopular = minPopular
        self.maxPopular = maxPopular
        self.run_time = run_time
        self.country = country
        self.genre_type = genre_type
        self.device = device

    def get_hints_rank(self):
        """
            * 获取搜索指数排行榜；
            * 返回列表，列表中是所有json记录；
        """
        self.keyword_hintsRank_list = []
        page_num = 1
        while True:
            url = 'https://api.qimai.cn/trend/keywordHintsRank?date=%s&page=%s&change_inc=%s&minResult=%s&maxResult=%s&genre=%s&minHints=%s&maxHints=%s&device=%s&country=%s&minPopular=%s&maxPopular=%s' %(self.run_time, page_num, self.change_inc, self.minResult, self.maxResult, self.genre_type, self.minHints, self.maxHints, self.device, self.country, self.minPopular, self.maxPopular)
            res = session.get(url, headers=headers)
            self.keyword_hintsRank_list.append(res.json())
            page_num += 1
            if page_num > res.json()['maxPage']:
                break
        return self.keyword_hintsRank_list

    def get_hints_rank_onePage(self, page_num=1):
        """
            * 获取搜索指数排行榜；
            :param page_num: 页码数，默认获取第一页；
        """
        url = 'https://api.qimai.cn/trend/keywordHintsRank?date=%s&page=%s&change_inc=%s&minResult=%s&maxResult=%s&genre=%s&minHints=%s&maxHints=%s&device=%s&country=%s&minPopular=%s&maxPopular=%s' %(self.run_time, page_num, self.change_inc, self.minResult, self.maxResult, self.genre_type, self.minHints, self.maxHints, self.device, self.country, self.minPopular, self.maxPopular)
        res = session.get(url, headers=headers)
        return res.json()

# 封装关键词落词、新进、上升、下降列表接口；
@qm_auth_check  # 登录检查；
class Get_Keyword_LoseNewDownUp_List():
    """
        * 获取关键词下落榜、新进、上升、下降产品列表相关数据；
        * 举例①：获取当前词落榜产品基本信息，落榜前排名等相关数据；
        top_history: 历史排名，默认全部，可选进入过T10
    """
    def __init__(self, keyword, start_date=today_date-datetime.timedelta(30), end_date=today_date, country='cn', version='ios12', device='iphone', top_history='all', filter='offline', search_word='', sort_type='desc'):
        self.keyword = keyword
        self.start_date = start_date
        self.end_date = end_date
        self.top_history = top_history
        self.filter = filter
        self.search_word = search_word
        self.sort_type = sort_type
        self.country = country
        self.version = version
        self.device = device

    def get_lostApp_list(self):
        """
            * 获取关键词下落榜产品列表：
            * 返回列表，列表中是所有json记录；
        """
        self.keyword_lostApp_list = []
        page_num = 1
        while True:
            url = 'https://api.qimai.cn/search/searchPageExtend?history=%s&version=%s&device=%s&filter=%s&word=%s&country=%s&date=oneMonth&sort=out_time&sort_type=%s&type=out&sdate=%s&edate=%s&page=%s' %(self.top_history, self.version, self.device, self.filter, self.keyword, self.country, self.sort_type, self.start_date, self.end_date, page_num)
            res = session.get(url, headers=headers)
            self.keyword_lostApp_list.append(res.json())
            page_num += 1
            if page_num > res.json()['total_page']:
                break
        return self.keyword_lostApp_list

    def get_lostApp_onePage(self, page_num=1):
        """
            * 获取词下落榜App的数据-第一页：
        """
        url = 'https://api.qimai.cn/search/searchPageExtend?history=%s&version=%s&device=%s&filter=%s&word=%s&country=%s&date=oneMonth&sort=out_time&sort_type=%s&type=out&sdate=%s&edate=%s&page=%s' % (self.top_history, self.version, self.device, self.filter, self.keyword, self.country, self.sort_type, self.start_date, self.end_date, page_num)
        res = session.get(url, headers=headers)
        self.lostApp_onePage_data = res.json()
        return self.lostApp_onePage_data

    def get_lostApp_num(self, page_num=1):
        """
            * 获取词下落榜App的数量：
        """
        self.get_lostApp_onePage(page_num)
        return self.lostApp_onePage_data['total_num']

    def get_newApp_list(self):
        """
            * 获取关键词下新覆盖产品的列表；
            * 返回列表，列表中是所有json记录；
        """
        self.keyword_newApp_list = []
        page_num = 1
        while True:
            url = 'https://api.qimai.cn/search/searchPageExtend?history=%s&version=%s&device=%s&filter=%s&word=%s&country=%s&date=oneMonth&sort=new_time&sort_type=%s&type=new&sdate=%s&edate=%s&page=%s' % (self.top_history, self.version, self.device, self.filter, self.keyword, self.country, self.sort_type, self.start_date, self.end_date, page_num)
            res = session.get(url, headers=headers)
            self.keyword_newApp_list.append(res.json())
            page_num += 1
            if page_num > res.json()['total_page']:
                break
        return self.keyword_newApp_list

    def get_newApp_onePage(self, page_num=1):
        """
            * 获取词下新进App的数据-第一页：
        """
        url = 'https://api.qimai.cn/search/searchPageExtend?history=%s&version=%s&device=%s&filter=%s&word=%s&country=%s&date=oneMonth&sort=new_time&sort_type=%s&type=new&sdate=%s&edate=%s&page=%s' % (self.top_history, self.version, self.device, self.filter, self.keyword, self.country, self.sort_type, self.start_date, self.end_date, page_num)
        res = session.get(url, headers=headers)
        self.newApp_onePage_data = res.json()
        return self.newApp_onePage_data

    def get_newApp_num(self, page_num=1):
        """
            * 获取词下新进App的数量：
        """
        self.get_newApp_onePage(page_num)
        return self.newApp_onePage_data['total_num']

    def get_rankDown_list(self):
        """
            * 获取关键词下排名下降较多的产品列表；
            * 返回列表，列表中是所有json记录；
        """
        self.keyword_rankDown_list = []
        page_num = 1
        while True:
            url = 'https://api.qimai.cn/search/searchPageExtend?history=%s&version=%s&device=%s&filter=%s&word=%s&country=%s&date=oneMonth&sort=down_rank&sort_type=%s&type=down&sdate=%s&edate=%s&page=%s' % (self.top_history, self.version, self.device, self.filter, self.keyword, self.country, self.sort_type, self.start_date, self.end_date, page_num)
            res = session.get(url, headers=headers)
            self.keyword_rankDown_list.append(res.json())
            page_num += 1
            if page_num > res.json()['total_page']:
                break
        return self.keyword_rankDown_list

    def get_rankDown_onePage(self, page_num=1):
        """
            * 获取词下排名下降较快App的数据-第一页：
        """
        url = 'https://api.qimai.cn/search/searchPageExtend?history=%s&version=%s&device=%s&filter=%s&word=%s&country=%s&date=oneMonth&sort=down_rank&sort_type=%s&type=down&sdate=%s&edate=%s&page=%s' % (self.top_history, self.version, self.device, self.filter, self.keyword, self.country, self.sort_type, self.start_date, self.end_date, page_num)
        res = session.get(url, headers=headers)
        self.rankDown_onePage_data = res.json()
        return self.rankDown_onePage_data

    def get_rankDown_num(self, page_num=1):
        """
            * 获取词下排名下降较快App的数量：
        """
        self.get_rankDown_onePage(page_num)
        return self.rankDown_onePage_data['total_num']

    def get_rankGoUp_list(self):
        """
            * 获取关键词下排名上升较多的产品列表；
            * 返回列表，列表中是所有json记录；
        """
        self.keyword_rankUp_list = []
        page_num = 1
        while True:
            url = 'https://api.qimai.cn/search/searchPageExtend?history=%s&version=%s&device=%s&filter=%s&word=%s&country=%s&date=oneMonth&sort=up_rank&sort_type=%s&type=up&sdate=%s&edate=%s&page=%s' % (self.top_history, self.version, self.device, self.filter, self.keyword, self.country, self.sort_type, self.start_date, self.end_date, page_num)
            res = session.get(url, headers=headers)
            self.keyword_rankUp_list.append(res.json())
            page_num += 1
            if page_num > res.json()['total_page']:
                break
        return self.keyword_rankUp_list

    def get_rankGoUp_onePage(self, page_num=1):
        """
             * 获取词下排名上升较快App的数据-第一页：
        """
        url = 'https://api.qimai.cn/search/searchPageExtend?history=%s&version=%s&device=%s&filter=%s&word=%s&country=%s&date=oneMonth&sort=up_rank&sort_type=%s&type=up&sdate=%s&edate=%s&page=%s' % (self.top_history, self.version, self.device, self.filter, self.keyword, self.country, self.sort_type, self.start_date, self.end_date, page_num)
        res = session.get(url, headers=headers)
        self.rankGoUp_onePage_data = res.json()
        return self.rankGoUp_onePage_data

    def get_rankGoUp_num(self, page_num=1):
        """
             * 获取词下排名上升较快App的数量：
        """
        self.get_rankGoUp_onePage(page_num)
        return self.rankGoUp_onePage_data['total_num']

    def get_t10App_list(self):
        """
            * 获取关键词下T10产品监控数据；
            * 返回列表，列表中是所有json记录；
        """
        self.keyword_t10App_list = []
        page_num = 1
        while True:
            url = 'https://api.qimai.cn/search/rankHistory?version=%s&device=%s&word=%s&page=%s&country=%s&sdate=%s&edate=%s' % (self.version, self.device, self.keyword, page_num, self.country, self.start_date, self.end_date)
            res = session.get(url, headers=headers)
            self.keyword_t10App_list.append(res.json())
            page_num += 1
            if page_num > res.json()['total_page']:
                break
        return self.keyword_t10App_list

    def get_t10App_list_onePage(self, page_num=1):
        """
            * 获取关键词下T10产品监控数据；
            :param page_num: 页码数，默认获取第一页；
        """
        url = 'https://api.qimai.cn/search/rankHistory?version=%s&device=%s&word=%s&page=%s&country=%s&sdate=%s&edate=%s' % (self.version, self.device, self.keyword, page_num, self.country, self.start_date, self.end_date)
        res = session.get(url, headers=headers)
        return res.json()


# 获取免费、付费、畅销榜单产品列表；
@qm_auth_check  # 登录检查；
class Get_FreePaidGross_RankList():
    """
        * 获取免费、付费、畅销榜产品列表；
        * 举例①：获取游戏畅销榜前100产品信息；
    """
    def __init__(self, genre_type=36, snapshot='', run_time=today_date, country='cn', brand='', device='iphone'):
        self.snapshot = snapshot
        self.run_time = run_time
        self.country = country
        self.brand = brand
        self.device = device
        self.genre_type = genre_type

    def get_updateTime_data(self, page_num=1):
        """
            * 获取榜单快照更新时间列表；
        """
        url = 'https://api.qimai.cn/rank/indexSnapshot?brand=%s&device=%s&country=%s&genre=%s&date=%s&page=%s&is_rank_index=1' %(self.brand, self.device, self.country, self.genre_type, self.run_time, page_num)
        res = session.get(url, headers=headers)
        self.rank_update_data = res.json()
        return self.rank_update_data

    def get_freeRank_list(self, max_index=1000000):
        """
            * 获取免费榜产品列表-所有页面，一页50个：
            :param max_index: 获取产品数量
        """
        self.app_freeRank_list = []
        page_num = 1
        run_app_num = 50
        while True:
            url = 'https://api.qimai.cn/rank/index?brand=free&device=%s&country=%s&genre=%s&date=%s&snapshot=%s&is_rank_index=1&page=%s' %(self.device, self.country, self.genre_type, self.run_time, self.snapshot, page_num)
            res = session.get(url, headers=headers)
            self.app_freeRank_list.append(res.json())
            page_num += 1
            run_app_num += 50
            if page_num > res.json()['maxPage'] or run_app_num > max_index:
                break
        return self.app_freeRank_list

    def get_freeRank_onePage(self, page_num=1):
        """
            * 获取免费榜产品列表-第一页，一页50个：
        """
        url = 'https://api.qimai.cn/rank/index?brand=free&device=%s&country=%s&genre=%s&date=%s&snapshot=%s&is_rank_index=1&page=%s' % (self.device, self.country, self.genre_type, self.run_time, self.snapshot, page_num)
        res = session.get(url, headers=headers)
        return res.json()

    def get_paidRank_list(self, max_index=1000000):
        """
            * 获取付费榜产品列表：
            :param max_index: 获取产品数量
        """
        self.app_paidRank_list = []
        page_num = 1
        run_app_num = 50
        while True:
            url = 'https://api.qimai.cn/rank/index?brand=paid&device=%s&country=%s&genre=%s&date=%s&snapshot=%s&is_rank_index=1&page=%s' %(self.device, self.country, self.genre_type, self.run_time, self.snapshot, page_num)
            res = session.get(url, headers=headers)
            self.app_paidRank_list.append(res.json())
            page_num += 1
            run_app_num += 50
            if page_num > res.json()['maxPage'] or run_app_num > max_index:
                break
        return self.app_paidRank_list

    def get_paidRank_onePage(self, page_num=1):
        """
            * 获取付费榜产品列表-第一页，一页50个：
        """
        url = 'https://api.qimai.cn/rank/index?brand=paid&device=%s&country=%s&genre=%s&date=%s&snapshot=%s&is_rank_index=1&page=%s' % (self.device, self.country, self.genre_type, self.run_time, self.snapshot, page_num)
        res = session.get(url, headers=headers)
        return res.json()

    def get_grossRank_list(self, max_index=1000000):
        """
            * 获取畅销榜产品列表：
            :param max_index: 获取产品数量
        """
        self.app_grossRank_list = []
        page_num = 1
        run_app_num = 50
        while True:
            url = 'https://api.qimai.cn/rank/index?brand=grossing&device=%s&country=%s&genre=%s&date=%s&snapshot=%s&is_rank_index=1&page=%s' %(self.device, self.country, self.genre_type, self.run_time, self.snapshot, page_num)
            res = session.get(url, headers=headers)
            self.app_grossRank_list.append(res.json())
            page_num += 1
            run_app_num += 50
            if page_num > res.json()['maxPage'] or run_app_num > max_index:
                break
        return self.app_grossRank_list

    def get_grossRank_onePage(self, page_num=1):
        """
            * 获取畅销榜产品列表-第一页，一页50个：
        """
        url = 'https://api.qimai.cn/rank/index?brand=grossing&device=%s&country=%s&genre=%s&date=%s&snapshot=%s&is_rank_index=1&page=%s' % (self.device, self.country, self.genre_type, self.run_time, self.snapshot, page_num)
        res = session.get(url, headers=headers)
        return res.json()

# 获取预估下载量及预估收入接口；
@qm_auth_check  # 登录检查；
class Get_AppDownRevenue_Data():
    """
        * 获取产品预估下载量及预估收入数据；
        * 举例①：获取产品在某时间段内每日预估下载量数据；
    """
    def __init__(self, appid, start_date=today_date-datetime.timedelta(days=6), end_date=today_date-one_day, country='cn', device='iphone'):
        self.appid = appid
        self.start_date = start_date
        self.end_date = end_date
        self.country = country
        self.device = device

    def get_down_data(self):
        """
            * 获取产品在时间段内预估下载量数据：
        """
        url = 'https://api.qimai.cn/pred/download?appid=%s&country=%s&sdate=%s&edate=%s&platform=%s' %(self.appid, self.country, self.start_date, self.end_date, self.device)
        res = session.get(url, headers=headers)
        self.app_downNum_list = res.json()
        return self.app_downNum_list

    def get_revenue_data(self):
        """
            * 获取产品在时间段内预估收入数据：
        """
        url = 'https://api.qimai.cn/pred/revenue?appid=%s&country=%s&sdate=%s&edate=%s&platform=%s' %(self.appid, self.country, self.start_date, self.end_date, self.device)
        res = session.get(url, headers=headers)
        self.app_revenueNum_list = res.json()
        return self.app_revenueNum_list

# 获取iOS 14/iOS 13、iOS 12热搜；
@qm_auth_check  # 登录检查；
class Get_HotSearch_Data():
    """
        * 获取热搜相关数据；
        * 举例①：获取近期上榜的关键词数量指数区间分析；
        * 举例②：获取热搜更新时间分布数据；
    """
    def __init__(self, start_date=today_date-datetime.timedelta(days=6), end_date=today_date, country='cn', version='ios12', device='iphone'):
        self.start_date = start_date
        self.end_date = end_date
        self.country = country
        self.version = version
        self.device = device

    def get_hotSearch_search(self, tab_type=437476):
        """
            * 获取iOS13/iOS14、iOS 12热搜数据：
            * 包含热搜关键词、热搜产品；
        """
        url = 'https://api.qimai.cn/engagement/getHotSearch%s?country=%s&sdate=%s&edate=%s&tab_type=%s' %(self.version, self.country, self.start_date, self.end_date, tab_type)
        res = session.get(url, headers=headers)
        self.date_hotSearch_search = res.json()
        return self.date_hotSearch_search

    def get_hotSearch_rank(self):
        """
            * 获取iOS13/iOS14、iOS 12历史热搜排行：
        """
        url = 'https://api.qimai.cn/engagement/hotSearchRank?version=%s&country=%s&device=%s&sdate=%s&edate=%s' %(self.version, self.country, self.device, self.start_date, self.end_date)
        res = session.get(url, headers=headers)
        self.date_hotSearch_rank = res.json()
        return self.date_hotSearch_rank

    def get_hotSearch_analyze(self):
        """
            * 获取iOS13/iOS14、iOS 12热搜上榜分析：
        """
        url = 'https://api.qimai.cn/engagement/brandAnalyze?version=%s&country=%s&device=%s&sdate=%s&edate=%s' %(self.version, self.country, self.device, self.start_date, self.end_date)
        res = session.get(url, headers=headers)
        self.date_hotSearch_analyze = res.json()
        return self.date_hotSearch_analyze

    def get_hotSearch_monitor(self):
        """
            * 获取iOS13/iOS14、iOS 12热搜榜更新监测：
        """
        url = 'https://api.qimai.cn/engagement/hotSearchMonitor?version=%s&country=%s&device=%s&sdate=%s&edate=%s' %(self.version, self.country, self.device, self.start_date, self.end_date)
        res = session.get(url, headers=headers)
        self.date_hotSearch_monitor = res.json()
        return self.date_hotSearch_monitor

# 榜单上升下降最快数据；
@qm_auth_check  # 登录检查；
class Get_Rank_UpDown_List():
    """
        * 获取榜单上升下降较快的产品；
        * 举例①：获取今日下降较快产品；
        brand: 价格类型：默认全部，其他可选例如免费、付费、畅销
    """
    def __init__(self, upDown_type='one', brand='all', country='cn', device='iphone', genre_type=36):
        self.upDown_type = upDown_type
        self.brand = brand
        self.country = country
        self.device = device
        self.genre_type = genre_type

    def get_up_rank(self, max_index=1000000):
        """
            * 获取榜单上升较快的产品列表：
            * 返回列表，列表中是多个json；
            :param max_index: 最大获取产品数；
        """
        self.up_rank_list = []
        page_num = 1
        run_app_num = 200
        while True:
            url = 'https://api.qimai.cn/rank/float?float=up&genre=%s&device=%s&type=%s&brand=%s&country=%s&page=%s' %(self.genre_type, self.device, self.upDown_type, self.brand, self.country, page_num)
            res = session.get(url, headers=headers)
            self.up_rank_list.append(res.json())
            page_num += 1
            run_app_num += 200
            if page_num > res.json()['maxPage'] or run_app_num > max_index:
                break
        return self.up_rank_list

    def get_up_rank_onePgae(self, page_num=1):
        """
            * 获取榜单上升较快的产品列表：
            :param page_num: 页码数，默认获取第一页；
        """
        url = 'https://api.qimai.cn/rank/float?float=up&genre=%s&device=%s&type=%s&brand=%s&country=%s&page=%s' %(self.genre_type, self.device, self.upDown_type, self.brand, self.country, page_num)
        res = session.get(url, headers=headers)
        return res.json()

    def get_down_rank(self, max_index=1000000):
        """
            * 获取榜单下降较快的产品列表：
            * 返回列表，列表中是多个json；
            :param max_index: 最大获取产品数；
        """
        self.down_rank_list = []
        page_num = 1
        run_app_num = 200
        while True:
            url = 'https://api.qimai.cn/rank/float?float=down&genre=%s&device=%s&type=%s&brand=%s&country=%s&page=%s' %(self.genre_type, self.device, self.upDown_type, self.brand, self.country, page_num)
            res = session.get(url, headers=headers)
            self.down_rank_list.append(res.json())
            page_num += 1
            run_app_num += 200
            if page_num > res.json()['maxPage'] or run_app_num > max_index:
                break
        return self.down_rank_list

    def get_down_rank_onePage(self, page_num=1):
        """
            * 获取榜单下降较快的产品列表：
            :param page_num: 页码数，默认获取第一页；
        """
        url = 'https://api.qimai.cn/rank/float?float=down&genre=%s&device=%s&type=%s&brand=%s&country=%s&page=%s' %(self.genre_type, self.device, self.upDown_type, self.brand, self.country, page_num)
        res = session.get(url, headers=headers)
        return res.json()

# 获取各类覆盖排行榜；
@qm_auth_check  # 登录检查；
class Get_Cover_Rank():
    """
        * 获取各类覆盖排行榜；
        * 举例①：获取Top3总数量覆盖排行榜；
    """
    def __init__(self, search_word='', country='cn', device='iphone', genre_type=36):
        self.search_word = search_word
        self.country = country
        self.device = device
        self.genre_type = genre_type

    def get_keyword_cover(self, max_index=1000000, keyword_type='all', match_hints='0'):
        """
            * 获取产品关键词覆盖排行榜产品列表：
            * 返回列表，列表中是多个json；
            :param max_index: 最大获取产品数；
            :param keyword_type: 获取类型限制，例：全部/T3/T10；
            :param match_hints: 获取指数限制，例：0/4605；
        """
        self.keyword_cover_list = []
        page_num = 1
        run_app_num = 200
        while True:
            url = 'https://api.qimai.cn/rank/keywordCoverRank?device=%s&country=%s&genre=%s&type=%s&isinc=0&hints=%s&page=%s' %(self.device, self.country, self.genre_type, keyword_type, match_hints, page_num)
            res = session.get(url, headers=headers)
            self.keyword_cover_list.append(res.json())
            page_num += 1
            run_app_num += 200
            if page_num > res.json()['maxPage'] or run_app_num > max_index:
                break
        return self.keyword_cover_list

    def get_keyword_cover_onePage(self, page_num=1, keyword_type='all', match_hints='0'):
        """
            * 获取产品关键词覆盖排行榜产品列表：
            :param page_num: 页码数，默认获取第一页；
            :param keyword_type: 获取类型限制，例：全部/T3/T10；
            :param match_hints: 获取指数限制，例：0/4605；
        """
        url = 'https://api.qimai.cn/rank/keywordCoverRank?device=%s&country=%s&genre=%s&type=%s&isinc=0&hints=%s&page=%s' %(self.device, self.country, self.genre_type, keyword_type, match_hints, page_num)
        res = session.get(url, headers=headers)
        return res.json()

    def get_grow_cover(self, max_index=1000000, keyword_type='all', match_hints='0'):
        """
            * 获取产品关键词增长榜产品列表：
            * 返回列表，列表中是多个json；
            :param max_index: 最大获取产品数；
            :param keyword_type: 获取类型限制，例：全部/T3/T10；
            :param match_hints: 获取指数限制，例：0/4605；
        """
        self.grow_cover_list = []
        page_num = 1
        run_app_num = 200
        while True:
            url = 'https://api.qimai.cn/rank/keywordCoverRank?device=%s&country=%s&genre=%s&type=%s&isinc=1&hints=%s&page=%s' %(self.device, self.country, self.genre_type, keyword_type, match_hints, page_num)
            res = session.get(url, headers=headers)
            self.grow_cover_list.append(res.json())
            page_num += 1
            run_app_num += 200
            if page_num > res.json()['maxPage'] or run_app_num > max_index:
                break
        return self.grow_cover_list

    def get_grow_cover_onePage(self, page_num=1, keyword_type='all', match_hints='0'):
        """
            * 获取产品关键词增长榜产品列表：
            :param page_num: 页码数，默认获取第一页；
            :param keyword_type: 获取类型限制，例：全部/T3/T10；
            :param match_hints: 获取指数限制，例：0/4605；
        """
        url = 'https://api.qimai.cn/rank/keywordCoverRank?device=%s&country=%s&genre=%s&type=%s&isinc=1&hints=%s&page=%s' %(self.device, self.country, self.genre_type, keyword_type, match_hints, page_num)
        res = session.get(url, headers=headers)
        return res.json()

    def get_topic_cover(self, max_page=1000000):
        """
            * 获取专题关键词覆盖榜列表：
            * 返回列表，列表中是多个json；
            :param max_page: 最大获取专题页码数；
        """
        self.topic_cover_list = []
        page_num = 1
        while True:
            url = 'https://api.qimai.cn/search/searchExtendCover?kind=editorialItem&page=%s&device=%s&country=%s&genre=%s&search=%s' %(page_num, self.device, self.country, self.genre_type, self.search_word)
            res = session.get(url, headers=headers)
            self.topic_cover_list.append(res.json())
            page_num += 1
            if page_num > res.json()['max_page'] or page_num > max_page:
                break
        return self.topic_cover_list

    def get_topic_cover_onePage(self, page_num=1):
        """
            * 获取专题关键词覆盖榜列表：
            :param page_num: 页码数，默认获取第一页；
        """
        url = 'https://api.qimai.cn/search/searchExtendCover?kind=editorialItem&page=%s&device=%s&country=%s&genre=%s&search=%s' %(page_num, self.device, self.country, self.genre_type, self.search_word)
        res = session.get(url, headers=headers)
        return res.json()

    def get_develpoer_cover(self, max_index=1000000):
        """
            * 获取开发者关键词覆盖榜列表：
            * 返回列表，列表中是多个json；
            :param max_index: 最大获取开发者数；
        """
        self.develpoer_cover_list = []
        page_num = 1
        run_app_num = 50
        while True:
            url = 'https://api.qimai.cn/search/searchExtendCover?kind=softwareDeveloper&page=%s&device=%s&country=%s&genre=%s&search=%s' %(page_num, self.device, self.country, self.genre_type, self.search_word)
            res = session.get(url, headers=headers)
            self.develpoer_cover_list.append(res.json())
            page_num += 1
            run_app_num += 50
            if page_num > res.json()['max_page'] or run_app_num > max_index:
                break
        return self.develpoer_cover_list

    def get_develpoer_cover_onePage(self, page_num=1):
        """
            * 获取开发者关键词覆盖榜列表：
            :param page_num: 页码数，默认获取第一页；
        """
        url = 'https://api.qimai.cn/search/searchExtendCover?kind=softwareDeveloper&page=%s&device=%s&country=%s&genre=%s&search=%s' %(page_num, self.device, self.country, self.genre_type, self.search_word)
        res = session.get(url, headers=headers)
        return res.json()

    def get_purchase_cover(self, max_index=1000000):
        """
            * 获取内购关键词覆盖榜列表：
            * 返回列表，列表中是多个json；
            :param max_index: 最大获取开发者数；
        """
        self.purchase_cover_list = []
        page_num = 1
        run_app_num = 50
        while True:
            url = 'https://api.qimai.cn/search/searchExtendCover?kind=softwareAddOn&page=%s&device=%s&country=%s&genre=%s&search=%s' %(page_num, self.device, self.country, self.genre_type, self.search_word)
            res = session.get(url, headers=headers)
            self.purchase_cover_list.append(res.json())
            page_num += 1
            run_app_num += 50
            if page_num > res.json()['max_page'] or run_app_num > max_index:
                break
        return self.purchase_cover_list

    def get_purchase_cover_onePage(self, page_num=1):
        """
            * 获取内购关键词覆盖榜列表：
            :param page_num: 页码数，默认获取第一页；
        """
        url = 'https://api.qimai.cn/search/searchExtendCover?kind=softwareAddOn&page=%s&device=%s&country=%s&genre=%s&search=%s' %(page_num, self.device, self.country, self.genre_type, self.search_word)
        res = session.get(url, headers=headers)
        return res.json()
