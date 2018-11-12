
# coding: utf-8
import re
import requests
from pprint import pprint
import json 
 
 
def main():
    
    url = 'https://kyfw.12306.cn/otn/resources/js/framework/station_name.js?station_version=1.8971'
    # 发送get请求，不判断证书
    response = requests.get(url, verify=False)
    #　使用正则表达式提取所有的站点：汉字和大写代号
    stations = dict(re.findall(u'([\u4e00-\u9fa5]+)\|([A-Z]+)', response.text))
    # 转换成字典就是为了将汉字站点和字母代号分开且有一一对应关系：键－－>值
    #pprint(stations.keys())
    #pprint(stations.values())
    data = json.dumps(stations, indent=2, ensure_ascii=False)
    print(data)
    with open('stations.json','w') as file:
        file.write(data)
 
if __name__ == '__main__':
    main()
