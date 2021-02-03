import requests,datetime,time,warnings,json,calendar,math,os
from datetime import date
from dateutil.relativedelta import relativedelta
from pandas.io.json import json_normalize
from urllib.parse import quote
import pandas as pd
import numpy as np
from scipy.stats import norm, mstats
warnings.filterwarnings("ignore")


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

'''


# 保持会话；
session = requests.session()

# 请求头；
headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.87 Safari/537.36"
}

# 钉钉推送；
class DingDing_Push:
    def __init__(self, push_title, *args, push_status='执行成功', now_time=str(datetime.datetime.now())[:19], push_url='https://oapi.dingtalk.com/robot/send?access_token=f3a590b8c5f4c4777fe0f217067f15132091bff53e2a2143a5daa981d795159d'):
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
        payload = {
            "msgtype": "markdown",
            "markdown": {
                "title": "【%s】%s" %(self.now_time[:10], self.push_title),
                "text": "**推送事件**：%s\n\n**推送时间**：%s\n\n**推送状态**：%s" %(self.push_title, self.now_time, self.push_status)
            }
        }
        payload = json.dumps(payload)
        res = requests.post(self.push_url, data=payload, headers=self.headers)

    def app_rank_abnormal_push(self):
        self.samePubApp_link = 'https://www.qimai.cn/app/samePubApp/appid/%s/country/cn' %(self.other_var[0])
        self.app_rank_link = 'https://www.qimai.cn/app/rank/appid/%s/country/cn' %(self.other_var[0])
        self.app_keyword_link = 'https://www.qimai.cn/app/keyword/appid/%s/country/cn' %(self.other_var[0])
        # self.app_name = self.other_var[1]
        # self.samePubApp_name = self.other_var[2]
        # self.offline_time = self.other_var[3]
        # self.offline_yesterday_rank = self.other_var[4]
        payload = {
            "msgtype": "markdown",
            "markdown": {
                "title": "【%s】%s" %(self.now_time[:10], self.push_title),
                "text": "**推送事件**：%s\n\n**抓取时间**：%s\n\n**App名称**：[%s](%s)\n\n**开发商名称**：[%s](%s)\n\n**下架/清榜时间**：%s\n\n**下架/清榜前一日总榜**：%s" %(self.push_title, self.now_time, self.other_var[1], self.app_rank_link, self.other_var[2], self.samePubApp_link, self.other_var[3], self.other_var[4])
            }
        }
        payload = json.dumps(payload)
        res = requests.post(self.push_url, data=payload, headers=self.headers)

    def app_args_push(self):
        payload = {
            "msgtype": "markdown",
            "markdown": {
                "title": "%s" %(self.push_title),
                "text": "%s" %(self.other_var[0])
            }
        }
        payload = json.dumps(payload)
        res = requests.post(self.push_url, data=payload, headers=self.headers)

# 自动登录；
class Sing_Qimai:
    def __init__(self, user_id, user_pwd):
        self.user_id = user_id
        self.user_pwd = user_pwd

    def login_qm(self):
        url = 'https://api.qimai.cn/account/signinForm'
        payload = "username=%s&password=%s" %(self.user_id, self.user_pwd)
        headers = {
            'Content-Type': "application/x-www-form-urlencoded",
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.87 Safari/537.36"
        }
        res = session.post(url, headers=headers, data=payload)

# 计算七麦外的其他备用工具；
class Qimai_Outside_Tool:
    def __init__(self, *args):
        self.data_info = args

    def match_str_chinese(self):
        for ch in self.data_info[0]:
            if u'\u4e00' <= ch <= u'\u9fff':
                return True
        return False

    def match_publisher_company(self):
        company_str_list = ['公司', 'Technology', 'Beijing', '(', ')', '（', '）', 'Ltd', '.', 'Inc', 'china', '互联网', '科技', '网络', '计算机', 'LLC', '-', 'Company', 'games', '工作室', 'Tech', '信息', 'online', 'Network', '互动', '移动', '游戏', '技术', 'LIMITED', '株式会社', 'Tov', 'USA', 'UK', '银行', '组织', '机构']
        for company_str in company_str_list:
            if company_str.lower() in self.data_info[0].lower() or len(self.data_info[0])>20:
                return True
        return False

    def json_to_df(self):
        self.json_df = json_normalize(self.data_info[0])
        return self.json_df

    def list_to_df(self):
        self.list_df = pd.DataFrame(self.data_info[0])
        return self.list_df

    def unix_time(self):
        # 世界标准时间
        date_now = datetime.datetime.strptime(self.data_info[0], '%Y-%m-%d %H:%M:%S')
        # 北京时间UTC+8
        cst_time = date_now.astimezone(datetime.timezone(datetime.timedelta(hours=-8))).strftime("%Y-%m-%d %H:%M:%S")
        return cst_time

    def time_to_date(self):
        if len(str(self.data_info[0])) == 13:
            self.run_time = int(self.data_info[0]/1000)
        else:
            self.run_time = self.data_info[0]
        timeArray = time.localtime(self.run_time)
        otherStyleTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
        return otherStyleTime

    def date_to_time(self):
        if len(str(self.data_info[0])) == 10:
            self.run_date = self.data_info[0] + ' 00:00:00'
        timeArray = time.strptime(self.run_date, "%Y-%m-%d %H:%M:%S")
        timeStamp = int(time.mktime(timeArray))
        return timeStamp

    def get_month_time(self):
        day_start = datetime.date.fromisoformat(str(self.data_info[0]))
        day_end = datetime.date.fromisoformat(str(self.data_info[1]))
        # monthRange_start = calendar.monthrange(day_start.year, day_start.month)
        monthRange_end = calendar.monthrange(day_end.year, day_end.month)
        start_time = str(day_start)[:8] + str('01')
        end_time = str(day_end)[:8] + str(monthRange_end[1])
        return start_time, end_time

    def calc_interval_time(self):
        spider_time_datetime = datetime.datetime.strptime(str(self.data_info[0]), '%Y-%m-%d %H:%M:%S')
        rank_out_datetime = datetime.datetime.strptime(str(self.data_info[1]), '%Y-%m-%d %H:%M:%S')
        interval_seconds = (rank_out_datetime - spider_time_datetime).seconds
        m, s = divmod(interval_seconds, 60)
        h, m = divmod(m, 60)
        interval_time = "%02d小时%02d分钟%02d秒" % (h, m, s)  # 计算间隔时间；
        return interval_time

    def calc_overlap_days(self, s1, e1, s2, e2):
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
class Qimai_Intside_Tool:
    def __init__(self, data_info):
        self.data_info = data_info

    def rank_ios10_type(self):
        if self.data_info == '0.00' or self.data_info == '免费':
            return '总榜(免费)'
        else:
            return '总榜(付费)'

    def old_rank_num(self, rank_name='总榜(免费)'):
        for app_rank in self.data_info['data']['list']:
            if app_rank['name'] == rank_name:
                return app_rank['data'][0][0]
        else:
            return 0

    def new_rank_num(self, rank_name='总榜(免费)'):
        for app_rank in self.data_info['data']['list']:
            if app_rank['name'] == rank_name:
                return app_rank['data'][-1][0]
        else:
            return 0

    def lost_keyword_calc(self, appid, start_date, end_date):
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

# 常用的自定义参数；
class Qimai_Diy_Var:
    def __init__(self, country='cn', rank_type='all', version='ios12', device='iphone', search_type='all', brand='all', day=1, appRankShow=1, subclass='all', simple=1, rankEchartType=1, rankType='day', run_time=datetime.date.today(), status=6, keyword_hot_start=4605, typec='day', star='five', delete=-1, orderType='time', commentType='default', genre_type=36, status_type=3, clear_type=1, filter='offline', search_word='', export_type='rank_clear_words', sort_field='beforeClearNum', sort_type='desc', option=4, app_status_str='all', app_status_sdate='', app_status_edate='', app_status_order='', app_status_sort='', preOrder_order=1, change_inc=0, minResult='', maxResult='', minHints='', maxHints='', minPopular='', maxPopular='', top_history='all', lost_sort='out_time'):
        self.country = country
        self.rank_type = rank_type
        self.version = version
        self.device = device
        self.search_type= search_type
        self.brand = brand
        self.day = day
        self.appRankShow = appRankShow
        self.subclass = subclass
        self.simple = simple
        self.rankEchartType = rankEchartType
        self.rankType = rankType
        self.run_time = run_time
        self.one_day = datetime.timedelta(days=1)
        self.status = status
        self.keyword_hot_start = keyword_hot_start
        self.typec = typec
        self.star = star
        self.delete = delete
        self.orderType = orderType
        self.commentType = commentType
        self.clear_type = clear_type
        self.status_type = status_type
        self.genre_type = genre_type
        self.search_word = search_word
        self.filter = filter
        self.export_type = export_type
        self.sort_field = sort_field
        self.sort_type = sort_type
        self.option = option
        self.app_status_str = app_status_str
        self.app_status_sdate = app_status_sdate
        self.app_status_edate = app_status_edate
        self.app_status_order = app_status_order
        self.app_status_sort = app_status_sort
        self.preOrder_order = preOrder_order
        self.change_inc = change_inc
        self.minResult = minResult
        self.maxResult = maxResult
        self.minHints = minHints
        self.maxHints = maxHints
        self.minPopular = minPopular
        self.maxPopular = maxPopular
        self.lost_sort = lost_sort
        self.top_history = top_history

# 获取基础信息相关数据；
class Get_App_Appinfo(Qimai_Diy_Var):
    def __init__(self, appid):
        Qimai_Diy_Var.__init__(self)
        self.appid = appid

    def get_appinfo(self):
        url = 'https://api.qimai.cn/app/appinfo?appid=%s&country=%s' %(self.appid, self.country)
        res = session.get(url, headers=headers)
        self.appinfo = res.json()
        return self.appinfo

    def get_subname(self):
        self.get_appinfo()
        self.subname = self.appinfo['appInfo']['subname']
        return self.subname

# 获取榜单相关数据；
class Get_App_Rank(Qimai_Diy_Var):
    def __init__(self, appid, start_time, end_time):
        Qimai_Diy_Var.__init__(self)
        self.appid = appid
        self.start_time = start_time
        self.end_time = end_time

    def get_rank_info(self):
        url = 'https://api.qimai.cn/app/rankMore?appid=%s&country=%s&brand=%s&day=%s&appRankShow=%s&subclass=%s&simple=%s&sdate=%s&edate=%s&rankEchartType=%s&rankType=%s&device=%s' %(self.appid, self.country, self.brand, self.day, self.appRankShow, self.subclass, self.simple, self.start_time, self.end_time, self.rankEchartType, self.rankType, self.device)
        res = session.get(url, headers=headers)
        self.rank_info = res.json()
        return self.rank_info

    def all_rank(self):
        self.get_rank_info()
        try:
            return self.rank_info['data']['list']
        except:
            return []

    def clear_rank(self):
        self.get_rank_info()
        try:
            return self.rank_info['data']['clear']
        except:
            return []

# 获取开发商相关数据；
class Get_App_SamePubApp(Get_App_Appinfo, Qimai_Diy_Var):
    def __init__(self, appid):
        Get_App_Appinfo.__init__(self, appid)
        Qimai_Diy_Var.__init__(self)

    def get_samePubApp(self):
        url = 'https://api.qimai.cn/app/samePubApp?appid=%s&country=%s' %(self.appid, self.country)
        res = session.get(url, headers=headers)
        self.app_samePubApp = res.json()['samePubApps']
        return self.app_samePubApp

    def get_app_genName(self):
        self.get_samePubApp()
        for info in self.app_samePubApp:
            if str(info['appInfo']['appId']) == str(self.appid):
                self.app_total_genid = info['total']['brand']
                self.app_class_genid = info['class']['brand']
                return self.app_total_genid, self.app_class_genid

    def samePubApp_sorce(self):
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
class Get_Keyword_Info(Qimai_Diy_Var):
    def __init__(self, keyword):
        Qimai_Diy_Var.__init__(self)
        self.keyword = keyword

    def get_keyword_search(self):
        url = 'https://api.qimai.cn/search/index?device=%s&country=%s&search=%s&version=%s&date=%s&search_type=%s&status=%s&edate=%s' %(self.device, self.country, self.keyword, self.version, self.run_time, self.search_type, self.status, self.run_time-self.one_day)
        res = session.get(url, headers=headers)
        self.keyword_serch_index = res.json()
        return self.keyword_serch_index

    def get_keyword_wordinfo(self):
        url = 'https://api.qimai.cn/search/getWordInfo?country=%s&device=%s&search=%s&version=%s&date=%s&search_type=%s&status=%s&edate=%s' % (self.country, self.device, self.keyword, self.version, self.run_time, self.search_type, self.status, self.run_time - self.one_day)
        res = session.get(url, headers=headers)
        self.keyword_WordInfo = res.json()
        return self.keyword_WordInfo

    def get_keywordHistory_hints(self, start_date, end_date):
        url = 'https://api.qimai.cn/app/searchHints'
        payload='device=%s&word[0]=%s&country=%s&sdate=%s&edate=%s' %(self.device, quote(self.keyword, 'utf-8'), self.country, start_date, end_date)
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.87 Safari/537.36"
        }
        res = session.post(url, data=payload, headers=headers)
        self.keywordHistory_hints = res.json()
        return self.keywordHistory_hints

    def get_top_to_df(self, top_num=100):
        self.get_keyword_search()
        keyword_top_list = []
        run_num = 1
        for ky_search in self.keyword_serch_index['appList']:
            if ky_search['kind'] == 'software' and run_num <= top_num:
                keyword_top_list.append(ky_search['appInfo'])
                run_num += 1
        self.keyword_top_df = Qimai_Outside_Tool(keyword_top_list).json_to_df()
        return self.keyword_top_df

    def get_keyword_hints(self):
        self.get_keyword_wordinfo()
        self.hints = self.keyword_WordInfo['wordInfo']['hints']
        return self.hints

    def get_keyword_results(self):
        self.get_keyword_wordinfo()
        self.results = self.keyword_WordInfo['wordInfo']['search_no']
        return self.results

    def get_keyword_wordID(self):
        self.get_keyword_wordinfo()
        self.wordID = self.keyword_WordInfo['wordInfo']['word_id']
        return self.wordID

# 获取产品的关键词相关数据；
class Get_App_Keyword(Qimai_Diy_Var):
    def __init__(self, appid):
        Qimai_Diy_Var.__init__(self)
        self.appid = appid

    def get_keywordDetail(self):
        url = 'https://api.qimai.cn/app/keywordDetail?country=%s&appid=%s&version=%s&sdate=%s&device=%s&edate=' %(self.country, self.appid, self.version, self.run_time, self.device)
        res = session.get(url, headers=headers)
        self.app_keywordDetail = res.json()
        return self.app_keywordDetail

    def get_keywordSummary(self):
        url = 'https://api.qimai.cn/app/keywordSummary?country=%s&appid=%s&version=%s&sdate=%s&device=%s&edate=' %(self.country, self.appid, self.version, self.run_time, self.device)
        res = session.get(url, headers=headers)
        self.app_keywordSummary = res.json()
        return self.app_keywordSummary

    def get_AnalysisDataKeyword(self, start_time, end_time):
        self.start_time = start_time
        self.end_time = end_time
        url = 'https://api.qimai.cn/account/getAnalysisDataKeyword?appid=%s&country=%s&device=%s&sdate=%s&edate=%s&version=%s&hints=%s' %(self.appid, self.country, self.device, self.start_time, self.end_time, self.version, self.keyword_hot_start)
        res = session.get(url, headers=headers)
        self.app_AnalysisDataKeyword = res.json()
        return self.app_AnalysisDataKeyword

    def get_keywordHistory_rank(self, keyword, start_date, end_date):
        word_id = Get_Keyword_Info(keyword).get_keyword_wordID()
        url = 'https://api.qimai.cn/app/keywordHistory?version=%s&device=%s&country=%s&appid=%s&day=%s&sdate=%s&edate=%s&word_id=%s&word=%s' %(self.version, self.device, self.country, self.appid, self.day, start_date, end_date, word_id, keyword)
        res = session.get(url, headers=headers)
        self.app_keywordHistor_data = res.json()
        return self.app_keywordHistor_data

    def get_keywordDetail_to_df(self):
        self.get_keywordDetail()
        self.json_df = json_normalize(self.app_keywordDetail['data'])
        self.json_df.columns = ['关键词ID', '关键词', '排名', '变动前排名', '排名变动值', '指数', '结果数', '未知1', '未知2']
        return self.json_df

    def app_cover_regular(self):
        self.get_keywordSummary()
        for keywordSummary_info in self.app_keywordSummary['keywordSummary']:
            title = keywordSummary_info['title']
            if title == '合计':
                all_keyword = keywordSummary_info['all']['num']
                top3_keyword = keywordSummary_info['top3']['num']
                top10_keyword = keywordSummary_info['top10']['num']
                if int(all_keyword) >= 3000:
                    return ['覆盖合格', all_keyword, top3_keyword, top10_keyword]
                else:
                    return ['覆盖不合格', all_keyword, top3_keyword, top10_keyword]

# 获取产品评论的相关接口；
class Get_App_Comment(Qimai_Diy_Var):
    def __init__(self, appid, start_time, end_time):
        Qimai_Diy_Var.__init__(self)
        self.appid = appid
        self.start_time = start_time
        self.end_time = end_time

    def get_commentRateNum(self):
        url = 'https://api.qimai.cn/app/commentRateNum?appid=%s&country=%s&sdate=%s&edate=%s&typec=%s' %(self.appid, self.country, self.start_time, self.end_time, self.typec)
        res = session.get(url, headers=headers)
        self.app_commentRateNum = res.json()
        return self.app_commentRateNum

    def get_commentNum(self):
        url = 'https://api.qimai.cn/app/commentNum?appid=%s&country=%s&delete=%s&sdate=%s&edate=%s' %(self.appid, self.country, self.delete, self.start_time, self.end_time)
        res = session.get(url, headers=headers)
        self.app_commentNum = res.json()
        return self.app_commentNum

    def get_comment(self):
        url = 'https://api.qimai.cn/app/comment?appid=%s&country=%s&sword=&sdate=%s+00:00:00&edate=%s+23:59:59&orderType=%s&commentType=%s' %(self.appid, self.country, self.start_time, self.end_time, self.orderType, self.commentType)
        res = session.get(url, headers=headers)
        self.app_comment = res.json()
        return self.app_comment

    def get_all_commentRateNum(self):
        self.get_commentRateNum()
        df = pd.DataFrame({})
        for comment_info in self.app_commentRateNum['rateInfo']:
            df_new = Qimai_Outside_Tool(comment_info['data']).list_to_df()
            df = pd.concat([df, df_new])
        df.columns = ['日期', '评论数']
        df['日期'] = df['日期'].apply(lambda x: Qimai_Outside_Tool(x).time_to_date())
        df = df.groupby('日期').sum()
        return df

    def get_Star_commentRateNum(self, star_value='五星'):
        self.get_commentRateNum()
        df = pd.DataFrame({})
        for comment_info in self.app_commentRateNum['rateInfo']:
            if comment_info['name'] == star_value:
                df_new = Qimai_Outside_Tool(comment_info['data']).list_to_df()
                df = pd.concat([df, df_new])
        df.columns = ['日期', '评论数']
        df['日期'] = df['日期'].apply(lambda x: Qimai_Outside_Tool(x).time_to_date())
        df = df.groupby('日期').sum()
        return df

# 获取清榜列表相关数据；
class Get_Clear_Rank_List(Qimai_Diy_Var):
    def __init__(self, start_time, end_time):
        Qimai_Diy_Var.__init__(self)
        self.start_time = start_time
        self.end_time = end_time

    def get_clear_rank(self):
        self.clear_rank_list = []
        page_num = 1
        while True:
            url = 'https://api.qimai.cn/rank/clear?1=&sdate=%s&edate=%s&page=%s&type=%s&genre=%s&status=%s' %(self.start_time, self.end_time, page_num, self.clear_type, self.genre_type, self.status_type)
            res = session.get(url, headers=headers)
            self.clear_rank_list.append(res.json())
            page_num += 1
            if page_num > res.json()['maxPage']:
                break
        return self.clear_rank_list

# 获取清词列表相关数据；
class Get_Clear_Keyword_List(Qimai_Diy_Var):
    def __init__(self, start_time, end_time):
        Qimai_Diy_Var.__init__(self)
        self.start_time = start_time
        self.end_time = end_time

    def get_clear_keyword(self):
        self.clear_word_list = []
        page_num = 1
        while True:
            url = 'https://api.qimai.cn/rank/clearWords?edate=%s&page=%s&genre=%s&sdate=%s&filter=%s&export_type=%s&sort_field=%s&sort_type=%s&search=%s' %(self.end_time, page_num, self.genre_type, self.start_time, self.filter, self.export_type, self.sort_field, self.sort_type, self.search_word)
            res = session.get(url, headers=headers)
            self.clear_word_list.append(res.json())
            page_num += 1
            if page_num > res.json()['maxPage']:
                break
        return self.clear_word_list

# 获取下架产品列表相关数据；
class Get_App_Offline_List(Qimai_Diy_Var):
    def __init__(self, start_time, end_time):
        Qimai_Diy_Var.__init__(self)
        self.start_time = start_time
        self.end_time = end_time

    def get_app_offline(self):
        self.app_offline_list = []
        page_num = 1
        while True:
            url = 'https://api.qimai.cn/rank/offline?date=%s_%s&country=%s&genre=%s&option=%s&search=%s&sdate=%s&edate=%s&page=%s' % (self.start_time, self.end_time, self.country, self.genre_type, self.option, self.search_word, self.start_time, self.end_time, page_num)
            res = session.get(url, headers=headers)
            self.app_offline_list.append(res.json())
            page_num += 1
            if page_num > res.json()['maxPage']:
                break
        return self.app_offline_list

# 获取预订App列表；
class Get_PreOrder_AppList(Qimai_Diy_Var):
    def __init__(self):
        Qimai_Diy_Var.__init__(self)

    def get_preOrder_applist(self):
        self.preOrder_applist_list = []
        page_num = 1
        while True:
            url = 'https://api.qimai.cn/rank/preOrder?genre=%s&country=%s&order=%s&page=%s' %(self.genre_type, self.country, self.preOrder_order, page_num)
            res = session.get(url, headers=headers)
            self.preOrder_applist_list.append(res.json())
            page_num += 1
            if page_num > res.json()['maxPage']:
                break
        return self.preOrder_applist_list

# 获取产品被精品推荐及上热搜情况列表；
class Get_App_Recommend(Qimai_Diy_Var):
    def __init__(self, appid):
        Qimai_Diy_Var.__init__(self)
        self.appid = appid

    def get_app_featured(self):
        url = 'https://api.qimai.cn/app/featured?country=%s&appid=%s' %(self.country, self.appid)
        res = session.get(url, headers=headers)
        self.app_featured = res.json()
        return self.app_featured

    def get_app_engagement(self, start_time, end_time):
        url = 'https://api.qimai.cn/app/engagement'
        payload='app_id=%s&s_date=%s&e_date=%s' %(self.appid, start_time, end_time)
        res = session.post(url, data=payload, headers=headers)
        self.app_engagement = res.json()
        return self.app_engagement

    def featured_match(self):
        self.get_app_featured()
        tuijian_num = len(self.app_featured['featured'])
        if tuijian_num > 0:
            return ['有推荐', tuijian_num]
        else:
            return ['无推荐', tuijian_num]

# 获取App不同状态列表；
class Get_App_Status(Qimai_Diy_Var):
    def __init__(self, appid):
        Qimai_Diy_Var.__init__(self)
        self.appid = appid

    def get_all_appStatusList(self):
        self.app_status_list = []
        page_num = 1
        while True:
            url = 'https://api.qimai.cn/app/appStatusList'
            payload='appid=%s&country=%s&status=all&sdate=%s&edate=%s&page=1&order=%s&sort=%s' %(self.appid, self.country, self.app_status_sdate, self.app_status_edate, self.app_status_order, self.app_status_sort)
            res = session.post(url, data=payload, headers=headers)
            self.app_status_list.append(res.json())
            page_num += 1
            if page_num > res.json()['maxPage']:
                break
        return self.app_status_list

    def get_status_appStatusList(self):
        self.app_status_list = []
        page_num = 1
        while True:
            url = 'https://api.qimai.cn/app/appStatusList'
            payload='appid=%s&country=%s&status=%s&sdate=%s&edate=%s&page=1&order=%s&sort=%s' %(self.appid, self.country, self.app_status_str, self.app_status_sdate, self.app_status_edate, self.app_status_order, self.app_status_sort)
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

    def get_new_status_info(self):
        self.get_status_appStatusList()
        for status_list in self.app_status_list:
            if status_list['msg'] == '成功':
                if len(status_list['data']) > 0:
                    sdate_time = status_list['data'][0]['sdate']
                    return sdate_time
                else:
                    return ''
            return ''

    def get_old_status_info(self):
        self.get_status_appStatusList()
        for status_list in self.app_status_list:
            if status_list['msg'] == '成功':
                if len(status_list['data']) > 0:
                    sdate_time = status_list['data'][-1]['sdate']
                    return sdate_time
                else:
                    return ''
            return ''

# 封装指数排行榜接口；
class Get_Keyword_HintsRank(Qimai_Diy_Var):
    def __init__(self):
        Qimai_Diy_Var.__init__(self)

    def get_hints_rank(self):
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

# 封装关键词落词列表接口；
class Get_Keyword_LoseNewDownUp_List(Qimai_Diy_Var):
    def __init__(self, keyword, start_date=datetime.date.today(), end_date=datetime.date.today()):
        Qimai_Diy_Var.__init__(self)
        self.keyword = keyword
        self.start_date = start_date
        self.end_date = end_date

    def get_lostApp_list(self):
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

    def get_newApp_list(self):
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

    def get_rankDown_list(self):
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

    def get_rankGoUp_list(self):
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

    def get_t10App_list(self):
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

# 获取免费、付费、畅销榜单产品列表；
class Get_FreePaidGross_RankList(Qimai_Diy_Var):
    def __init__(self, snapshot=''):
        Qimai_Diy_Var.__init__(self)
        self.snapshot = snapshot

    def get_updateTime_list(self):
        url = 'https://api.qimai.cn/rank/indexSnapshot?brand=%s&device=%s&country=%s&genre=%s&date=%s&page=1&is_rank_index=1' %(self.brand, self.device, self.country, self.genre_type, self.run_time)
        res = session.get(url, headers=headers)
        self.rank_update_List = res.json()

    def get_freeRank_list(self, max_index=1000000):
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

    def get_paidRank_list(self, max_index=1000000):
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

    def get_grossRank_list(self, max_index=1000000):
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

# 获取预估下载量及预估收入接口；
class Get_AppDownRevenue_Data(Qimai_Diy_Var):
    def __init__(self, appid, start_date, end_date):
        Qimai_Diy_Var.__init__(self)
        self.appid = appid
        self.start_date = start_date
        self.end_date = end_date

    def get_down_data(self):
        url = 'https://api.qimai.cn/pred/download?appid=%s&country=%s&sdate=%s&edate=%s&platform=%s' %(self.appid, self.country, self.start_date, self.end_date, self.device)
        res = session.get(url, headers=headers)
        self.app_downNum_list = res.json()
        return self.app_downNum_list

    def get_revenue_data(self):
        url = 'https://api.qimai.cn/pred/revenue?appid=%s&country=%s&sdate=%s&edate=%s&platform=%s' %(self.appid, self.country, self.start_date, self.end_date, self.device)
        res = session.get(url, headers=headers)
        self.app_revenueNum_list = res.json()
        return self.app_revenueNum_list




