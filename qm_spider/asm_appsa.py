"""
@FileName：asm_appsa.py\n
@Description：\n
@Author：道长\n
@Time：2021/8/19 16:29\n
@Department：运营部\n
@Website：www.geekaso.com.com\n
@Copyright：©2019-2021 七麦数据
"""

from qm_spider import *


class AppSA_Get_Info_List:
    """
        * Get，主要用于获取信息；
    """
    def __init__(self, start_date='', end_date=''):
        self.start_date = start_date
        self.end_date = end_date

    def get_group_list(self, search=''):
        """
            * 获取账号下广告系列组列表；
        """
        url = 'https://api.appsa.com/asaplanIndex/getGroupList'
        payload = 'sdate=%s&edate=%s&search=%s' %(self.start_date, self.end_date, search)
        res = session.post(url, data=payload, headers=headers_post)
        return res.json()

    def get_campaign_list(self, group_id):
        """
            * 获取广告系列组下广告系列列表；
        """
        url = 'https://api.appsa.com/asaplanNew/campaignList?group_id=%s&status=&storefront=0&campaign_name_or_id=&display_status=1&sdate=%s&edate=%s&type=0&app_id=0'%(group_id, self.start_date, self.end_date)
        res = session.get(url, headers=headers)
        return res.json()

    def get_adgroup_list(self, campaign_id, group_id):
        """
            * 获取广告系列下广告组列表；
        """
        url = 'https://api.appsa.com/asaplanNew/campaignAds?campaign_id=%s&group_id=%s&app_id=0&status=&delete=0&sdate=%s&edate=%s&ad_group_name_or_id=' %(campaign_id, group_id, self.start_date, self.end_date)
        res = session.get(url, headers=headers)
        return res.json()

    def get_adkeyword_list(self, group_id, campaign_id=0, app_id='', ad_group_id='', match_type='', delete=0, status='', search=''):
        """
            * 获取广告下关键词列表；
            * 默认获取广告系列组下关键词列表；
            * 传广告系列ID、及广告组ID均可，往下一级获取必须带上上一级的；
        """
        url = 'https://api.appsa.com/asaplanNew/campaignKeywords'
        payload='group_id=%s&app_id=%s&campaign_id=%s&ad_group_id=%s&match_type=%s&delete=%s&status=%s&search=%s&sdate=%s&edate=%s' %(group_id, app_id, campaign_id, ad_group_id, match_type, delete, status, search, self.start_date, self.end_date)
        res = session.post(url, data=payload, headers=headers_post)
        return res.json()
