from urllib import parse
import requests
import hashlib
import json

'''
获取经纬度api
'''


class GeoAPI:
    # baidu开发者中心申请
    _ak = 'bi8EogV4GhUx1nFBKhU8UGG6dbuTUXW0'#'vtNnuAcqNStCdYkakK4LcfndgcrRVvAb' #'2HlEGjO3Y2aUWyPOB1vjcOhIoaAOUu9t'
    _sk = 'GtyFQRV62dmuvdeTqIkifowkCjzDEWge'#'V4UXQe95De6hrQF5ziUsM2AdFpBcWtN4' #'VL9BwNK1yo0XKoChy7zFrqMNQyU0ZifC'

    # 根据地址向百度api发起请求获取返回结果的链接
    @staticmethod
    def get_url(address):
        queryStr = '/geocoder/v2/?address=%s&output=json&ak=' % address + GeoAPI._ak
        # 对queryStr进行转码，safe内的保留字符不转换
        encodedStr = parse.quote(queryStr, safe="/:=&?#+!$,;'@()*[]")
        # 在最后直接追加上yoursk
        rawStr = encodedStr + GeoAPI._sk
        # 计算sn
        sn = (hashlib.md5(parse.quote_plus(rawStr).encode("utf8")).hexdigest())
        # 由于URL里面含有中文，所以需要用parse.quote进行处理，然后返回最终可调用的url
        url = parse.quote("http://api.map.baidu.com" + queryStr + "&sn=" + sn, safe="/:=&?#+!$,;'@()*[]")
        return url

    # 获取返回的经纬度信息
    @staticmethod
    def get_geowind(address):
        html = requests.get(GeoAPI.get_url(address))
        geo_info = json.loads(html.text)
        return geo_info

    # 得到经纬度坐标并返回一个列表
    @staticmethod
    def get_lng_lat(address):
        geo_info = GeoAPI.get_geowind(address)
        # print(geo_info)
        lng = geo_info['result']['location']['lng']
        lat = geo_info['result']['location']['lat']
        return lng, lat

    @staticmethod
    def get_lna_lats(address):
        for a in range(len(address['Table1']) - 1, -1, -1):
            geo_info = GeoAPI.get_geowind(address['Table1'][a]['addressDetail'])
            if geo_info['status'] == 0:
                address['Table1'][a]['lnalats'] = \
                    GeoAPI.get_lng_lat(address['Table1'][a]['addressDetail'])
            else:
                print('移除该数据')
                address['Table1'].pop(a)
        return address
