import json
import re
import scrapy
from scrapy.http import HtmlResponse
from instaparser.items import InstaparserItem
from urllib.parse import urlencode
from copy import deepcopy

class InstaSpider(scrapy.Spider):
    name = 'instagram'
    allowed_domains = ['instagram.com']
    start_urls = ['https://www.instagram.com/']
    inst_login_link = 'https://www.instagram.com/accounts/login/ajax/'
    inst_login = 'xefolo4154'
    inst_pwd = '#PWD_INSTAGRAM_BROWSER:10:1651255454:AR5QAJpyn9GChsGRF89+mojr6ezQkD92XQs1PQTAH01HrXU471coU09d4NitZmrs0jTQy4vKLPgXTdh3hw1z+CWq/XFvrDX6hIFbo55ZMS05/2ZJaK+aQ8n6efgpzgSxmmj5FBm9pCtF2By+YnZG'
    parse_user_list = ['techskills_2022', 'crossfit_kgn']
    inst_graphql_link = 'https://www.instagram.com/graphql/query/?'
    insta_api_url = 'https://i.instagram.com/api/v1/'

    def parse(self, response: HtmlResponse):
        csrf = self.fetch_csrf_token(response.text)
        yield scrapy.FormRequest(
            self.inst_login_link,
            method='POST',
            callback=self.login,
            formdata={'username': self.inst_login, 'enc_password': self.inst_pwd},
            headers={'X-CSRFToken': csrf}
        )

    def login(self, response: HtmlResponse):
        j_body = response.json()
        if j_body['authenticated']:
            for parse_user in self.parse_user_list:
                yield response.follow(
                   f'/{parse_user}',
                   callback=self.user_data_parse,
                   cb_kwargs={'username':parse_user}
                  )
    def user_data_parse(self, response: HtmlResponse, username):
        user_id = self.fetch_user_id(response.text, username)
        variables = {"count": 12}
        user_status = 'followers'
        for user_status in ('following', 'followers'):
            get_follow_user_url = f'{self.insta_api_url}friendships/{user_id}/{user_status}/?{urlencode(variables)}'
            yield response.follow(get_follow_user_url,
                                  cb_kwargs={'username': username,
                                             'user_id': user_id,
                                             'variables': deepcopy(variables),
                                             'user_status': user_status},
                                  callback=self.user_data_parse_follow,
                                  headers={'User-Agent': 'Instagram 155.0.0.37.107'})


    def user_data_parse_follow(self, response: HtmlResponse, username, user_id, variables, user_status):
        j_data = response.json()
        if j_data.get('next_max_id'):
            variables['max_id'] = j_data.get('next_max_id')
            get_following_users_url = f'{self.insta_api_url}friendships/{user_id}/{user_status}/?{urlencode(variables)}'
            yield response.follow(get_following_users_url,
                                  callback=self.user_data_parse_follow,
                                  cb_kwargs={'username': username,
                                             'user_id': user_id,
                                             'variables': deepcopy(variables),
                                             'user_status': user_status},
                                  headers={'User-Agent': 'Instagram 155.0.0.37.107'})


        for user in j_data.get('users'):
            item = InstaparserItem(
                username=user.get('username'),
                user_status=user_status,
                user_id=user.get('pk'),
                photo=user.get('profile_pic_url'),
                from_username=username
            )
            yield item





    def fetch_csrf_token(self, text):
        """ Get csrf-token for auth """
        matched = re.search('\"csrf_token\":\"\\w+\"', text).group()
        return matched.split(':').pop().replace(r'"', '')

    def fetch_user_id(self, text, username):
        try:
            matched = re.search(
                '{\"id\":\"\\d+\",\"username\":\"%s\"}' % username, text
            ).group()
            return json.loads(matched).get('id')
        except:
            return re.findall('\"id\":\"\\d+\"', text)[-1].split('"')[-2]





















































