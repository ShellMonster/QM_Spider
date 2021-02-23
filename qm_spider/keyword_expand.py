"""
@FileName：keyword_expand.py\n
@Description：\n
@Author：道长\n
@Time：2021/2/2 13:57\n
@Department：运营部\n
@Website：www.geekaso.com.com\n
@Copyright：©2019-2021 七麦数据
"""


from qm_spider import *

# 获取需要查询的关键词列表；
def save_except(keyword, keyword_hot):
    df = pd.DataFrame({
        '关键词': [keyword],
        '关键词热度': [keyword_hot]
    })
    df.to_csv(
        './%s-关键词扩展性计算-异常值.csv' %(datetime.date.today()), mode='a', encoding='utf-8-sig', index=False, header=False
    )

# 获取需要查询的关键词列表；
def save_backup(keyword, keyword_len, keyword_all_num):
    df = pd.DataFrame({
        '关键词': [keyword],
        '关键词长度': [keyword_len],
        '扩展性': [keyword_all_num]
    })
    df.to_csv(
        './%s-关键词-扩展性计算.csv' % (str(datetime.date.today())), mode='a', encoding='utf-8-sig', index=False, header=False
    )

class Calc_Keyword_Expand:
    def __init__(self, file_path):
        self.file_path = file_path

    def calc_expand(self):
        if '.csv' in self.file_path:
            df = pd.read_csv(self.file_path)
        elif '.xlsx' in self.file_path or '.xls' in self.file_path:
            df = pd.read_excel(self.file_path)
        else:
            df = pd.DataFrame({})
            print('当前文件格式错误，请指定csv或者xlsx格式文件给予读取')
            exit()

        # # 提前处理异常数据；
        # # df[0] = df[0].fillna('0')
        # df['关键词'] = df['关键词'].fillna('0')
        # replace_text = os.popen('cd ~/Downloads/;pwd').read().replace('\n', '') + '/'

        # 准备计算：
        app_name_list = [i.start() for i in re.finditer('/', self.file_path)]
        app_name = self.file_path[app_name_list[-1]+1:self.file_path.index('关键词')-1]
        df['关键词'] = df['关键词'].astype('str')
        df_new = pd.DataFrame({})
        for num, keyword in enumerate(df['关键词'].values):
            # 判断是否包含特殊字符；
            regex = re.compile(u"[`~!@#$%^&*()+=|{}':',\\[\\].<>/?~！@#￥%……& amp;*（）——+|{}【】‘；：”“’。，、？|-]")
            # 判断是否包含英文；
            re_english = re.compile(u'[\u4e00-\u9fa5]', re.UNICODE)
            # if re.search(re_english, ky_find) is None:  # 判断字符是否为字母；
            #     print('\n【%s】不是中文，删除' % (ky_find))
            keyword_rank = df[df['关键词']==keyword]['排名'].values[0]
            try:
                keyword_hot = df[df['关键词']==keyword]['指数'].values[0]
            except:
                keyword_hot = df[df['关键词']==keyword]['搜索指数'].values[0]
            try:
                keyword_result = df[df['关键词']==keyword]['结果数'].values[0]
            except:
                keyword_result = df[df['关键词']==keyword]['搜索结果数'].values[0]
            try:
                keyword_popular = df[df['关键词']==keyword]['流行度'].values[0]
            except:
                keyword_popular = ''

            if bool(re.findall(regex, keyword)) == True:
                # print('【%s】行【%s】包含特殊字符' %(x + 1, keyword))
                pass
            else:
                # print('【%s】行【%s】不包含特殊字符' %(x + 1, keyword))
                if len(keyword) <= 6:
                    # 是否要英文，要则注释
                    # if re.search(re_english, str(keyword)) is None:
                    #     pass
                    # else:
                    keyword_len = len(keyword)  # 计算字符串长度
                    if keyword_len <= 6:
                        try:
                            keyword_all_num = len(df[df['关键词'].str.contains(keyword)])  # 包含;
                        except:
                            keyword_all_num = 0
                        df_old = pd.DataFrame({
                            '关键词': [keyword],
                            '排名': [keyword_rank],
                            '搜索指数': [keyword_hot],
                            '结果数': [keyword_result],
                            '扩展性': [keyword_all_num],
                            '流行度': [keyword_popular],
                            '长度': [keyword_len]
                        })
                        df_new = df_new.append(df_old)
                        print('\n第【%s】行【%s】关键词被包含次数为【%s】次，插入CSV成功。。。' % (num+1, keyword, keyword_all_num))
        # 合并去重；
        df_new = df_new.drop_duplicates(keep=False)
        df_new = df_new.sort_values(by='扩展性', ascending=False)
        df_new.to_excel('./%s_关键词扩展性计算.xlsx' % (app_name), index=False)