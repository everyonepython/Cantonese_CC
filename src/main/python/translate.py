# coding=utf-8
import sys
import hashlib
import random
import json
import urllib
from pprint import pprint

import requests


my_appid = ''  # 帳號
my_secretkey = '' # 密鑰


def unicode2zh(string):
    '''Python3 处理网页返回的中文 unicode 字符串。'''
    return string.encode('utf-8').decode('unicode-escape')


def baidu_translate(q, appid, secretkey, from_lang='auto', to_lang='zh'):
    '''
    Return: res_dict
    Success: {"from":"yue",
             "to":"zh",
             "trans_result":[{"src":"Hello大家好呀","dst":"Hello大家好的"},
                            {"src":"唔知大家有冇試過好似我咁","dst":"不知道大家有试过像我这样"}]}
    Fail: {"error_code":"54001","error_msg":"Invalid Sign"}
    '''

    base_url = 'http://api.fanyi.baidu.com/api/trans/vip/translate'
    # Generate Sign.
    salt = str(random.randint(32768, 65536))
    sign = appid + q + salt + secretkey  # 签名字符串
    sign = hashlib.md5(sign.encode('utf8')).hexdigest()  # 哈希签名

    # Join request URL.
    myurl = f'{base_url}?appid={appid}&q={urllib.parse.quote(q)}&from={from_lang}&to={to_lang}&salt={salt}&sign={sign}'

    # Post 請求參數
    # 請求字節大於 2kb 不能用 get，只能用 post 方法。
    # payload = {
    #     'appid': appid,
    #     'q': urllib.parse.quote(q),
    #     'from': from_lang,
    #     'to': to_lang,
    #     'salt': salt,
    #     'sign': sign,
    #     'Content-Type': 'application/x-www-form-urlencoded',
    # }

    # Get translation.
    translation = ''
    try:
        # Get 請求須必須控制在 2kb 以下，約1000個漢字。
        # Post 請求會發生 54001 簽名錯誤。未知原因。
        # response = requests.post(base_url, data=payload)
        response = requests.get(myurl)
    except Exception as e:
        print(response.status_code)
        print(e)
        return

    res = unicode2zh(response.content.decode('utf-8'))  # api 返回结果是 bytes，非字符串。
    res_dict = json.loads(res)  # 將 json 字符串轉為字典。
    return res_dict


if __name__ == '__main__':
    if len(sys.argv) > 1:
        q = sys.argv[1]
        from_lang = 'auto'
    else:
        q = '呢个系一个测试文件，我宜家写紧嘅系广东话。'
        from_lang = 'yue'
    res = baidu_translate(q, my_appid, my_secretkey, from_lang=from_lang)
    print(res)
