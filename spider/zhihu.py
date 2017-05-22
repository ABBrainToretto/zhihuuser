# -*- coding: utf-8 -*-
import scrapy
import json
from scrapy import Spider,Request
from zhihuuser.items import ZhihuuserItem


class ZhihuSpider(scrapy.Spider):
    name = "zhihu"
    allowed_domains = ["www.zhihu.com"]

    follows_url = 'https://www.zhihu.com/api/v4/members/{user}/followees?include={include}&amp;offset={offset}&amp;limit={limit}'
    start_user = 'excited-vczh'
    follows_query = 'data[*].answer_count,articles_count,gender,follower_count,is_followed,is_following,badge[?(type=best_answerer)].topics'

    user_url = 'https://www.zhihu.com/api/v4/members/{user}?include={include}'
    user_query = 'locations,employments,gender,educations,business,voteup_count,thanked_Count,follower_count,following_count,cover_url,following_topic_count,following_question_count,following_favlists_count,following_columns_count,avatar_hue,answer_count,articles_count,pins_count,question_count,columns_count,commercial_question_count,favorite_count,favorited_count,logs_count,marked_answers_count,marked_answers_text,message_thread_token,account_status,is_active,is_force_renamed,is_bind_sina,sina_weibo_url,sina_weibo_name,show_sina_weibo,is_blocking,is_blocked,is_following,is_followed,mutual_followees_count,vote_to_count,vote_from_count,thank_to_count,thank_from_count,thanked_count,description,hosted_live_count,participated_live_count,allow_message,industry_category,org_name,org_homepage,badge[?(type=best_answerer)].topics'

    follower_url = 'https://www.zhihu.com/api/v4/members/{user}/followers?include={include}&amp;offset={offset}&amp;limit={limit}'
    follower_query = 'data[*].answer_count,articles_count,gender,follower_count,is_followed,is_following,badge[?(type=best_answerer)].topics'
    
    #从excited-vczh开始请求
    def start_requests(self):
        yield Request(self.user_url.format(user = self.start_user,include = self.user_query),self.parse_user)
        yield Request(self.follows_url.format(user=self.start_user,include=self.follows_query,offset=0,limit=20),self.parse_follows)
        yield Request(self.follower_url.format(user=self.start_user,include=self.follower_query,offset=0,limit=20),self.parse_follower)
    
    #请求用户详情页，并输出给item
    def parse_user(self, response):
        result = json.loads(response.text)
        item = ZhihuuserItem()
        for field in item.fields: #items.fields可获取item的所有fields
            if field in result.keys():
                item[field] = result.get(field)
        yield item
        yield Request(self.follows_url.format(user=result.get('url_token'),include=self.follows_query,offset=0,limit=20),self.parse_follows)
        yield Request(self.follower_url.format(user=result.get('url_token'),include=self.follower_query,offset=0,limit=20),self.parse_follower)
    
    #请求关注的人的列表
    def parse_follows(self,response):
        results = json.loads(response.text)
        if 'data' in results.keys():
            for result in results.get('data'):
                yield Request(self.user_url.format(user=result.get('url_token'),include=self.user_query),self.parse_user)
                if 'paging' in results.keys() and results.get('paging').get('is_end') == False:
                    next_page = results.get('paging').get('next')
                    yield Request(next_page,self.parse_follows)
    
    #请求粉丝的人列表
    def parse_follower(self,response):
        resulty = json.loads(response.text)
        if 'data' in resulty.keys():
            for result in resulty.get('data'):
                yield Request(self.user_url.format(user=result.get('url_token'),include=self.user_query),self.parse_user)
                if 'paging' in resulty.keys() and resulty.get('paging').get('is_end') == False:
                    next_page = resulty.get('paging').get('next')
                    yield Request(next_page,self.parse_follower)
