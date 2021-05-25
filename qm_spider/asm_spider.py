from qm_spider import *


# 封装获取消耗情况的脚本；
class Get_ASM_Consume:
    def __init__(self, accountName, accountPwd, X_Apple_Widget_Key='a01459d797984726ee0914a7097e53fad42b70e1f08d09294d14523a1d4f61e1', file_name='ASM-可用余额存取表.xlsx', file_path='./', push_url=push_token):
        self.accountName = accountName
        self.accountPwd = accountPwd
        self.X_Apple_Widget_Key = X_Apple_Widget_Key
        self.today_date = datetime.date.today()
        self.one_day = datetime.timedelta(days=1)
        self.yesterday_date = self.today_date - self.one_day
        self.file_name = file_name
        self.file_path = file_path if file_path[-1]=='/' else file_path+'/'
        self.yes_file_path = '%s%s_%s' %(self.file_path, self.yesterday_date, self.file_name)
        self.yes_yes_file_path = '%s%s_%s' %(self.file_path, self.yesterday_date-one_day, self.file_name)
        self.today_file_path = '%s%s_%s' %(self.file_path, self.today_date, self.file_name)
        self.push_url = push_url

    def clear_trash_file(self):
        # 开始执行文件清理；
        now_file_list = os.listdir(self.file_path)
        for now_file_name in now_file_list:
            if '.xlsx' in now_file_name and 'ASM-可用余额存取表' in now_file_name:
                if str(self.today_date) in now_file_name or str(self.today_date - self.one_day) in now_file_name or str(self.yesterday_date - self.one_day) in now_file_name:
                    pass
                else:
                    print(now_file_name, '将被删除')
                    # 如果不是今天或者昨天的日报文件，就删除；
                    os.system('rm -rf %s/%s' % (self.file_path, now_file_name))

    def asm_login(self):
        # 模拟网页请求；
        url = 'https://idmsa.apple.com/appleauth/auth/signin?isRememberMeEnabled=true'
        payload = {
            "accountName": self.accountName,
            "rememberMe": True,
            "password": self.accountPwd
        }
        headers = {
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'X-Apple-Widget-Key': self.X_Apple_Widget_Key,
            'X-Requested-With': 'XMLHttpRequest',
            'Content-Type': 'application/json',
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.87 Safari/537.36"
        }
        res = session.post(url, headers=headers, data=json.dumps(payload), verify=False)
        if res.status_code == 412:
            print('...模拟启动浏览器成功...')
            X_Apple_Session_Token = res.headers['X-Apple-Repair-Session-Token']
            X_Apple_ID_Session_Id = res.headers['X-Apple-ID-Session-Id']
            scnt = res.headers['scnt']

            # 模拟登陆；
            url = 'https://appleid.apple.com/widget/account/repair?trustedWidgetDomain=https%3A%2F%2Fidmsa.apple.com&widgetKey=a01459d797984726ee0914a7097e53fad42b70e1f08d09294d14523a1d4f61e1&rv=1&language=zh_CN_CHN'
            headers = {
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
                'Connection': 'keep-alive',
                'Host': 'appleid.apple.com',
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.3'
            }
            res = session.get(url, headers=headers, verify=False)
            if res.status_code == 200:
                print('...模拟访问网页成功...')

                # 开始模拟登陆；
                url = 'https://idmsa.apple.com/appleauth/auth/repair/complete'
                headers = {
                    'Accept': 'application/json;charset=utf-8',
                    'Connection': 'keep-alive',
                    'Content-Type': 'application/json',
                    'Host': 'idmsa.apple.com',
                    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36',
                    'scnt': scnt,
                    'X-Apple-Repair-Session-Token': X_Apple_Session_Token,
                    'X-Apple-ID-Session-Id': X_Apple_ID_Session_Id,
                    ''
                    'X-Apple-Widget-Key': self.X_Apple_Widget_Key,
                    'X-Requested-With': 'XMLHttpRequest'
                }
                res = session.post(url, headers=headers, verify=False)
                print('...模拟登陆网页成功...')
                if res.status_code == 204:
                    url = 'https://app.searchads.apple.com/cm/api/v1/startup'
                    headers = {
                        'Accept': 'application/json, text/javascript, */*; q=0.01',
                        'Connection': 'keep-alive',
                        'Content-Type': 'application/json',
                        'Host': 'app.searchads.apple.com',
                        'Referer': 'https://appleid.apple.com/widget/account/repair?trustedWidgetDomain=https%3A%2F%2Fidmsa.apple.com&widgetKey=a01459d797984726ee0914a7097e53fad42b70e1f08d09294d14523a1d4f61e1&rv=1&language=zh_CN_CHN',
                        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36',
                        'X-Requested-With': 'XMLHttpRequest'
                    }
                    res = session.get(url, headers=headers, verify=False)
                    self.defOrg_id = res.json()['data']['userDetails']['defOrg']
                    if res.status_code == 200:
                        self.res_token_cm = session.cookies.get_dict()['XSRF-TOKEN-CM']
                        print('...正在获取Token...')
                        print('当前Token：%s' %(self.res_token_cm))
                        return self.res_token_cm
                    else:
                        print('...获取Token失败...请重试...')
                        return '当前接口请求异常: %s' % (url)
                else:
                    print('...模拟登陆网页失败...请重试...')
                    return '当前接口请求异常: %s' % (url)
            else:
                print('...模拟访问网页失败...请重试...')
                return '当前接口请求异常: %s' %(url)
        else:
            print('...模拟启动浏览器失败...请重试...')
            return '当前接口请求异常: %s' %(url)

    def asm_credits(self):
        url = 'https://app.searchads.apple.com/cm/api/v1/orgs/%s/locdetails' %(self.defOrg_id)
        headers = {
            'Host': 'app.searchads.apple.com',
            'Connection': 'keep-alive',
            'Content-Type': 'application/json;charset=UTF-8',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36',
            'X-XSRF-TOKEN-CM': self.res_token_cm
        }
        res = session.get(url, headers=headers, verify=False, timeout=5)
        return res.json()['data']['availableCredit'][0]['availableAmount']['value']

    def asm_consume(self):
        push_text_list = []  # 汇总推送的内容；
        df_new = pd.DataFrame({})  # 创建个当天的；
        res_status = self.asm_login()
        headers = {
            'Host': 'app.searchads.apple.com',
            'Connection': 'keep-alive',
            'Content-Type': 'application/json;charset=UTF-8',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36',
            'X-XSRF-TOKEN-CM': self.res_token_cm
        }
        if '异常' not in res_status:
            os.system('rm -rf %s' % (self.today_file_path))
            try:
                df = pd.read_excel('%s' %(self.yes_file_path))
            except:
                DingDing_Push('ASM异常推送告警', '### ASM余额监控-异常告警提示\n\n**提示内容**：当前读取前1日存储账单记录异常，已再向前1日读取存储，数据或出现偏移，请注意确认！', push_url=self.push_url).app_args_markdown_push()
                df = pd.read_excel('%s' % (self.yes_yes_file_path))

            # 正式开始执行；
            run_num = 1
            offset_num = 0
            while True:
                url = "https://app.searchads.apple.com/cm/api/v4/budgetorders/find"
                # payload = {
                #     "selector":
                #         {
                #             "conditions": [],
                #             "pagination":
                #                 {
                #                     "offset": offset_num,
                #                     "limit": 50
                #                 },
                #             "orderBy":
                #                 [
                #                     {
                #                         "field": "startDate",
                #                         "sortOrder": "ASCENDING"
                #                     }
                #                 ]
                #         },
                #     "budgetOrderType": "owned",
                #     "addCampaignGroupAssignments": True
                # }
                payload = {
                    "selector": {
                        "conditions": [
                            {
                                "field": "status",
                                "operator": "IN",
                                "values": [
                                    "ACTIVE",
                                    "EXHAUSTED"
                                ]
                            }
                        ],
                        "pagination": {
                            "offset": offset_num,
                            "limit": 50
                        },
                        "orderBy": [
                            {
                                "field": "startDate",
                                "sortOrder": "ASCENDING"
                            }
                        ]
                    },
                    "budgetOrderType": "owned",
                    "addCampaignGroupAssignments": True
                }
                res = session.post(url, headers=headers, data=json.dumps(payload), verify=False)
                if len(res.json()['data']) > 0:
                    for i in res.json()['data']:
                        # 开始获取账户对应的数据；
                        budget_order_id = i['bo']['id']
                        advertiser_or_product = i['bo']['clientName']  # 公司名称
                        budget_name = i['bo']['name']  # 备注名称
                        if budget_name[:7] != '1317320':
                            print('获取第【%s】页【%s】的相关数据...' % (int(offset_num / 50 + 1), budget_order_id))

                            # 开始请求详细数据；
                            url = 'https://app.searchads.apple.com/cm/api/v4/budgetorders/%s' % (budget_order_id)
                            res = session.get(url, headers=headers, verify=False)  # 获取内页数据；
                            budget_order_status = res.json()['data']['bo']['status']  # 状态
                            try:
                                spent_value = res.json()['data']['spent']['value']
                            except:
                                spent_value = 0
                            # 判断是否要计算余额；
                            if int(spent_value) != 0:
                                order_number = res.json()['data']['bo']['orderNumber']
                                start_date = res.json()['data']['bo']['startDate'][:10]  # 开始时间
                                end_date = res.json()['data']['bo']['endDate']  # 结束时间
                                if str(end_date) == 'None':
                                    end_date = '当前'
                                else:
                                    end_date = end_date[:10]
                                budget_amount = int(res.json()['data']['bo']['budget']['value'])  # 总消耗限制金额
                                campaign_group_list = []
                                for com_x in res.json()['data']['linkedOrgs']:
                                    campaign_group_list.append(com_x['orgName'])
                                campaign_group = '、'.join(campaign_group_list)  # 公司组名

                                # 下方获取字段坑存在空值的情况，因前一日获取数据时无导致，可取0；
                                # print(budget_order_id, int(budget_order_id), len(str(budget_order_id)))
                                try:
                                    yes_spent_value = float(df[(df['账单ID'] == int(budget_order_id))].values[0][2])

                                    # 开始计算；
                                    if float(spent_value) != yes_spent_value:
                                        yes_run_num = round(spent_value - yes_spent_value, 2)  # 昨日消耗的；
                                        now_yue_num = budget_amount - spent_value  # 限制消耗金额减去当前总消耗
                                        now_yue_days = int(math.floor(now_yue_num / yes_run_num))  # 预估还可消耗天数；
                                    else:
                                        # 如果今日昨日一样，代表没消耗的，就可以跳过；
                                        yes_run_num = '空'
                                        now_yue_days = 10000

                                    if now_yue_days <= 7:  # 小于等于7则推送，否则不管；
                                        print('当前【%s】符合，加入待推送列表...' % (budget_order_id))
                                        push_title = "【%s】%s" % (advertiser_or_product, 'ASM账户余额推送'),
                                        push_text = "**当前日期**：%s\n\n**账户备注名**：%s(%s)\n\n**账户公司名**：%s\n\n**昨日消耗**：%s\n\n**累计消耗**：%s\n\n**限制消耗金额**：%s\n\n**预估剩余消耗天数**：**%s天**\n\n**时间区间**：%s至%s\n\n**账号组别**：%s\n\n " % (self.today_date, budget_name, budget_order_status, advertiser_or_product, yes_run_num, spent_value, budget_amount, now_yue_days, start_date, end_date, campaign_group)
                                        # DingDing_Push(push_title, *[push_text], push_url=self.push_url).app_args_markdown_push()
                                        push_text_list.append([push_title, push_text])
                                        # 推送成功，进行下一步；
                                except:
                                    print('当前【%s】获取昨日消耗异常，先存此条数据不推送此条' %(budget_name))
                            else:
                                pass

                            # 存为实例Excel；
                            df_new = df_new.append(pd.DataFrame({
                                '账单ID': [int(budget_order_id)],
                                '日期': [str(self.today_date)],
                                '消耗总额': [spent_value]
                            }))

                        # 运行次数加 1；
                        run_num += 1
                    # 延迟 5 分钟继续；
                    offset_num += 50
                else:
                    print('本次获取完毕，跳出循环')
                    break

            # 存为实例Excel；
            today_credits_num = self.asm_credits()
            print('当前账户可用信用额度：', today_credits_num)
            df_new = df_new.append(pd.DataFrame({
                '账单ID': [int(self.defOrg_id)],
                '日期': [str(self.today_date)],
                '消耗总额': [today_credits_num]
            }))
            # 开始计算；
            yes_credits_num  = float(df[(df['账单ID'] == int(self.defOrg_id))].values[0][2])
            if float(today_credits_num) != yes_credits_num:
                yes_run_num = round(yes_credits_num - today_credits_num, 2)  # 昨日消耗的；
                if yes_run_num < 0: # 如果是负值说明充值了额度(因为前面已经判断了不等于，所以这里不会有0)；
                    now_yue_days = '昨日已续额度，可用：∞'
                else:
                    # now_yue_num = budget_amount - spent_value  # 限制消耗金额减去当前总消耗
                    now_yue_days = math.floor(float(today_credits_num) / yes_run_num)  # 预估还可消耗天数；
            else:
                # 如果今日昨日一样，代表没消耗的，就可以跳过；
                yes_run_num = '空'
                now_yue_days = '∞∞∞'
            # 加入推送列表；
            push_title = '七麦科技-ASM账户总可用信用额度监控'
            asm_link = 'https://app.searchads.apple.com/cm/app/settings/billing/loc'
            push_text = "### %s-七麦科技-ASM信用额度提醒 \n\n**今日可用的信用额度**：[%s(USD)](%s)\n\n**昨日可用的信用额度**：%s(USD)\n\n**昨日消耗信用额度**：%s(USD)\n\n**预估剩余可用天数**：**%s天**" % (self.today_date, round(today_credits_num, 2), asm_link, round(yes_credits_num, 2), yes_run_num, now_yue_days)
            push_text_list.append([push_title, push_text])
            # 完毕后读取当前数据进行去重，
            df_new.drop_duplicates(['账单ID', '日期', '消耗总额'], keep='last', inplace=True)

            # # 成功推送；
            # push_title = '%s_余额监控任务' %(self.today_date)
            # DingDing_Push(push_title).status_push()

            # 存储；
            df_new.to_excel(
                self.today_file_path, index=False, encoding='utf-8-sig'
            )

            # 开始推送；
            print('文件已存储完毕，开始推送')
            for push_info in push_text_list:
                DingDing_Push(push_info[0], *[push_info[1]], push_url=self.push_url).app_args_markdown_push()
                time.sleep(5)

        else:
            # 失败推送；
            push_title = '%s_ASM余额监控任务' %(self.today_date)
            dingding_push = DingDing_Push(push_title)
            dingding_push.push_status = '登陆失败，无法正常获取token'
            dingding_push.status_push()
            return '...登陆异常，请重试...'

# 封装获取账单的脚本；
class Get_ASM_Bill(Get_ASM_Consume):
    def __init__(self, accountName, accountPwd, start_date, end_date):
        Get_ASM_Consume.__init__(self, accountName, accountPwd)
        self.start_date, self.end_date = Qimai_Outside_Tool(*[start_date, end_date]).get_month_time()
        self.file_path = self.file_path if self.file_path[-1] == '/' else self.file_path + '/'

    def asm_bill(self):
        self.asm_login()
        self.file_path = self.file_path if self.file_path[-1]=='/' else self.file_path+'/'
        run_num = 1
        offset_num = 0
        df = pd.DataFrame({})
        while True:
            url = 'https://app.searchads.apple.com/cm/api/v1/locinvoicesummary'
            headers = {
                'Host': 'app.searchads.apple.com',
                'Connection': 'keep-alive',
                'Content-Type': 'application/json;charset=UTF-8',
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36',
                'X-XSRF-TOKEN-CM': self.res_token_cm
            }
            payload = {"startDate":"%s" %(self.start_date),"endDate":"%s" %(self.end_date),"selector":{"orderBy":[{"field":"billingPeriod","sortOrder":1}],"pagination":{"offset":offset_num,"limit":50}}}
            res = session.post(url, data=json.dumps(payload), headers=headers, verify=False)
            if len(res.json()['data']) > 0:
                for bill_info in res.json()['data']:
                    orgId = bill_info['orgId']
                    amount = bill_info['amount']['amount']
                    currencyCode = bill_info['amount']['currencyCode']
                    orderNumber = bill_info['orderNumber']
                    budgetOrderName = bill_info['budgetOrderName']
                    invoiceSummaryDate = bill_info['invoiceSummaryDate']
                    paymentDueDate = bill_info['paymentDueDate']
                    downloadDate = bill_info['downloadDate']
                    summaryType = bill_info['summaryType']
                    advertiser = bill_info['advertiser']
                    paymentReferenceId = bill_info['paymentReferenceId']
                    billingPeriod = bill_info['billingPeriod']
                    print('获取第【%s】页总第【%s】条【%s】的相关数据...' % (int(offset_num / 10 + 1), run_num, advertiser))

                    df = df.append(pd.DataFrame({
                        'billingPeriod': [billingPeriod],
                        'paymentReferenceId': [paymentReferenceId],
                        'orgId': [orgId],
                        'orderNumber': [orderNumber],
                        'advertiser': [advertiser],
                        'budgetOrderName': [budgetOrderName],
                        'amount': [amount],
                        'currencyCode': [currencyCode],
                        'invoiceSummaryDate': [invoiceSummaryDate],
                        'paymentDueDate': [paymentDueDate],
                        'downloadDate': [downloadDate],
                        'summaryType': [summaryType]
                    }))

                    # 运行次数加 1；
                    run_num += 1
                # 延迟 5 分钟继续；
                offset_num += 10

            else:
                print('...本次获取完毕，跳出循环...')
                break
        # 存储；
        self.file_name = self.file_name if self.file_name[-1]=='x' else self.file_name+'.xlsx'
        now_file_name_path = '%s%s_%s' %(self.file_path, self.end_date, self.file_name)
        # df.to_excel('%s' %(now_file_name_path), index=False, encoding='utf-8-sig')
        return df, now_file_name_path
