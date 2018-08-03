# -*- coding: utf-8 -*-
# @Time    : 2018/8/3 13:33
# @Author  : Yuan Zheng
# @Version    : 0.0.1
# @File    : update_score.py


import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
import zmail



def send_email(data_dict, course_info):
    if "ucas" in rece_email:
        server = zmail.server(rece_email, rece_pass, pop_host='mail.cstnet.cn', pop_ssl=True,
                              smtp_host='mail.cstnet.cn', smtp_ssl=True)
    else:
        server = zmail.server(rece_email, rece_pass)
    if server.smtp_able():
        pass
    # SMTP function.
    if server.pop_able():
        pass
    # POP function.
    content = ''
    content += data_dict['GPA'] + '\n' + data_dict['GPA_rank'] + '\n'
    for item in course_info:
        content += "{:<15}{:<10}{:<10}\n".format(item[0], item[1], item[2])
    mail_content = {
        'subject': "课程成绩更新",
        'content': content
    }
    print("*"*10, "有成绩更新啦！", "*"*10)
    print(content)

    server.send_mail(rece_email, mail_content)



def check_score():
    chromePath = r'D:\python程序\chromedriver.exe' ## 按需修改
    phantomjsPath = r'D:\python程序\phantomjs.exe'
    try:
        #wd = webdriver.Chrome(executable_path=chromePath)  # 构建浏览器
        wd = webdriver.PhantomJS(executable_path=phantomjsPath)
        loginUrl = "http://onestop.ucas.ac.cn/home/index"

        wd.get(loginUrl)  # 进入登陆界面
        wd.maximize_window()
        wd.find_element_by_xpath('//*[@id="menhuusername"]').send_keys(username)  # 输入用户名
        wd.find_element_by_xpath('//*[@id="menhupassword"]').send_keys(password)  # 输入密码
        wd.find_element_by_xpath('//*[@id="menuhudiv"]/div[4]/div').click()  # 点击登陆
        #print('跳转前:', wd.current_url)

        # 确保已经登录成功 以下一种均可以
        WebDriverWait(wd, 30)
        time.sleep(5)

        xuankeurl = "http://sep.ucas.ac.cn/portal/site/226/821"
        wd.get(xuankeurl)
        WebDriverWait(wd, 30)
        time.sleep(5)

        semester_score = "http://jwxk.ucas.ac.cn/score/bks/52575"  ## 不同学期末尾不一样，按需修改
        wd.get(semester_score)
        #os.system("pause")
        i = 0
        course_num = 0

        while (1):
            i += 1
            wd.refresh()
            html = wd.page_source
            # print(html)
            soup = BeautifulSoup(html, "html.parser")
            # print(soup)
            # os.system('pause')
            tags = soup.find_all('tbody')
            info_tag = tags[0]
            score_tag = tags[1]
            info_entry = info_tag.find_all('td')
            data_dict = dict()
            data_dict['GPA'] = info_entry[4].text
            data_dict['GPA_rank'] = info_entry[5].text
            #print(data_dict['GPA'], "    ", data_dict['GPA_rank'])

            course_info = list()
            score_entries = score_tag.find_all('tr')

            for idx, score_entry in enumerate(score_entries):
                info = score_entry.findChildren()
                course_info.append((info[1].text, info[3].text, info[4].text))
            #print(course_info)

            if len(score_entries) != course_num:
                course_num = len(score_entries)
                if (i != 1):
                    send_email(data_dict, course_info)
            if (i == 1):
                print("首次查询，当前数据如下")
                print(data_dict['GPA'], "    ", data_dict['GPA_rank'])
                for item in course_info:
                    print("{:<15}{:<10}{:<10}\n".format(item[0], item[1], item[2]))
            time.sleep(60)
    finally:
        wd.quit()

username = input("请输入课程网站用户名：")
password = input("请输入课程网站密码：")
rece_email = input("请输入收件邮箱：")
rece_pass = input("请输入收件邮箱密码：")
check_score()