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

@qm_auth_check  # 登录检查；
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

# 分词算法汇总；
@qm_auth_check  # 登录检查；
class Jieba_Word_algorithm:
    def __init__(self, keyword_list):
        self.keyword_list = keyword_list

    def jieba_keyword_search(self):
        """
            * 普通的jieba分词算法，默认精确模式：
            * 当前使用的搜索引擎模式；
        """
        self.word_cutSearch_list = []
        for app_title in self.keyword_list:
            seg_list = jieba.cut_for_search(app_title)  # 默认是精确模式
            for ky_word in seg_list:
                # 循环添加关键词到列表，待组词使用；
                self.word_cutSearch_list.append(ky_word)
        return self.word_cutSearch_list

    def jieba_keyword_TF(self):
        """
            * 升阶版分词算法，主要是拆分出有用的词：
            * 又名jieba的TF分词算法；
        """
        self.word_jiebaTF_list = []
        for app_title in self.keyword_list:
            seg_list = jieba.analyse.extract_tags(app_title)
            for ky_word in seg_list:
                # 循环添加关键词到列表，待组词使用；
                self.word_jiebaTF_list.append(ky_word)
        return self.word_jiebaTF_list

    def class_generate_words(self):
        """
            * 组词算法，自动组成100字符的关键词组
        """
        now_keyword_list = []
        word_itc = ''
        while len(word_itc) < 100:
            # 判断是否有重复项，如果有就跳过；
            last_word_num = 100 - len(word_itc)  # 计算当前剩余字符位置；
            if last_word_num == 3:
                while True:
                    now_word = random.choice(self.keyword_list)
                    if len(now_word) == 3 and now_word[0] != word_itc[-1] and now_word not in now_keyword_list:
                        now_keyword_list.append(now_word)
                        self.keyword_list.remove(now_word)  # 添加过的去一下重；
                        word_itc = word_itc + now_word
                        break
            elif last_word_num == 2:
                while True:
                    now_word = random.choice(self.keyword_list)
                    if len(now_word) == 2 and now_word[0] != word_itc[-1] and now_word not in now_keyword_list:
                        now_keyword_list.append(now_word)
                        self.keyword_list.remove(now_word)  # 添加过的去一下重；
                        word_itc = word_itc + now_word
                        break
            elif last_word_num == 1:
                while True:
                    now_word = random.choice(self.keyword_list)
                    if len(now_word) == 1 and now_word[0] != word_itc[-1] and now_word not in now_keyword_list:
                        now_keyword_list.append(now_word)
                        self.keyword_list.remove(now_word)  # 添加过的去一下重；
                        word_itc = word_itc + now_word
                        break
            else:
                # 剩余字符多则随意抽取；
                now_word = random.choice(self.keyword_list)
                if now_word not in now_keyword_list and len(now_word)>1:  # 存在就跳过；
                    for i in range(len(now_word)-1, 0, -1):  # 此处算法旨在缩减AB、BC关键词为ABC组合
                        # print(word_itc, now_word, i, -i)
                        if len(word_itc)==0:
                            word_itc += now_word
                            break
                        elif now_word[:i] == word_itc[-i:]:
                            word_itc += now_word[i:]
                            break
                    else:
                        # 上面规则不符合则继续检测是否出现ABCD、EBCD类型需要合并为AEBCD类型的；
                        run_is_bool = False
                        for cut_x in range(2, len(now_word)-1):
                            cut_word_x = now_word[cut_x:]
                            if run_is_bool == False:
                                for cut_i in range(len(word_itc)-(len(cut_word_x)-1)):
                                    cut_word_i = word_itc[cut_i:cut_i+len(cut_word_x)]
                                    if cut_word_x == cut_word_i:
                                        # 相等说明出现了重叠情况，在指定位置插入即可；
                                        nPos = word_itc.find(cut_word_i)
                                        # print(cut_word_x, '第一种匹配', word_itc[:nPos], now_word[:cut_x], word_itc[nPos:])
                                        word_itc = word_itc[:nPos] + now_word[:cut_x] + word_itc[nPos:]
                                        run_is_bool = True
                                        break
                            else:
                                break
                        else:
                            # 上面规则不符合则继续检测是否出现ABCD、EFCD类型需要合并为ABEFCD类型的；
                            for cut_x in range(2, len(now_word) - 1):
                                cut_word_x = now_word[:cut_x]
                                if run_is_bool == False:
                                    for cut_i in range(len(word_itc) - (len(cut_word_x) - 1)):
                                        cut_word_i = word_itc[cut_i:cut_i + len(cut_word_x)]
                                        if cut_word_x == cut_word_i:
                                            # 相等说明出现了重叠情况，在指定位置插入即可；
                                            nPos = word_itc.find(cut_word_i)
                                            # print(cut_word_x, '第二种匹配', word_itc[:nPos+len(cut_word_x)], now_word[cut_x:], word_itc[nPos+len(cut_word_x):])
                                            word_itc = word_itc[:nPos+len(cut_word_x)] + now_word[cut_x:] + word_itc[nPos+len(cut_word_x):]
                                            run_is_bool = True
                                            break
                                else:
                                    break
                            else:
                                word_itc += now_word
                    now_keyword_list.append(now_word)
                    self.keyword_list.remove(now_word)  # 添加过的去一下重；
        # 运行一遍完毕后，清空已添加过的词的列表；
        # del now_keyword_list
        return word_itc

    # 拆词组词算法；
    def class_word_new(self, word_itc, now_word):
        """
            * 精细化拆词组词算法，尚未完成：
        """
        if word_itc[-1] == now_word[0]:
            # 判断如果当前100字符没组合完，继续组合时发现下个词头部与当前尾部字相同，则拼接；
            word_itc = word_itc + now_word  # 拼接

# 关键词搜索数据抓取版汇总；
@qm_auth_check  # 登录检查；
class Get_Search_AppTitle:
    def __init__(self, keyword):
        self.keyword = keyword

    def get_asodata_chandashi(self):
        """
            * 取源数据用于分词取词，从禅大师获取：
        """
        url = 'https://www.chandashi.com/search/index?keyword=%s&type=store&country=cn' % (self.keyword)
        res = requests.get(url, headers=headers)
        res_text = BeautifulSoup(res.text, 'html.parser')
        ky_search_list = []
        print('\n\n📣📣📣正在根据【%s】扩充相关关键词。。。' % (self.keyword))
        for j, i in enumerate(res_text.find_all(class_='pic')):
            if j <= 4:
                search_ky = i.get('title')  # 获取应用名称；
                # search_appid = re.findall(r"\d+\.?\d*", i.get('href'))[0]  # 获取ID；
                ky_search_list.append(search_ky)
            else:
                break
        return ky_search_list

    def get_asodata_66aso(self):
        """
            * 取源数据用于分词取词，从66ASO获取：
        """
        url = 'http://www.66aso.cn/api/scheme/search?pageSize=50&currentPage=1&key=%s' % (self.keyword)
        ky_search_list = []
        print('\n\n📣📣📣正在根据【%s】扩充相关关键词。。。' % (self.keyword))
        for i in range(3):
            res = requests.get(url, headers=headers)
            len_num = len(res.json()['data'])
            if len_num >= 50:
                for j, app in enumerate(res.json()['data']):
                    if j <= 3:
                        search_ky = app['appName']  # 获取App名称；
                        # search_appid = app['appId']  # 获取ID；
                        ky_search_list.append(search_ky)
                    else:
                        break
                return ky_search_list
            else:
                print('请求的App量级不符合，重新请求')
        else:
            res = requests.get(url, headers=headers)
            for app in res.json()['data']:
                search_ky = app['appName']  # 获取App名称；
                # search_appid = app['appId']  # 获取ID；
                ky_search_list.append(search_ky)
            return ky_search_list

    def get_asodata_qimai(self):
        """
            * 取源数据用于分词取词，从七麦数据获取：
        """
        ky_search_list = []
        keyword_result = Get_Keyword_Info(self.keyword).get_keyword_search()
        print('\n\n📣📣📣正在根据【%s】扩充相关关键词。。。' % (self.keyword))
        app_num = 1
        for app in keyword_result['appList']:
            if app_num <= 3 and app['kind'] == 'software':
                search_ky = app['appInfo']['appName']  # 获取App名称；
                # search_appid = app['appInfo']['appId']  #获取ID；
                subtitle = app['appInfo']['subtitle']  # 获取副标题；
                ky_search_list.append(search_ky)
                if subtitle is None:
                    pass
                else:
                    ky_search_list.append(subtitle)
            else:
                break
        # 返回数据
        return ky_search_list

    # 酷传ASO，检测热度+结果数；
    def get_hot_jieguo_66aso(self):
        """
            * 检测关键词热度、搜索结果数判断词价值，从66aso取数：
        """
        if '%' not in self.keyword:
            url = 'https://ios.kuchuan.com/keywordhot?keyword=%s&iosVersion=12' % (self.keyword)
            res = requests.get(url, headers=headers)
            return [res.json()['hot'], res.json()['results']]
        else:
            return ['0', '0']

    def get_hot_jieguo_qimai(self):
        """
            * 检测关键词热度、搜索结果数判断词价值，从七麦数据取数：
        """
        if '%' not in self.keyword:
            url = 'https://api.qimai.cn/search/getWordInfo?country=cn&search=%s' % (self.keyword)
            res = requests.get(url, headers=headers)
            return [res.json()['wordInfo']['hints'], res.json()['wordInfo']['search_no']]
        else:
            return ['0', '0']

# 生成100字符的主程序；
@qm_auth_check  # 登录检查；
class Generate_100_Keyword:
    def __init__(self, user_ky_list):
        self.user_ky_list = user_ky_list
        self.spare_keyword_list = []

    def generate_correlation_main(self, range_num=7):
        for keyword in self.user_ky_list:
            keyword_info_list = Get_Keyword_Info(keyword).get_keyword_extend(max_index=200, orderBy='relate', order='desc')
            for info_list in keyword_info_list:
                for keyword_info in info_list['extendList']['list']:
                    word = keyword_info['word']
                    relate = keyword_info['relate']
                    hints = keyword_info['hints']
                    search_no = keyword_info['search_no']

                    if int(relate) > 50 and int(hints) > 4605 and int(search_no) > 0 and len(word) <= 5:
                        self.spare_keyword_list.append(word)
                        print('当前已匹配【%s】个关键词【%s - %s】，尚未去重' %(len(self.spare_keyword_list), word, hints))

        # 调用组合算法，生成100字符；
        self.spare_keyword_list = list(set(self.spare_keyword_list))
        print('===去重后总计关键词【%s】个===\n' %(len(self.spare_keyword_list)))
        print('========下方为匹配出的关键词覆盖========')
        new_str_list = []
        for i in range(range_num):
            new_str_text = Jieba_Word_algorithm(self.spare_keyword_list).class_generate_words()
            new_str_list.append(new_str_text)
            print(new_str_text)
        return new_str_list

