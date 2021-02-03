from qm_spider import *


class Get_Top_Keyword:
    def __init__(self, appid, keyword_hot_start, start_time, end_time, keyword_hot_end=150000):
        self.keyword_hot_start = keyword_hot_start
        self.keyword_hot_end = keyword_hot_end
        self.appid = appid
        self.start_time = datetime.date.fromisoformat(start_time)
        self.end_time = datetime.date.fromisoformat(end_time)
        self.one_day = datetime.timedelta(days=1)

    def df_to_excel(self, file_path='./'):
        df = self.get_all_top()
        df.to_excel(
            '%s%s_%s_Top关键词数据.xlsx' % (file_path, self.end_time, self.app_name), encoding='utf-8-sig', index=False
        )

    def get_all_top(self):
        self.app_name = Get_App_Appinfo(self.appid).get_subname()
        self.t1_all_list = []
        self.t2_all_list = []
        self.t3_all_list = []
        self.t5_all_list = []
        self.t10_all_list = []
        self.date_list = []
        self.now_app_list = []
        print('==========开始获取【%s】产品相关数据==========' %(self.app_name))
        while self.start_time <= self.end_time:
            get_app_keyword_data = Get_App_Keyword(self.appid)
            get_app_keyword_data.run_time = self.start_time
            get_app_keyword_data.keyword_hot_start = self.keyword_hot_start
            res = get_app_keyword_data.get_keywordDetail()
            if res['msg'] == '成功' and len(res['data']) > 0:
                df_keyword = Qimai_Outside_Tool(res['data']).json_to_df()
                df_keyword.columns = ['关键词ID', '关键词', '排名', '变动前排名', '排名变动值', '指数', '结果数', '未知1', '未知2']

                t1_all_num = df_keyword[(df_keyword['排名'] <= 1) & (df_keyword['指数'] >= self.keyword_hot_start) & (df_keyword['指数'] <= self.keyword_hot_end) & (df_keyword['排名变动值'] != 'lost')].shape[0]
                t2_all_num = df_keyword[(df_keyword['排名'] <= 2) & (df_keyword['指数'] >= self.keyword_hot_start) & (df_keyword['指数'] <= self.keyword_hot_end) & (df_keyword['排名变动值'] != 'lost')].shape[0]
                t3_all_num = df_keyword[(df_keyword['排名'] <= 3) & (df_keyword['指数'] >= self.keyword_hot_start) & (df_keyword['指数'] <= self.keyword_hot_end) & (df_keyword['排名变动值'] != 'lost')].shape[0]
                t5_all_num = df_keyword[(df_keyword['排名'] <= 5) & (df_keyword['指数'] >= self.keyword_hot_start) & (df_keyword['指数'] <= self.keyword_hot_end) & (df_keyword['排名变动值'] != 'lost')].shape[0]
                t10_all_num = df_keyword[(df_keyword['排名'] <= 10) & (df_keyword['指数'] >= self.keyword_hot_start) & (df_keyword['指数'] <= self.keyword_hot_end) & (df_keyword['排名变动值'] != 'lost')].shape[0]

                print('【%s】【%s】在【%s+】热度t3词有【%s】个' % (self.start_time, self.app_name, self.keyword_hot_start, t3_all_num))
                self.t1_all_list.append(t1_all_num)
                self.t2_all_list.append(t2_all_num)
                self.t3_all_list.append(t3_all_num)
                self.t5_all_list.append(t5_all_num)
                self.t10_all_list.append(t10_all_num)
                self.date_list.append(str(self.start_time))
                self.now_app_list.append(self.appid)
            else:
                print('【%s】【%s】在【%s+】热度t3词有【%s】个' % (self.start_time, self.app_name, self.keyword_hot_start, 0))
                self.t1_all_list.append(0)
                self.t2_all_list.append(0)
                self.t3_all_list.append(0)
                self.t5_all_list.append(0)
                self.t10_all_list.append(0)
                self.date_list.append(str(self.start_time))
                self.now_app_list.append(self.appid)

            self.start_time += self.one_day
        df = pd.DataFrame({
            'AppID': self.now_app_list,
            '日期': self.date_list,
            'T1数量': self.t1_all_list,
            'T2数量': self.t2_all_list,
            'T3数量': self.t3_all_list,
            'T5数量': self.t5_all_list,
            'T10数量': self.t10_all_list
        })
        return df


class Get_Multiple_Top_Keyword():
    def __init__(self, appid_list, keyword_hot_start, start_time, end_time, file_path='./'):
        for appid in appid_list:
            app_name = Get_App_Appinfo(appid).get_subname()
            df = Get_Top_Keyword(appid, keyword_hot_start, start_time, end_time).get_all_top()
            df.to_excel(
                '%s%s_%s_Top关键词数据.xlsx' %(file_path, end_time, app_name), encoding='utf-8-sig', index=False
            )