import requests
import time
#import dmpt
import re
import random
from copyheaders import headers_raw_to_dict
 
DEFAULT_HEADERS={
'Host':'kyfw.12306.cn',
'Connection':'keep-alive',
'Upgrade-Insecure-Requests':'1',
'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36',
'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
'Referer':'https://kyfw.12306.cn/otn/index/init',
'Accept-Language':'zh-CN,zh;q=0.9',
}

def get_random():
  return str(random.random()) 
def get_13_time(): #一个十三位的时间戳
  return str(int(time.time()*1000))
class CN12306(object):
  def __init__(self):
    self.chufa='2018-02-03'
    self.s=requests.session()
    self.s.verify = False  # 忽略https 证书验证
  def get_init(self): #请求了一个首页
    url='https://kyfw.12306.cn/otn/login/init'
    r=self.s.get(url)
    print('首页获取成功，状态码：',r)
 
  def get_newpasscode(self): #这个页面不知道是干啥的，但是12306 请求了，咱们为了模仿的像一点也去请求
    url='https://kyfw.12306.cn/otn/resources/js/newpasscode/captcha_js.js?_={}'.format(get_13_time())
    r=self.s.get(url)
    print('newpasscode获取成功，状态码：',r)
 
  def get_auth_code(self): #获取验证码
    url='https://kyfw.12306.cn/passport/captcha/captcha-image?login_site=E&module=login&rand=sjrand&{}'.format(get_random())
    r=self.s.get(url)
    with open('auth_code.png', 'wb') as auth:
      auth.write(r.content)
      auth.flush()
      auth.close()
    return str(r) == '<Response [200]>'
 
  def analysis_auth_code(self): # 调用打码平台，返回验证码坐标
    dmt = dmpt.DamatuApi("打码平台帐号", "打码平台密码")
    analysis_auth = dmt.decode('auth_code.png', 287) # 上传打码
    analysis_auth = re.sub('\|', ',', analysis_auth)
    li = analysis_auth.split(',')
    for i in range(len(li)):
      if i % 2 == 0:
        pass
      else:
        li[i] = str(int(li[i]) - 30)
    analysis_auth = str(li)
    analysis_auth = re.sub("'", '', analysis_auth)
    analysis_auth = re.sub("\]", '', analysis_auth)
    analysis_auth = re.sub("\[", '', analysis_auth)
    analysis_auth = re.sub(" ", '', analysis_auth)
    print('验证码坐标', analysis_auth)
    self.analysis_auth= analysis_auth # 验证码坐标
 
  def auth_auth_code(self): #验证验证码是否正确提交方式post
    url='https://kyfw.12306.cn/passport/captcha/captcha-check'
    data={
      'answer':self.analysis_auth ,
      'login_site':'E',
      'rand':'sjrand',
    }
    r=self.s.post(url=url,data=data)
    print(r.text)
    if r.text == '''{"result_message":"验证码校验成功","result_code":"4"}''': #验证码校验成功
      return True
    else: #如果验证码校验失败
      print('验证码错误，刷新验证码，重新提交')
      if self.get_auth_code():  #获取验证码
        self.analysis_auth_code() #调用打码平台
        self.auth_auth_code() #重新校验验证码
 
  def login(self):
    url='https://kyfw.12306.cn/passport/web/login'
    data={
    'username' : '12306帐号',
    'password' : '12306密码',
    'appid' : 'otn',
    }
    r=self.s.post(url=url,data=data)
    self.uamtk=r.json()["uamtk"]
 
    print(r.text)
 
  def userLogin(self):
    url='https://kyfw.12306.cn/otn/login/userLogin'
    r=self.s.post(url=url)
    # print(r.text)
  def getjs(self):  #不知道是干啥的，但是也提交吧
    url='https://kyfw.12306.cn/otn/HttpZF/GetJS'
    r=self.s.get(url)
  def post_uamtk(self):
    url='https://kyfw.12306.cn/passport/web/auth/uamtk'
    data={ 'appid':'otn'}
    r=self.s.post(url=url,data=data,allow_redirects=False)
    self.newapptk=r.json()["newapptk"]
    r.encoding='utf-8'
    print(r.text)
  def post_uamauthclient(self):
    url='https://kyfw.12306.cn/otn/uamauthclient'
    data={
      'tk':self.newapptk
    }
    r=self.s.post(url=url,data=data)
    self.apptk = r.json()["apptk"]
    r.encoding='utf-8'
    print(r.text)
  def get_userLogin(self):
    url='https://kyfw.12306.cn/otn/login/userLogin'
    r=self.s.get(url)
    r.encoding='utf-8'
    # print(r.text)
  def get_leftTicket(self):
    url='https://kyfw.12306.cn/otn/leftTicket/init'
    r=self.s.get(url)
    r.encoding='utf-8'
    # print(r.text)
  def get_GetJS(self):
    url='https://kyfw.12306.cn/otn/HttpZF/GetJS'
    self.s.get(url)
 
  def get_qufzjql(self):
    url = 'https://kyfw.12306.cn/otn/dynamicJs/qufzjql'
    self.s.get(url)
 
  def get_queryZ(self):
    url='https://kyfw.12306.cn/otn/leftTicket/queryZ?leftTicketDTO.train_date={}&leftTicketDTO.from_station={}&leftTicketDTO.to_station={}&purpose_codes={}'.format(self.chufa,'BJP','TBP','ADULT')
    r=self.s.get(url)
    r.encoding='utf-8'
    # print(r.text)
    cheliang=r.json()["data"]["result"]
    for i in cheliang:
      dandulist=str(i).split('|')
      if len(str(dandulist[0]))>=100:
        self.secretStr=dandulist[0]
        # secretStr = str(x[0])
        车次=str(dandulist[3])
        出发时间=str(dandulist[8])
        到达时间 = str(dandulist[9])
        历时=str(dandulist[10])
        软卧 = str(dandulist[23])
        硬卧=str(dandulist[28])
        print(i)
        print('可预订车次列表，','车次：',车次,'出发时间：', 出发时间,'到达时间：', 到达时间,'历时：', 历时,'软卧剩余： ',软卧,' 硬卧剩余： ',硬卧)
        if (软卧 != '' and 软卧 != '0' and 软卧 != '无' and 软卧 != '空') or (硬卧 != '' and 硬卧 != '0' and 硬卧 != '无' and 硬卧 != '空'):
          #执行下单操作
          self.post_submitOrderRequest()
          self.post_initDc()
          self.post_getPassengerDTOs()
          return False
 
      print('*****************************************************')
    return True
 
 
  # 点击预定下单
  def post_submitOrderRequest(self):
    url='https://kyfw.12306.cn/otn/leftTicket/submitOrderRequest'
    data={
      'secretStr':self.secretStr,
      'train_date':self.chufa, #出发时间
      'back_train_date':self.chufa ,#返回时间
      'tour_flag':'dc',
      'purpose_codes':'ADULT',
      'query_from_station_name':'北京',
      'query_to_station_name':'天津北',
      'undefined':''
       }
    r=self.s.post(url=url,data=data)
    print(r.text)
  def post_initDc(self):
    url='https://kyfw.12306.cn/otn/confirmPassenger/initDc'
    r=self.s.post(url)
    # r.text
    self.REPEAT_SUBMIT_TOKEN=re.findall("globalRepeatSubmitToken = '(.*?)';",r.text)[0]
  def post_getPassengerDTOs(self): #获取乘客信息
    url='https://kyfw.12306.cn/otn/confirmPassenger/getPassengerDTOs'
    data={
      'REPEAT_SUBMIT_TOKEN':self.REPEAT_SUBMIT_TOKEN,
      '_json_att':''
    }
    r=self.s.post(url=url,data=data)
    r.encoding='utf-8'
    print(r.text)
 
if __name__ == '__main__':
  print(get_random())
  cn=CN12306()
  cn.get_init()
  cn.get_newpasscode()
  if cn.get_auth_code():
    #如果验证码获取成功，就调用打码平台
    print('验证码获取成功')
    print('正在调用打码平台...')
    cn.analysis_auth_code()
    if cn.auth_auth_code(): #验证验证码是否正确
      cn.login()
      cn.userLogin()
      cn.getjs()
      cn.post_uamtk()
      cn.post_uamauthclient()
      cn.get_userLogin()
      cn.get_leftTicket()
      cn.get_GetJS()
      cn.get_qufzjql()
 
      while cn.get_queryZ():
        time.sleep(30)
 

