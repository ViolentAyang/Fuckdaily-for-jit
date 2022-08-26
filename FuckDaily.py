import sys

import requests
import re
import json

class FuckDaily():

    def __init__(self,username,password,address,sever):
        self.username = username#账号
        self.password = password#密码
        self.address = address#地址

        self.severInform = sever#sever酱通知密钥
        # -------------------------------------------------------------------------------------------------------------
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:103.0) Gecko/20100101 Firefox/103.0',
        }
        self.loginUrl = 'http://authserver.jit.edu.cn/authserver/login?service=http://ehallapp.jit.edu.cn/qljfwapp/sys/lwJitHealthInfoDailyClock/index.do?amp_sec_version_=1'
        self.params = {
            'pageNumber': '1'
        }
        self.state = ''

    def login(self):
        session = requests.Session()
        response = requests.get(self.loginUrl, headers=self.headers)
        # get请求，获取响应网页数据
        htmls = response.content.decode()
        # 将字典转换为字符类型，用于正则表达式提取
        it = re.findall('name="lt" value="(.*?)"/>', htmls)[0]
        execution = re.findall('name="execution" value="(.*?)"/>', htmls)[0]
        # 从get请求获取的响应网页数据，正则表达式提取lt和execution数据

        cookies = requests.utils.dict_from_cookiejar(response.cookies)
        # 将cookie转换为字典
        route = cookies['route']
        JSESSIONID = cookies['JSESSIONID']
        # 从字典中获取route键值和JSESSIONID键值

        data = {

            "username": self.username,
            "password": self.password,
            "lt": it,
            "dllt": "userNamePasswordLogin",
            "execution": execution,
            "_eventId": "submit",
            "rmShown": "1"

        }  # 构建post表单数据/用户数据

        session.headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Connection': 'keep-alive',
            'Cookie': 'route={0}; JSESSIONID={1}'.format(route, JSESSIONID),
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:103.0) Gecko/20100101 Firefox/103.0',
        }  # 构建会话请求头部

        response = session.post(self.loginUrl, data=data, allow_redirects=False)
        # 发送请求头部和用户数据并禁止session重定向用来获取MOD_AUTH_CAS值

        session.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:103.0) Gecko/20100101 Firefox/103.0',
        }  # 重构会话请求头部

        casUrl = response.headers.get('Location')
        #获取重定向url
        ehallapp = session.get(casUrl)
        # 更新cookie值

        cookies = session.cookies
        # 最终cookies
        cookies=requests.utils.dict_from_cookiejar(cookies)

        cookies = {
            '_WEU': cookies.get('_WEU'),
            'EMAP_LANG': 'zh',
            'route': cookies.get('route'),
            'MOD_AUTH_CAS': cookies.get('MOD_AUTH_CAS'),
            'JSESSIONID': cookies.get('JSESSIONID'),
        }
        return cookies

    def time(self,cookies):

        timeUrl = 'http://ehallapp.jit.edu.cn/qljfwapp/sys/lwpub/api/getServerTime.do'
        severTime = requests.get(timeUrl,headers=self.headers,cookies=cookies)
        # 获取当前服务器时间
        timejson = severTime.json()
        time = timejson.get('date')
        DateTime = re.sub(r'/', "-", time)

        return DateTime

    def signJudge(self,cookies):
        reportUrl = 'http://ehallapp.jit.edu.cn/qljfwapp/sys/lwJitHealthInfoDailyClock/modules/healthClock/getTodayHasReported.do'
        getReport = requests.post(reportUrl, data=self.params,headers=self.headers,cookies=cookies)
        report = getReport.content.decode()
        reportObj = re.search(r'TODAY_TARRY_CONDITION_DISPLAY', report, re.M | re.I)
        return reportObj

    def getInfo(self,cookies):
        #获取上一次填写的数据和学生基本信息
        infoUrl = 'http://ehallapp.jit.edu.cn/qljfwapp/sys/lwJitHealthInfoDailyClock/modules/healthClock/getLatestDailyReportData.do'
        stuInfo = requests.post(infoUrl,cookies=cookies, headers=self.headers, data=self.params)
        stuJson = stuInfo.json()
        row1 = stuJson['datas']['getLatestDailyReportData']['rows']

        infoUrl2 = 'http://ehallapp.jit.edu.cn/qljfwapp/sys/lwJitHealthInfoDailyClock/modules/healthClock/V_LWPUB_JKDK_QUERY.do'
        stuInfo2 = requests.post(infoUrl2, cookies=cookies, headers=self.headers, data=self.params)
        stuJson2 = stuInfo2.json()
        row2 = stuJson2['datas']['V_LWPUB_JKDK_QUERY']['rows']

        infoDict={
            "BY4": row1[0]['BY4'],
            "BY3": row1[0]['BY3'],
            "TODAY_VACCINE_CONDITION": row1[0]['TODAY_VACCINE_CONDITION'],
            "BY4_DISPLAY": row1[0]['BY4_DISPLAY'],
            "TODAY_NAT_CONDITION": row1[0]['TODAY_NAT_CONDITION'],
            "TODAY_NAT_CONDITION_DISPLAY": row1[0]['TODAY_NAT_CONDITION_DISPLAY'],
            "BY1": row1[0]['BY1'],
            "TODAY_VACCINE_CONDITION_DISPLAY": row1[0]['TODAY_VACCINE_CONDITION_DISPLAY'],
            "TODAY_CONDITION": row1[0]['TODAY_CONDITION'],
            "BY3_DISPLAY": row1[0]['BY3_DISPLAY'],
            "PHONE_NUMBER": row1[0]['PHONE_NUMBER'],
            "TODAY_CONDITION_DISPLAY": row1[0]['TODAY_CONDITION_DISPLAY'],
            "BY1_DISPLAY": row1[0]['BY1_DISPLAY'],
            "BY19": row1[0]['BY19'],

            "USER_NAME": row2[0]['USER_NAME'],
            "DEPT_CODE": row2[0]['DEPT_CODE'],
            "DEPT_NAME": row2[0]['DEPT_NAME'],

        }
        return infoDict

    def widInfo(self,cookies):
        widUrl = 'http://ehallapp.jit.edu.cn/qljfwapp/sys/lwJitHealthInfoDailyClock/modules/healthClock/getMyTodayReportWid.do'
        widhtml = requests.post(widUrl, cookies=cookies, headers=self.headers, data=self.params)
        widText = widhtml.text
        widDict = {}
        widObj = re.search(r'"WID":"', widText, re.M | re.I)
        if widObj:
            wid = re.findall('"WID":"(.*?)","TODAY_', widText)[0]
            CZRQ = re.findall('CZRQ":"(.*?)","BY10', widText)[0]
            widDict = {
                'wid': wid,
                'CZRQ': CZRQ,
            }

        return widDict

    def addInfo(self,cookies):
        add = re.search(r'(.*)/(.*)/(.*)', self.address, re.M | re.I)
        province = add.group(1)
        city = add.group(2)
        county = add.group(3)


        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:103.0) Gecko/20100101 Firefox/103.0',
            'Referer': 'http://ehallapp.jit.edu.cn/qljfwapp/sys/lwJitHealthInfoDailyClock/index.do?amp_sec_version_=1',
        }

        add1Url = 'http://ehallapp.jit.edu.cn/qljfwapp/code/7c768460-374d-433f-a52b-30d72c2d95a1/1.do'
        add2Url = 'http://ehallapp.jit.edu.cn/qljfwapp/code/7c768460-374d-433f-a52b-30d72c2d95a1/2.do'
        add3Url = 'http://ehallapp.jit.edu.cn/qljfwapp/code/7c768460-374d-433f-a52b-30d72c2d95a1/3.do'

        add1 = requests.post(add1Url, cookies=cookies, headers=headers)
        add1Json = add1.json()
        rows = add1Json['datas']['code']['rows']
        id_by_name = dict([(p['name'], p['id']) for p in rows])
        proId = id_by_name[province]  # ************************************************************

        dainfo = '[{\"name\":\"LS\",\"value\":\"' + proId + '\",\"builder\":\"equal\",\"linkOpt\":\"AND\"}]'
        data = {
            "searchValue": dainfo,
        }
        add2 = requests.post(add2Url, cookies=cookies, headers=headers, data=data)
        add2Json = add2.json()
        rows = add2Json['datas']['code']['rows']
        id_by_name = dict([(p['name'], p['id']) for p in rows])
        cityId = id_by_name[city]  # *****************************************************************

        dainfo = '[{\"name\":\"LS\",\"value\":\"' + cityId + '\",\"builder\":\"equal\",\"linkOpt\":\"AND\"}]'
        data = {
            "searchValue": dainfo,
        }
        add3 = requests.post(add3Url, cookies=cookies, headers=headers, data=data)
        add3Json = add3.json()
        rows = add3Json['datas']['code']['rows']
        id_by_name = dict([(p['name'], p['id']) for p in rows])
        couId = id_by_name[county]  # *****************************************************************

        addDict = {
            'province': province,
            'city': city,
            'county': county,
            'proId': proId,
            'cityId': cityId,
            'couId': couId,
            'todayAdd':province+city,
        }
        return addDict


    def signIn(self,cookies,severTime,severDay,widDict,infoDict,addDict):

        reSaveUrl = 'http://ehallapp.jit.edu.cn/qljfwapp/sys/lwJitHealthInfoDailyClock/modules/healthClock/T_HEALTH_DAILY_INFO_SAVE.do'
        data = {
            "WID": widDict.get('wid'),
            "BY2": "",
            "BY7_DISPLAY": "否",
            "BY7": "0",
            "BY8_DISPLAY": "",
            "BY8": "",
            "CREATED_AT": severTime,
            "CZR": "",
            "CZZXM": "",
            "CZRQ": widDict.get('CZRQ'),
            "USER_ID": self.username,
            "USER_NAME": infoDict.get('USER_NAME'),
            "DEPT_CODE_DISPLAY": infoDict.get('DEPT_NAME'),
            "DEPT_CODE": infoDict.get('DEPT_CODE'),
            "DEPT_NAME": infoDict.get('DEPT_NAME'),
            "PHONE_NUMBER": infoDict.get('PHONE_NUMBER'),
            "FILL_TIME": severTime,
            "CLOCK_SITUATION": addDict.get('todayAdd'),
            "BY3_DISPLAY": addDict.get('province'),
            "BY3": addDict.get('proId'),
            "BY4_DISPLAY": addDict.get('city'),
            "BY4": addDict.get('cityId'),
            "BY11_DISPLAY": addDict.get('county'),
            "BY11": addDict.get('couId'),

            "TODAY_SITUATION_DISPLAY": "南京市外江苏省内",
            "TODAY_SITUATION": "004",
            "TODAY_CONDITION_DISPLAY": infoDict.get('TODAY_CONDITION_DISPLAY'),
            "TODAY_CONDITION": infoDict.get('TODAY_CONDITION'),
            "CONTACT_HISTORY_DISPLAY": "无",
            "CONTACT_HISTORY": "001",
            "TODAY_NAT_CONDITION_DISPLAY": infoDict.get('TODAY_NAT_CONDITION_DISPLAY'),
            "TODAY_NAT_CONDITION": infoDict.get('TODAY_NAT_CONDITION'),
            "TODAY_VACCINE_CONDITION_DISPLAY": infoDict.get('TODAY_VACCINE_CONDITION_DISPLAY'),
            "TODAY_VACCINE_CONDITION": infoDict.get('TODAY_VACCINE_CONDITION'),
            "TODAY_HEALTH_CODE_DISPLAY": "绿码",
            "TODAY_HEALTH_CODE": "001",
            "BY1_DISPLAY": infoDict.get('BY1_DISPLAY'),
            "BY1": infoDict.get('BY1'),
            "BY19_DISPLAY": self.address,
            "BY19": addDict.get('couId'),
            "BY5": "",
            "BY6": "",
            "BY20": "",
            "TODAY_BODY_CONDITION_DISPLAY": "",
            "TODAY_BODY_CONDITION": "",
            "TODAY_TEMPERATURE": "",
            "TODAY_ISOLATE_CONDITION_DISPLAY": "",
            "TODAY_ISOLATE_CONDITION": "",
            "TODAY_TARRY_CONDITION_DISPLAY": "",
            "TODAY_TARRY_CONDITION": "",
            "BY17_DISPLAY": "",
            "BY17": "",
            "NEED_CHECKIN_DATE": severDay,
            "CHECKED_DISPLAY": "",
            "CHECKED": "",
            "BY18_DISPLAY": "",
            "BY18": "",
            "BY9_DISPLAY": "",
            "BY9": "",
            "BY10_DISPLAY": "",
            "BY10": "",
            "BY16_DISPLAY": "",
            "BY16": "",
            "BY12_DISPLAY": "",
            "BY12": "",
            "BY13_DISPLAY": "",
            "BY13": "",
            "BY14_DISPLAY": "",
            "BY14": "",
            "BY15_DISPLAY": "",
            "BY15": ""
        }

        signIn = requests.post(reSaveUrl, data=data,headers=self.headers,cookies=cookies)
        signJson = signIn.json()
        print(signJson)
        '''
        save = signJson['datas']
        saveObj=save.get['T_HEALTH_DAILY_INFO_SAVE']
        if saveObj==1:
            print('ok')
        else:
            self.state='打卡失败'
        '''

    def severChan(self,severDay):
        #sever酱微信通知
        url = 'https://sctapi.ftqq.com/{}.send'.format(self.severInform)
        info = severDay + ' 健康打卡~'
        form = {
            'title': info
        }
        response = requests.post(url, data=form)

    def run(self):
        cookies=FuckDaily.login(self)

        severTime=FuckDaily.time(self,cookies)
        severDay = re.findall('(.*?) ', severTime)[0]

        widDict=FuckDaily.widInfo(self,cookies)
        infoDict=FuckDaily.getInfo(self,cookies)
        addDict=FuckDaily.addInfo(self,cookies)
        FuckDaily.signIn(self,cookies,severTime,severDay,widDict,infoDict,addDict)
        FuckDaily.severChan(self,severDay)
        
if __name__ == '__main__':
    app = FuckDaily(sys.argv[1],sys.argv[2],sys.argv[3],sys.argv[4])
    app.run()
