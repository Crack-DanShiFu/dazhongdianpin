import os
import random

import xlwt as xlwt
import getGew
import requests
import json


def get_info():
    url = 'https://www.dianping.com/mylist/ajax/shoprank?rankId=576fcc182382940f30db74d9b29df218d97945289578b7557a191d6c125161e7'

    USER_AGENT_LIST = [
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",
        "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6",
        "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5"]
    headers = {
        'User-Agent': '{0}'.format(random.sample(USER_AGENT_LIST, 1)[0])}
    # headers = {
    #     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'
    # }
    html = requests.get(url, headers=headers)
    jsonInfo = json.loads(html.text)['shopBeans']
    if os.path.exists('南通市.xls'):
        wbk = xlwt.Workbook()
        sheet = wbk.add_sheet('南通市')
    else:
        wbk = xlwt.Workbook()
        sheet = wbk.add_sheet('南通市')
        wbk.save('南通市.xls')

    data1 = ['shopName', 'branchName', 'mainRegionName', 'address', 'mainCategoryName', 'refinedScore1',
             'refinedScore2', 'refinedScore3', 'avgPrice']

    for key, val in enumerate(data1):
        sheet.write(0, key, val)
    sheet.write(0, 9, "lng_lat")
    for key, val in enumerate(jsonInfo):
        for key1, val1 in enumerate(data1):
            sheet.write(key + 1, key1, val[data1[key1]])
        sheet.write(key + 1, 9, str(getGew.GeoAPI.get_lng_lat('南通市' + val['address'])))
        # print(j['shopName'], j['branchName'], j['mainRegionName'], j['address'], j['mainCategoryName'], j['refinedScore1'],
        #       j['refinedScore2'],
        #       j['refinedScore3'], j['avgPrice'], getGew.GeoAPI.get_lng_lat('南通市' + j['address']))
    wbk.save('南通市.xls')


if __name__ == '__main__':
    get_info()
