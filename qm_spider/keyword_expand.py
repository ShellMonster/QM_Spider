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
        '~/Downloads/%s-关键词扩展性计算-异常值.csv' %(datetime.date.today()), mode='a', encoding='utf-8-sig', index=False, header=False
    )

# 获取需要查询的关键词列表；
def save_backup(keyword, keyword_len, keyword_all_num):
    df = pd.DataFrame({
        '关键词': [keyword],
        '关键词长度': [keyword_len],
        '扩展性': [keyword_all_num]
    })
    # 当前日期；
    # df.to_csv(
    #     '~/Downloads/%s-%s-关键词扩展性计算.csv' % (str(datetime.date.today()), file_name.replace(replace_text.replace('Downloads/', ''), '').replace('.csv', '').replace('Downloads/', '').replace('Desktop/', '').replace('Documents/', '')), mode='a', encoding='utf-8-sig', index=False, header=False
    # )xt学费
    df.to_csv(
        '~/Downloads/%s-关键词-扩展性计算.csv' % (str(datetime.date.today())), mode='a', encoding='utf-8-sig', index=False, header=False
    )

#读取csv，并尝试代入;
# df = pd.read_csv('/Users/mac/Downloads/酷狗-关键词覆盖.csv', error_bad_lines=False) # , error_bad_lines=False
file_name = '/Users/DaoZhang/Downloads/墨迹天气_关键词覆盖数据_20210202 (1).xlsx'
df = pd.read_excel(file_name) # , error_bad_lines=False

# # 提前处理异常数据；
# # df[0] = df[0].fillna('0')
# df['关键词'] = df['关键词'].fillna('0')
# replace_text = os.popen('cd ~/Downloads/;pwd').read().replace('\n', '') + '/'

# excel_num = 0
df['关键词'] = df['关键词'].astype('str')
for x, ky in enumerate(df.values):
    #判断是否包含特殊字符；
    regex = re.compile(u"[`~!@#$%^&*()+=|{}':',\\[\\].<>/?~！@#￥%……& amp;*（）——+|{}【】‘；：”“’。，、？|-]")
    #判断是否包含英文；
    re_english = re.compile(u'[\u4e00-\u9fa5]', re.UNICODE)
    # if re.search(re_english, ky_find) is None:  # 判断字符是否为字母；
    #     print('\n【%s】不是中文，删除' % (ky_find))
    keyword = ky[0]
    keyword_rank = ky[1]
    keyword_change = ky[2]
    keyword_hot = ky[3]
    keyword_result = ky[4]

    if bool(re.findall(regex, str(ky[0]))) == True:
        #print('【%s】行【%s】包含特殊字符' %(x + 1, ky[0]))
        pass
    else:
        # print('【%s】行【%s】不包含特殊字符' %(x + 1, ky[0]))

        if len(str(ky[0])) <= 6:

            # 是否要英文，要则注释
            # if re.search(re_english, str(ky[0])) is None:
            #     pass
            # else:

            keyword_len = len(keyword)  # 计算字符串长度

            if keyword_len <= 6:

                try:
                    keyword_all_num = len(df[df['关键词'].str.contains(keyword)])  #包含;
                except:
                    keyword_all_num = ''

                pd.DataFrame({
                    '关键词': [keyword],
                    '排名': [keyword_rank],
                    '指数': [keyword_hot],
                    '搜索结果数': [keyword_result],
                    '扩展性': [keyword_all_num],
                    '长度': [keyword_len]
                }).to_csv(
                    '~/Downloads/%s_关键词扩展性计算.csv' %(datetime.date.today()), index=False, encoding='utf-8-sig', mode='a'
                )
                print('\n第【%s】行【%s】关键词被包含次数为【%s】次，插入CSV成功。。。' % (x + 1, keyword, keyword_all_num))