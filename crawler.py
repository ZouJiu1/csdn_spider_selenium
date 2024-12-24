#################
###ZouJiu-202306
#################
from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver import EdgeOptions
import os
from selenium.webdriver.common.by import By
import time
import pickle
import json
from selenium.webdriver.support.wait import WebDriverWait
import requests
from copy import deepcopy
import argparse
from datetime import datetime
# from selenium.webdriver.common import keys
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.common.exceptions import ElementNotVisibleException, ElementNotSelectableException
from selenium.webdriver.common.actions.wheel_input import ScrollOrigin
# import numpy as np
import shutil
# from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.print_page_options import PrintOptions
# from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support import expected_conditions as EC
import base64
import re
from zipfile import ZipFile
from bs4 import BeautifulSoup
import shutil

abspath = os.path.abspath(__file__)
filename = abspath.split(os.sep)[-1]
abspath = abspath.replace(filename, "")

import sys
sys.path.append(abspath)
import platform
# wkhtmltopdf_path = os.path.join(abspath, r'wkhtmltopdf\bin\wkhtmltopdf.exe')
# sys.path.append(wkhtmltopdf_path)

copyed = True

def find_userDataDir():
    global copyed
    cdi = r'C:\Users'
    userDataDir = r'''C:\Users\10696\AppData\Local\Microsoft\Edge\User Data'''
    for i in os.listdir(cdi):
        nowpth = userDataDir.replace(r"10696", i)
        if os.path.exists(nowpth):
            cppath = nowpth.replace(r'''User Data''', "UserData1")
            if os.path.exists(cppath) and copyed:
                return cppath
            if os.path.exists(cppath):
                shutil.rmtree(cppath)
            if not os.path.exists(cppath):
                try:
                    shutil.copytree(nowpth, cppath,dirs_exist_ok=True, ignore_dangling_symlinks=True)
                except Exception as e:
                    with open(verify_txt, 'w', encoding='utf-8') as obj:
                        obj.write("1\n")
                        obj.write(userDataDir+"\n")
                    print("需要关闭浏览器，否则没有权限复制目录和文件")
                    # raise e
            copyed = True
            return cppath
    raise FileNotFoundError(userDataDir)

def edgeopen(driverpath, pdfpath):
    global human_verify
    # driverpath = r'''C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe'''
    service=Service(executable_path=driverpath)
    edge_options = EdgeOptions()

    #https://stackoverflow.com/questions/53039551/selenium-webdriver-modifying-navigator-webdriver-flag-to-prevent-selenium-detec
    edge_options.add_experimental_option('excludeSwitches', ['enable-automation'])
    edge_options.add_experimental_option('useAutomationExtension', False)
    edge_options.add_argument('lang=zh-CN,zh,zh-TW,en-US,en')
    # edge_options.add_argument('--window-size=1920,1080')
    edge_options.add_argument('--disable-gpu')
    edge_options.add_argument('--disable-dev-shm-usage')
    edge_options.add_argument('--remote-debugging-port=9222')
    if human_verify:
        userDataDir = find_userDataDir()
        print("---------------------------------------------")
        print("---------------------------------------------")
        print("---------------------------------------------")
        print("被网站屏蔽了，不允许登录，采用另一种登录方式")
        print("被复制的文件夹路径在：")
        print(f"{userDataDir}")
        print("占用的磁盘空间还请自行查看")
        # print("下面需要登录并保存cookie")
        # print("需要在浏览器设置里面，选择自己的账户")
        # userDataDir = r'''C:\Users\10696\AppData\Local\Microsoft\Edge\UserData1'''
        # profileDir = r'''Profile 2'''  # 浏览器内的第几个账户，从1开始
        edge_options.add_argument(f"--user-data-dir={userDataDir}")
        # edge_options.add_argument(f"--profile-directory=.")
        with open(verify_txt, 'w', encoding='utf-8') as obj:
            obj.write("1\n")
            obj.write(userDataDir+"\n")
    # edge_options.add_argument("--headless")
    # edge_options.add_argument('start-maxmized')
    edge_options.add_argument("disable-blink-features=AutomationControlled")#就是这一行告诉chrome去掉了webdriver痕迹
    
    # #https://stackoverflow.com/questions/56897041/how-to-save-opened-page-as-pdf-in-selenium-python
    # settings = {
    #     "recentDestinations": [{
    #             "id": "Save as PDF",
    #             "origin": "local",
    #             "account": "",
    #         }],
    #         "selectedDestinationId": "Save as PDF",
    #         "version": 2
    #     }
    # #https://www.apiref.com/java11-zh/java.desktop/javax/print/attribute/standard/MediaSize.ISO.html
    # settings = {
    #     "recentDestinations": [{
    #         "id": "Save as PDF",
    #         "origin": "local",
    #         "account": ""
    #     }],
    #     "selectedDestinationId": "Save as PDF",
    #     "version": 2,
    #     "isHeaderFooterEnabled": False,
    #     "mediaSize": {
            
    #         "height_microns": 297000,
    #         "name": "ISO_A4",
    #         "width_microns": 210000,
    #         "custom_display_name": "A4"
    #     },
    #     "customMargins": {"margin": 0},
    #     "marginsType": 3,
    #     # "scaling": 130,
    #     # "scalingType": 3,
    #     # "scalingTypePdf": 3,
    #     "isCssBackgroundEnabled": True
    # }
    # prefs = {
    #     'printing.print_preview_sticky_settings.appState': json.dumps(settings),
    #     'savefile.default_directory': pdfpath,
    #     }
    # edge_options.add_experimental_option('prefs', prefs)
    # edge_options.add_argument('--kiosk-printing')

    # https://www.selenium.dev/documentation/webdriver/drivers/options/#pageloadstrategy  
    # https://stackoverflow.com/questions/44503576/selenium-python-how-to-stop-page-loading-when-certain-element-gets-loaded
    # edge_options.add_argument(page_load_strategy, 'normal')
    # if strategy:
    edge_options.page_load_strategy = 'normal'
    # edge_options.use_chromium = True
    # cap = DesiredCapabilities.EDGE
    # cap['pageLoadStrategy'] = 'none'
    
    driver = webdriver.Edge(options=edge_options, service = service)
    # stealth(driver,
    #         languages=["en-US", "en"],
    #         vendor="Google Inc.",
    #         platform="Win32",
    #         webgl_vendor="Intel Inc.",
    #         renderer="Intel Iris OpenGL Engine",
    #         fix_hairline=True,
    #         )
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    import numpy as np
    driver.execute_cdp_cmd('Network.setUserAgentOverride', {"userAgent": 'Mozilla/6.0 (Windows NT 11.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4103.53 Safari/600.36' + str(np.random.randint(1, 100000))})
    driver.set_script_timeout(130)
    
    return driver

def crawlsleep(times):
    time.sleep(times + 1)

def now():
    return time.time()

def nowtime():
    nowtm = datetime.fromtimestamp(time.time()).isoformat().replace(":", "_")
    return nowtm

def old_crawl_article_links(driver:webdriver):
    #crawl articles links
    footer = driver.find_element(By.TAG_NAME, "html")
    number = driver.find_element(By.CLASS_NAME, "user-profile-body-right").find_elements(By.TAG_NAME, "ul")[0]
    tagname = driver.find_element(By.CLASS_NAME, "user-profile-head-info-r-c").find_elements(By.CLASS_NAME, "user-profile-statistics-num")
    num = 0
    # for t in tagname:
    #     if '文章' in t.text:
    num = tagname[1].text
    number = int(num)
    scrollHeight = driver.execute_script('''return document.getElementsByClassName("user-profile-body-right")[0].scrollHeight''')
    scroll_origin = ScrollOrigin.from_element(footer, 0, 0)
    ActionChains(driver).scroll_from_origin(scroll_origin, 0, -100000).perform()
    for i in range(number // 20 + 10):
        ActionChains(driver).scroll_from_origin(scroll_origin, 0, scrollHeight).perform()
        crawlsleep(1)
    crawlsleep(sleeptime)
    article = driver.find_elements(By.TAG_NAME, "article")
    all_article_detail = {}
    for at in article:
        href = at.find_element(By.TAG_NAME, 'a').get_attribute('href')
        title = at.find_element(By.CLASS_NAME, 'blog-list-box-top').text
        nam = title.replace(":", "_").replace("?", "_问号_"). \
                    replace("/","_").replace("\\","_").replace("\"", "_").\
                    replace("*","_").replace("|", "_").replace("？", "_问号_").replace("！", "_感叹号_").\
                    replace("<", "小于").replace(">", "大于").replace("(", "").\
                    replace(")", "").replace(",", "_逗号_").replace("，", "_逗号_").replace("   ", "_空格_").\
                    replace("  ", "_空格_").replace(" ", "_空格_").replace("：", "_冒号_")
        viewme = at.find_element(By.CLASS_NAME, "view-time-box").text
        viewme = viewme[2+3:].replace(".", "_").replace(":", "_")[:-2]
        readnum = at.find_element(By.CLASS_NAME, "view-num").text
        readnum = readnum.split(" ")[0]
        all_article_detail[viewme+"_"+str(title)+"_"+readnum] = href
    crawlsleep(sleeptime)

    with open(os.path.join(articledir, 'article.txt'), 'w', encoding='utf-%d'%(6+2)) as obj:
        for key, val in all_article_detail.items():
            obj.write(val + " " + key + '\n')

def crawl_article_links(driver:webdriver):
    #crawl articles links
    driver.get(r'https://mp.csdn.net/mp_blog/manage/article')
    footer = driver.find_element(By.TAG_NAME, "html")
    # number = driver.find_element(By.CLASS_NAME, "user-profile-body-right").find_elements(By.TAG_NAME, "ul")[0]
    WebDriverWait(driver, timeout=60).until(lambda d:d.find_element(By.CLASS_NAME, "number"))
    WebDriverWait(driver, timeout=60).until(lambda d:d.find_element(By.CLASS_NAME, "nav-link"))
    number = driver.find_elements(By.CLASS_NAME, "number")[-1].text
    number = int(number)
    driver.get(r'https://mp.csdn.net/mp_blog/manage/article')
    WebDriverWait(driver, timeout=60).until(lambda d:d.find_element(By.CLASS_NAME, "nav-link"))
    tagname = driver.find_elements(By.CLASS_NAME, "nav-link")
    num = 0
    # for t in tagname:
    #     if '文章' in t.text:
    num = tagname[0].text
    num = int(num[3:-1])
    button = driver.find_element(By.CLASS_NAME, "btn-next")
    number = int(driver.find_elements(By.CLASS_NAME, "number")[-1].text)

    all_article_detail = {}
    for ij in range(number+1):
        if ij==number-1:
            k=0
        button = driver.find_element(By.CLASS_NAME, "btn-next")
        article_list_item_mp = driver.find_elements(By.CLASS_NAME, "article-list-item-mp")
        for i in article_list_item_mp:
            tiltime = i.find_element(By.CLASS_NAME, "list-item-title")
            title = tiltime.find_element(By.CLASS_NAME, "article-list-item-txt").text.replace("？", "问号").strip()
            time = tiltime.find_element(By.CLASS_NAME, "article-list-item-time").text
            hrefs = i.find_elements(By.TAG_NAME, "a")
            hrefs.reverse()
            href = ''
            for h in hrefs:
                href = h.get_attribute('href')
                if 'http' in href:
                    break
            all_article_detail[time+"_"+str(title)] = href
        try:
            ActionChains(driver).click(button).perform()
        except Exception as e:
            print(e)
            break
        # crawlsleep(30)
        crawlsleep(1)

    with open(os.path.join(articledir, 'article.txt'), 'w', encoding='utf-%d'%(6+2)) as obj:
        for key, val in all_article_detail.items():
            obj.write(val + " " + key + '\n')

def cleartxt(kkk):
    while ' ' in kkk:
        kkk = kkk.replace(" ", "")
    while "\n" in kkk:
        kkk = kkk.replace("\n", "")
    return kkk

num_prenodes = 0
def parser_beautiful(innerHTML, article, number, dircrea, bk=False, prenodes = None):
    global num_prenodes

    if not innerHTML:
        return article, number
    # if bk:
    #     article += "**"
    if isinstance(innerHTML, str):
        article += innerHTML.text
        return article, number
    inname = innerHTML.name
    
    # if inname=='li' and 'style' in innerHTML.attrs.keys():
    #     style = innerHTML.attrs["style"]
    #     if '153' in style:
    #         return article, number
    # inname = innerHTML.name
    allchild = [i for i in innerHTML.children]
    for id, chi in enumerate(innerHTML.children):
        # article, number = parser_beautiful(chi, article, number, dircrea, bk, prenodes)
        tag_name = chi.name
        if chi=='\n':
            continue
        if isinstance(chi, str):
            article += chi.text
            continue
        else:
            cll = [c for c in chi.children]
        if tag_name in ['table', 'tbody', 'tr', 'td', 'u', "article", 'pre', 'ul']:
            article, number = parser_beautiful(chi, article, number, dircrea, bk, prenodes)
        elif tag_name=="li":
            # article += "\n* "
            art, _ = parser_beautiful(chi, "", 0, dircrea, bk, prenodes)
            article += "\n* "+art + "\n"
        elif tag_name=="em":
            article += " *" + chi.text + "* "
        elif tag_name=="blockquote":
            if len(cll) > 1:
                art, _ = parser_beautiful(chi, "", 0, dircrea, True, prenodes)
                art = re.sub(r'\n\n+', '\n', art)
                article += '\n>'+art+'\n'
            else:
                article += "\n>" + chi.text + "\n"
        elif tag_name=="br":
            if inname=="p" and tag_name=='br':
                kk = list(innerHTML.children)
                if len(kk) >= 2 and kk[1].name=='a':
                    linksite = None
                    title = None
                    if 'href' in kk[1].attrs.keys():
                        linksite = kk[1].attrs['href']
                    if 'title' in kk[1].attrs.keys():
                        title = kk[1].attrs['title']
                    if linksite and title:
                        article += f'[{title}]({linksite})\n\n'
                    break
            article += "\n"
        elif tag_name=="p":
            if len(article)==0:
                pass
            # elif article[-1]=='\n':
            #     article += "\n"
            # else:
            #     article += "\n\n"
            article, number = parser_beautiful(chi, article, number, dircrea, bk, prenodes)
            article += "\n\n"
        # elif tag_name=="br":
        #     article += "<br>\n"
        elif tag_name in ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']:
            article += '#' * int(tag_name[-1]) + ' '
            article, number = parser_beautiful(chi, article, number, dircrea, bk, prenodes)
            article += '\n\n'
        elif tag_name=="span":
            datatex = None
            classc = None
            span = chi.find_all("span")
            for ip in span:
                if 'class' in ip.attrs.keys():
                    katex_mathml = ip.attrs['class']
                    if len(katex_mathml) > 0 and katex_mathml[0] == 'katex-mathml':
                        mathml = ip.text
                        kk = mathml.split("\n")
                        rek = []
                        maxind = -6
                        ind = 0
                        for ki in kk:
                            while ki and (ki[0]==" " or ki[0]=='\n'):
                                ki = ki[1:]
                            while ki and (ki[-1]==" " or ki[-1]=='\n'):
                                ki = ki[:-1]
                            if len(ki) > 0:
                                rek.append(ki)
                                if len(ki) > maxind:
                                    maxind = len(ki)
                                    ind = len(rek) - 1
                        text = rek[ind]
                        article += "$" + text + "$"
                        break
            if 'data-tex' in chi.attrs.keys():
                datatex = chi.attrs["data-tex"]
            if 'class' in chi.attrs.keys():
                classc = chi.attrs["class"]
            if datatex and classc and 'ztext-math' in classc:
                if article[-3-1:]=='<br>' or article[-1:]=='\n':
                    article += "\n$" + chi.attrs["data-tex"] + "$"
                else:
                    article += "$" + chi.attrs["data-tex"] + "$"
        elif tag_name=="a":
            linksite = None
            if 'href' in chi.attrs.keys():
                linksite = chi.attrs['href']
            if linksite:
                ar, _ = parser_beautiful(chi, "", 0, dircrea, False, prenodes)
                if ar=='':
                    if 'title' in chi.attrs.keys():
                        ar = chi['title']
                if len(article) > 0 and article[-1]=='\n':
                    article += "["+ar+"]"+"("+linksite + ")"
                else:
                    article += "["+ar+"]"+"("+linksite + ")"
            if id!=len(allchild)-1 and allchild[id+1].name=='a':
                article += '\n\n'
        elif tag_name=='b' or tag_name=='strong':
            if len(cll) > 1:
                art, _ = parser_beautiful(chi, "", 0, dircrea, False, prenodes)
                article += "**" + art + "**"
            else:
                txt = chi.text
                while len(txt) > 0 and txt[-1] == " ":
                    txt = txt[:-1]
                article += " **" + txt + "** "
        elif tag_name=="img":
            noscript = chi.find_all('noscript')
            if len(noscript) > 0:
                chi.noscript.extract()
            # imgchunk = chi.find_all('img')

            imglink = chi.attrs["src"]
            if imglink==None:
                return article, number
            if 'alt' in chi.attrs.keys():
                alt = chi.attrs["alt"]
            else:
                return article, number
            if alt!=None:
                while len(alt) > 0 and alt[-1]==" ":
                    alt = alt[:-1]
                while len(alt) > 0 and alt[0]==" ":
                    alt = alt[1:]
                if len(alt) > 0:
                    if article[-3-1:]=='<br>' or article[-1:]=='\n':
                        article += "\n$" + alt + "$"
                    else:
                        article += "$" + alt + "$"
            try:
                response = requests.get(imglink, timeout=30)
            except:
                try:
                    response = requests.get(imglink, timeout=30)
                except:
                    continue
            if response.status_code==200:
                article += ''' <img src="%d.jpg" width="100%%"/> \n\n'''%number
                # article += '''<img src="%d.jpg"/>'''%number
                with open(os.path.join(dircrea, str(number) + '.jpg'), 'wb') as obj:
                    obj.write(response.content)
                number += 1
                crawlsleep(sleeptime)
        elif tag_name == "code":
            text = chi.text
            language = "text"
            lan = None
            if inname!='pre':
                article += "`" + text + "`"
                continue

            if 'class' in chi.attrs.keys():
                lan = chi.attrs["class"]
                if isinstance(lan, list):
                    lan = ' '.join(lan)
            if lan:
                lgg = re.findall(' *language-(\w*) *', lan)
                if len(lgg)!=0:
                    language = lgg[0]
            if language=='text':
                precode = text
                if "#include" in precode or 'vector' in precode or 'using namespace' in precode or 'cout' in precode or 'cin' in precode: 
                    language = "cpp"
                elif "def " in precode or "print" in precode or "):" in precode or \
                    ('import' in precode and 'as' in precode):
                    language = "python"
                elif "document" in precode or "</style>" in precode or "</script>" in precode or \
                    "</div>" in precode or "</video>" in precode or 'function()' in precode or \
                    'getElementById' in precode or '</html>' in precode:
                    language = "javascript"
                elif 'package' in precode or 'java.io' in precode or 'java.' in precode or \
                    'extends' in precode:
                    language = 'java'
            text = text.replace("\n\'\n运行", '')
            try:
                # language = "text"
                pn = prenodes[num_prenodes]
                # codelan = pn.find_elements(By.TAG_NAME, "code")
                # if len(codelan) > 0:
                #     lan = codelan[0].get_attribute("class")
                #     language = "text"
                # # if 'class' in pn.attrs.keys():
                #     # lan = pn.attrs['class']
                #     if len(lan)>0:
                #         lgg = re.findall(' *language-(\w*) *', lan)
                #         if len(lgg)!=0:
                #             language = lgg[0]
                #         # if 'language-' in lan:
                #         #     language = lan.split(" ")[0].split("-")[-1]
                if '\n' not in text:
                    text = pn.text
                
                if "\n1\n2" in text:
                    ind = text.index("\n1\n2")
                    text = text[:ind]
                    text = re.sub(r"\n\d", "", str(text))
                text = text.replace("\n\'\n运行", '')
                article += "\n\n```%s []\n"%language + text + "\n```\n\n"
                num_prenodes += 1
            except:
                article += chi.text + "\n"
                continue
        elif tag_name=="div":
            if inname=='pre':
                continue
            prenode = chi.find_all('code')
            if len(prenode) > 0:
                for i in prenode:
                    article += "\n\n```\n" + i.text + "\n```\n\n"
            else:
                article, number = parser_beautiful(chi, article, number, dircrea, bk, prenodes)
                article += "\n\n"

    # if bk:
    #     article += "**"
    article = re.sub(r'\n\* \d+', '', article)
    article = article.replace("\n\n\n\n\n", "\n\n")
    article = article.replace("\n\n\n\n", "\n\n")
    article = article.replace("\n\n\n", "\n\n")
    return article, number

def recursion(nod, article, number, driver, dircrea):
    if isinstance(nod, dict):
        if 'nodeName' in nod.keys() and nod['nodeName']=='#text':
            kkk = cleartxt(nod['textContent'])
            if len(kkk) > 0:
                article += nod['textContent']
            return article, number

    elif isinstance(nod, webdriver.remote.webelement.WebElement):
        tag_name = nod.tag_name
        if tag_name=="br":
            article += "<br>\n"
        if tag_name=="article":
            p_childNodes = driver.execute_script("return arguments[0].childNodes;", nod)
            for pnode in p_childNodes:
                article, number = recursion(pnode, article, number, driver, dircrea)
            article += "<br>\n"
        elif tag_name in ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']:
            article += "\n" + '#' * int(tag_name[-1]) + ' '
            p_childNodes = driver.execute_script("return arguments[0].childNodes;", nod)
            for pnode in p_childNodes:
                article, number = recursion(pnode, article, number, driver, dircrea)
            article += '\n'
        elif tag_name in ['table', 'tbody', 'tr', 'td', 'u']:
            p_childNodes = driver.execute_script("return arguments[0].childNodes;", nod)
            for pnode in p_childNodes:
                article, number = recursion(pnode, article, number, driver, dircrea)
        elif tag_name=="pre":
            # atags = nod.find_elements(By.TAG_NAME, 'a')
            try:
                morecode = nod.find_element(By.TAG_NAME, "img")
                footer = driver.find_element(By.TAG_NAME, "html")
                scroll_origin = ScrollOrigin.from_element(footer, 0, 0)
                ActionChains(driver).scroll_from_origin(scroll_origin, 0, -100000).perform()
                ActionChains(driver).scroll_from_origin(scroll_origin, 0, int(morecode.rect['y'])).perform()
                if morecode:
                    # crawlsleep(10)
                    WebDriverWait(nod, timeout=20, poll_frequency=1, \
                        ignored_exceptions=[ElementNotVisibleException, ElementNotSelectableException]).until(EC.element_to_be_clickable((By.TAG_NAME, "img")))
                    try:
                        driver.execute_script("arguments[0].click();", morecode)
                        morecode.click()
                    except:
                        try:
                            morecode = nod.find_element(By.CLASS_NAME, "look-more-preCode")
                            WebDriverWait(nod, timeout=10, poll_frequency=1, \
                                            ignored_exceptions=[ElementNotVisibleException, ElementNotSelectableException]).until(EC.element_to_be_clickable((By.TAG_NAME, "img")))
                            driver.execute_script("arguments[0].click();", morecode)
                            morecode.click()
                        except:
                            pass
            except:
                pass

            prenode = nod.find_elements(By.TAG_NAME, 'code')
            if len(prenode) > 0:
                for i in prenode:
                    article += "<br>\n```\n" + i.text + "\n```\n<br>"
        elif tag_name=="span":
            datatex = nod.get_attribute("data-tex")
            classc = nod.get_attribute("class")
            if datatex and classc and 'ztext-math' in classc:
                if article[-3-1:]=='<br>' or article[-1:]=='\n':
                    article += "\n$" + nod.get_attribute("data-tex") + "$"
                else:
                    article += "$" + nod.get_attribute("data-tex") + "$"
            else:
                # try:
                imgchunk = nod.find_elements(By.TAG_NAME, 'img')
                achunk = nod.find_elements(By.TAG_NAME, 'a')
                if len(imgchunk)==0 and len(achunk)==0:
                    # innerHTML = driver.execute_script("return arguments[0].innerHTML;", nod)
                    article += nod.text
                else:
                    p_childNodes = driver.execute_script("return arguments[0].childNodes;", nod)
                    for pnode in p_childNodes:
                        article, number = recursion(pnode, article, number, driver, dircrea)
                # except:
                    # article += nod.text
                    # pass
                # article += "<br>\n"
            # else:
            #     formula_span = nod.find_elements(By.CLASS_NAME, "ztext-math")
            #     for jf in range(len(formula_span)):
            #         ele = formula_span[jf]
            #         article += "$" + ele.get_attribute("data-tex") + "$"
        elif tag_name=="a":
            linksite = nod.get_attribute("href")
            if linksite:
                linksite = linksite.replace("//link.zhihu.com/?target=https%3A", "").replace("//link.zhihu.com/?target=http%3A", "")
                if article[-3-1:]=='<br>' or article[-1:]=='\n':
                    article += "\n\n["+nod.text+"]"+"("+linksite + ")"
                else:
                    article += "["+nod.text+"]"+"("+linksite + ")"
        elif tag_name=="b" or tag_name=="strong":
            txt = nod.text
            while len(txt) > 0 and txt[-1] == " ":
                txt = txt[:-1]
            article += " **" + txt + "** "
        elif tag_name=="em":
            article += nod.text
        elif tag_name=="blockquote":
            article += "<br>\n```\n" + nod.text + "\n```\n<br>"
        elif tag_name=='p':
            p_childNodes = driver.execute_script("return arguments[0].childNodes;", nod)
            for pnode in p_childNodes:
                article, number = recursion(pnode, article, number, driver, dircrea)
            article += "\n"
        elif tag_name=="div":
            # atags = nod.find_elements(By.TAG_NAME, 'a')
            prenode = nod.find_elements(By.TAG_NAME, 'code')
            if len(prenode) > 0:
                for i in prenode:
                    article += "<br>\n```\n" + i.text + "\n```\n<br>"
            else:
                p_childNodes = driver.execute_script("return arguments[0].childNodes;", nod)
                for pnode in p_childNodes:
                    article, number = recursion(pnode, article, number, driver, dircrea)
        elif tag_name=="img":
            # imgchunk = nod.find_elements(By.TAG_NAME, 'img')
            # for i in range(len(imgchunk)):
            imglink = nod.get_attribute("src")
            if imglink==None:
                return article, number
            alt = nod.get_attribute("alt")
            if alt!=None:
                while len(alt) > 0 and alt[-1]==" ":
                    alt = alt[:-1]
                if len(alt) > 0:
                    if article[-3-1:]=='<br>' or article[-1:]=='\n':
                        article += "\n$" + alt + "$"
                    else:
                        article += "$" + alt + "$"
            try:
                response = requests.get(imglink, timeout=30)
            except:
                try:
                    response = requests.get(imglink, timeout=30)
                except:
                    pass
            if response.status_code==200:
                # article += '''<img src="%d.jpg" width="100%%"/>'''%number
                article += ''' <img src="%d.jpg"/> '''%number
                with open(os.path.join(dircrea, str(number) + '.jpg'), 'wb') as obj:
                    obj.write(response.content)
                number += 1
                crawlsleep(sleeptime)
    return article, number

def removeelement(driver):
    try:
        driver.execute_script('''document.getElementById("asideSearchArticle").remove();''')
    except:
        pass
    try:
        driver.execute_script('''document.getElementById("asideHotArticle").remove();''')
    except:
        pass
    try:
        driver.execute_script('''document.getElementById("asideNewComments").remove();''')
    except:
        pass
    try:
        driver.execute_script('''document.getElementById("asideNewNps").remove();''')
    except:
        pass
    try:
        driver.execute_script('''document.getElementsByClassName("recommend-box")[0].remove();''')
    except:
        pass
    try:
        driver.execute_script('''document.getElementsByClassName("recommend-box")[1].remove();''')
    except:
        pass
    try:
        driver.execute_script('''document.getElementsByClassName("recommend-box")[2].remove();''')
    except:
        pass
    try:
        driver.execute_script('''document.getElementsByClassName("recommend-box")[0].remove();''')
    except:
        pass
    try:
        driver.execute_script('''document.getElementsByClassName("recommend-nps-box")[0].remove();''')
    except:
        pass
    try:
        driver.execute_script('''document.getElementById("csdn-toolbar").remove();''')
    except:
        pass
    try:
        driver.execute_script('''document.getElementsByClassName("toolbar-inside")[0].remove();''')
    except:
        pass
    try:
        driver.execute_script('''document.getElementsByClassName("blog-footer-bottom")[0].remove();''')
    except:
        pass
    try:
        driver.execute_script('''document.getElementById("treeSkill").remove();''')
    except:
        pass

def clickmorecode(driver):
    nodes = driver.find_elements(By.TAG_NAME, "pre")
    for nod in nodes:
        try:
            morecode = nod.find_element(By.TAG_NAME, "img")
        
            footer = driver.find_element(By.TAG_NAME, "html")
            scroll_origin = ScrollOrigin.from_element(footer, 0, 0)
            ActionChains(driver).scroll_from_origin(scroll_origin, 0, -100000).perform()
            ActionChains(driver).scroll_from_origin(scroll_origin, 0, int(morecode.rect['y'])).perform()
            if morecode:
                crawlsleep(2)
                WebDriverWait(nod, timeout=20, poll_frequency=1, \
                    ignored_exceptions=[ElementNotVisibleException, ElementNotSelectableException]).until(EC.element_to_be_clickable((By.TAG_NAME, "img")))
                try:
                    driver.execute_script("arguments[0].click();", morecode)
                    morecode.click()
                except:
                    try:
                        morecode = nod.find_element(By.CLASS_NAME, "look-more-preCode")
                        WebDriverWait(nod, timeout=10, poll_frequency=1, \
                                        ignored_exceptions=[ElementNotVisibleException, ElementNotSelectableException]).until(EC.element_to_be_clickable((By.TAG_NAME, "img")))
                        driver.execute_script("arguments[0].click();", morecode)
                        morecode.click()
                    except:
                        pass
        except:
            continue
    nodes = driver.find_elements(By.TAG_NAME, "pre")
    return nodes

def crawl_article_detail(driver:webdriver):
    global num_prenodes
    website_col = {}
    for i in os.listdir(articledir):
        try:
            kk = int(i)
            shutil.rmtree(os.path.join(articledir, i))
        except:
            pass
    with open(os.path.join(articledir, 'article.txt'), 'r', encoding='utf-8') as obj:
        for i in obj.readlines():
            i = i.strip()
            ind = i.index(" ")
            website = i[:ind]
            title   = i[ind+1:].replace("\n", "")
            website_col[website] = title

    allbegin = now()
    numberpage = 1e-6
    for website, title in website_col.items():
        begin = now()
        nam = title.replace(":", "_").replace("?", "_问号_"). \
                    replace("/","_").replace("\\","_").replace("\"", "_").\
                    replace("*","_").replace("|", "_").replace("？", "_问号_").replace("！", "_感叹号_").\
                    replace("<", "小于").replace(">", "大于").replace("(", "").\
                    replace(")", "").replace(",", "_逗号_").replace("，", "_逗号_").replace("   ", "_空格_").\
                    replace("  ", "_空格_").replace(" ", "_空格_").replace("：", "_冒号_")
        if len(nam) > 100:
            nam = nam[:100]
        temp_name = nam #str(np.random.randint(999999999)) + str(np.random.randint(999999999))
        # nam_pinyin = pinyin.get(nam, format='numerical')
        # if 'they_are_set_and_tested_correctly_in_' not in title:
        #     continue
        dircrea  = os.path.join(articledir, temp_name)
        fileexit = False
        dirname = ''
        filesize = 0
        kkk = -9
        tm = -1
        for i in os.listdir(articledir):
            if nam in i and os.path.isdir(os.path.join(articledir, i)):
                direxit = True
                dircol = os.path.join(articledir, i)
                for j in os.listdir(dircol):
                    if '.pdf' in j:
                        # tm = os.path.getmtime(os.path.join(dircol, j))
                        if os.path.getsize(os.path.join(dircol, j)) > 0:
                            kkk = 9
                            break
                if kkk > 0:
                    break
        if kkk > 0:
            print(f"{os.path.join(dircol, j)}已经爬取过了，不再重复爬取")
            continue
        # fileexit = os.path.exists(os.path.join(articledir, nam, nam + "_.pdf"))
        # if fileexit:
        #     filesize = os.path.getsize(os.path.join(articledir, nam, nam + "_.pdf"))
        # direxit  = os.path.exists(os.path.join(articledir, nam))

        # if direxit and not fileexit:
        #     try:
        #         os.remove(os.path.join(articledir, nam))
        #     except:
        #         pass
        # if direxit and fileexit and filesize > 0:
        #     continue
        # if direxit and fileexit and filesize == 0:
        #     os.remove(os.path.join(articledir, nam, nam + "_.pdf"))
        #     os.remove(os.path.join(articledir, nam))
        os.makedirs(dircrea, exist_ok = True)

        #get article text
        driver.get(website)
        WebDriverWait(driver, timeout=20).until(lambda d: d.find_element(By.CLASS_NAME, "more-toolbox-new"))
        # driver.maximize_window()
        #https://stackoverflow.com/questions/61877719/how-to-get-current-scroll-height-in-selenium-pythonblog-content-box
        scrollHeight = driver.execute_script('''return document.getElementsByClassName("blog-content-box")[0].scrollHeight''')
        footer = driver.find_element(By.TAG_NAME, "html")
        scroll_origin = ScrollOrigin.from_element(footer, 0, -60)
        # ActionChains(driver).scroll_from_origin(scroll_origin, 0, 100000).perform()
        crawlsleep(20)
        # ActionChains(driver).scroll_from_origin(scroll_origin, 0, -100000).perform()
        #remove noneed element

        url = driver.current_url
        prenodes = clickmorecode(driver)
        if MarkDown_FORMAT:

            contentbox = driver.find_element(By.CLASS_NAME, "blog-content-box")
            # richtext = contentbox.find_element(By.CLASS_NAME, "article-header-box")
            titletext = driver.find_element(By.CLASS_NAME, "title-article")
            # article_childNodes = driver.execute_script("return arguments[0].childNodes;", richtext)
            article = ""
            number = 0
            richtext = contentbox.find_element(By.TAG_NAME, "article").find_element(By.ID, "content_views")
            # article_childNodes = driver.execute_script("return arguments[0].childNodes;", richtext)
            # for nod in article_childNodes:
            #     article, number = recursion(nod, article, number, driver, dircrea)

            inner = driver.execute_script("return arguments[0].innerHTML;", richtext)
            innerHTML = BeautifulSoup(inner, "html.parser")
            num_prenodes = 0
            article, number = parser_beautiful(innerHTML, article, number, dircrea, prenodes=prenodes)

            article = article.replace("修改\n", "").replace("开启赞赏\n", "开启赞赏, ").replace("添加评论\n", "").replace("分享\n", "").\
                replace("收藏\n", "").replace("设置\n", "")
            tle = titletext.text

            article += "<br>\n\n["+url+"](" + url + ")<br>\n"
            driver.execute_script("const para = document.createElement(\"h3\"); \
                                    const br = document.createElement(\"br\"); \
                                    const node = document.createTextNode(\"%s\");\
                                    para.appendChild(node);\
                                    const currentDiv = document.getElementsByClassName(\"title-article\")[0];\
                                    currentDiv.appendChild(br); \
                                    currentDiv.appendChild(para);"%url \
                                )
            
            if len(article) > 0:
                try:
                    f=open(os.path.join(dircrea, nam[23:26] + "_.md"), 'w', encoding='utf-8')
                    f.close()
                except:
                    nam = nam[:len(nam)//2]
                    # dircrea  = os.path.join(articledir, temp_name[:len(temp_name)//2])
                    # nam = nam[:len(nam)//2]
                    # os.makedirs(dircrea)
                with open(os.path.join(dircrea, nam[23:26] + "_.md"), 'w', encoding='utf-8') as obj:
                    obj.write("# " + tle+"\n\n")
                    if len(article) > 0:
                        obj.write(article + "\n\n\n")

        # article to pdf
        try:
            rek = driver.find_element(By.XPATH, "//*[@id=\"mainBox\"]/main/div[1]/div[1]/div/div[2]/div[1]/div/span[1]")
        except:
            rek = "-"
        try:
            clocktxt = re.search("\d+-\d+-\d+ \d+:\d+:\d+", rek.text)[0]
        except:
            clocktxt = nam[:10]
        removeelement(driver)
        crawlsleep(1)
        clock = clocktxt.replace(":", "_")
        pagetopdf(driver, dircrea, temp_name, nam, articledir, url, Created=clock)
        
        crawlsleep(sleeptime)

        #https://stackoverflow.com/questions/23359083/how-to-convert-webpage-into-pdf-by-using-python
        #https://github.com/JazzCore/python-pdfkit
        # if article_to_jpg_pdf_markdown:
        #     config = pdfkit.configuration(wkhtmltopdf = wkhtmltopdf_path)
        #     pdfkit.from_url(website, os.path.join(dircrea, nam_pinyin+"_.pdf"), configuration = config)
        end = now()
        print("爬取一篇article耗时：", title, round(end - begin, 3))
        logfp.write("爬取一篇article耗时：" +title+" "+ str(round(end - begin, 3)) + "\n")
        numberpage += 1

        # crawlsleep(30)

    allend = now()
    print("平均爬取一篇article耗时：", round((allend - allbegin) / numberpage, 3))
    logfp.write("平均爬取一篇article耗时：" + str(round((allend - allbegin) / numberpage, 3)) + "\n")

def pagetopdf(driver, dircrea, temp_name, nam, destdir, url, Created=""):
    fileexit = os.path.exists(os.path.join(dircrea, temp_name + "_.pdf"))
    if fileexit:
        os.remove(os.path.join(dircrea, temp_name + "_.pdf"))

    printop = PrintOptions()
    printop.shrink_to_fit = True

    # https://css.paperplaza.net/conferences/support/page.php
    # printop.margin_left = 1.9
    # printop.margin_right = 1.32
    # printop.margin_top = 1.9
    # printop.margin_bottom = 3.67
    # printop.page_height = 29.7
    # printop.page_width = 21

    printop.background = True
    printop.scale = 1.0

    try:
        pdf = driver.print_page(print_options=printop)
        with open(os.path.join(dircrea, nam[23:26] + "_.pdf"), 'wb') as obj:
            obj.write(base64.b64decode(pdf))
    except:
        with open(os.path.join(dircrea, nam[23:26] + "_pdf.txt"), 'w') as obj:
            obj.write("the page is too large, can not save, you should save pdf using \"Ctrl+P or Ctrl+Shift+P\"\n")
    
        # driver.execute_script("window.print();")
        # for i in os.listdir(articledir):
        #     if '.pdf' in i:
        #         try:
        #             shutil.move(os.path.join(articledir, i), dircrea)
        #         except:
        #             crawlsleep(10)
        #             try:
        #                 shutil.move(os.path.join(articledir, i), dircrea)
        #             except:
        #                 pass
    
    # driver.execute_script('window.print();')
    clock = Created    #clocktxt.text[3+1:].replace(":", "_")
    with open(os.path.join(dircrea, clock+".txt"), 'w', encoding='utf-8') as obj:
        obj.write(clock+"\n")
        obj.write(url)

    try:
        os.rename(dircrea, os.path.join(destdir, nam))
    except:
        crawlsleep(3+addtime)
        try:
            os.rename(dircrea, os.path.join(destdir, nam))
        except:
            pass

def save_cookie(driverkkk, path):
    #https://stackoverflow.com/questions/45417335/python-use-cookie-to-login-with-selenium
    with open(path, 'wb') as filehandler:
        pickle.dump(driverkkk.get_cookies(), filehandler)

def load_cookie(driverkkk, path):
    #https://stackoverflow.com/questions/45417335/python-use-cookie-to-login-with-selenium
     with open(path, 'rb') as cookiesfile:
         cookies = pickle.load(cookiesfile)
         for cookie in cookies:
             driverkkk.add_cookie(cookie)

def downloaddriver():
    global driverpath
    url = "https://msedgedriver.azureedge.net/116.0.1938.62/edgedriver_win64.zip"
    if not os.path.exists(driverpath):
        ret = requests.get("https://developer.microsoft.com/en-us/microsoft-edge/tools/webdriver/")
        if ret.status_code!=200:
            assert ret.status_code!=200
        ret = BeautifulSoup(ret.content, 'html.parser')
        # divall = ret.find_all('div', class_=r'common-card--lightblue')
        ddl = ret.find_all('a')
        name = "msedgedriver.exe"
        for k in ddl:
            key = k.attrs.keys()
            if 'href' not in key:
                continue
            href = k.attrs['href']
            if 'darwin' not in sys.platform:
                if 'href' in key and "win64" in href and ".zip" in href:
                    url = href
                    break
            elif 'darwin' in sys.platform and 'arm' not in platform.processor():
                if 'href' in key and "mac64" in href and "m1" not in href and ".zip" in href:
                    url = href
                    name = "msedgedriver"
                    break
            elif 'darwin' in sys.platform and 'arm' in platform.processor():
                if 'href' in key and "mac64_m1" in href and ".zip" in href:
                    url = href
                    name = "msedgedriver"
                    break
        response = requests.get(url)
        if response.status_code==200:
            with open(os.path.join(abspath, 'msedgedriver/edgedriver.zip'), 'wb') as obj:
                obj.write(response.content)
            with ZipFile(os.path.join(abspath, 'msedgedriver/edgedriver.zip'), "r") as obj:
                obj.extractall(os.path.join(abspath, 'msedgedriver'))
            nth = os.path.join(abspath, 'msedgedriver')
            for r, d, f in os.walk(nth):
                kk = 6
                for i in f:
                    if 'driver' in i and '.zip' not in i:
                        try:
                            shutil.move(os.path.join(r, i), os.path.join(nth, i))
                        except:
                            pass
                        os.rename(os.path.join(nth, i), os.path.join(nth, name))
                        if 'darwin' in sys.platform:
                            print(f"\n\n请执行权限操作再继续执行：\nchmod +x {os.path.join(nth, name)}\n")
                            exit(0)
                        kk = -6
                        break
                if kk < 0:
                    break

number = 0
def csdn():
    # #crawl articles links
    # downloaddriver()
    global human_verify, number, driverpath
    if number==2:
        return
    try:
        downloaddriver()
        driver = edgeopen(driverpath, articledir)
    except Exception as e:
        if os.path.exists(driverpath):
            os.remove(driverpath)
        downloaddriver()
        driver = edgeopen(driverpath, articledir)
        
    # driver.get(csdn_person_website)
    driver.get(r'https://mp.csdn.net/mp_blog/manage/article')
    try:
        if not os.path.exists(cookie_path):
            assert 1==0
        load_cookie(driver, cookie_path)
        driver.refresh()
        driver.get(r'https://mp.csdn.net/mp_blog/manage/article')
        html = driver.find_element(By.TAG_NAME, "html").text
        if '真人' in html:
            human_verify = True
            number += 1
            driver.quit()
            print("被网站屏蔽了，不允许登录，所以需要采用另一种登录方式，需要额外的磁盘空间，需要用到edge浏览器")
            csdn()
            return

    except Exception as e:
        if os.path.exists(cookie_path):
            os.remove(cookie_path)
            print("浏览器cookie失效了，删除了之前的cookie，需要再次登录并保存cookie。")
        else:
            print("需要登陆并保存cookie，下次就不用登录了。")

        toggle = []
        ti = 1
        while toggle==[] and ti < 600:
            toggle = driver.find_elements(By.CLASS_NAME, "hasAvatar")
            time.sleep(3)
            if ti%10==0:
                print("等待输入账号并点击登录，登录以后请不要执行任何操作，10分钟后自动退出.........")
            ti += 3
        hasAvatar = driver.find_elements(By.CLASS_NAME, "hasAvatar")
        if len(hasAvatar) > 0:
            save_cookie(driver, cookie_path)
            # driver.quit()
            print(f"cookie保存好了的放在了：{cookie_path}")
            crawlsleep(3)
            # print("cookie 已经保存好了的")
            # exit(0)
        else:
            print("还没有登陆的，还请登录保存cookie.......")
            driver.quit()
            exit(0)
        original_window = driver.current_window_handle
        driver.switch_to.new_window('tab')
        new_window = driver.current_window_handle
        driver.switch_to.window(original_window)
        driver.close()
        driver.switch_to.window(new_window)
        # driver.quit()
        # driver = edgeopen(driverpath, articledir)
        crawlsleep(3)
        # driver.get(r'https://passport.csdn.net/login?code=applets')
        driver.get(r'https://mp.csdn.net/mp_blog/manage/article')
        crawlsleep(6)
        html = driver.find_element(By.TAG_NAME, "html").text
        url = driver.current_url
        if '密码登录' in html or 'passport' not in url:
            human_verify = False
        else:
            human_verify = True
        # if not human_verify:
            # login = driver.find_elements(By.CLASS_NAME, "toolbar-btn-loginfun")
            # if len(login)==0:
            #     driver.refresh()
            #     html = driver.find_element(By.TAG_NAME, "html").text
            #     if '正在验证您是否是真人。这可能需要几秒钟时间' in html:
            #         human_verify = True
            #         csdn()
            #         return
            # else:
            #     login = login[0]
            # ActionChains(driver).click(login).perform()
            # WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.CLASS_NAME, r'passport-login-container')))
            # login_box = driver.find_element(By.CLASS_NAME, "passport-login-container")
            # iframe = login_box.find_element(By.TAG_NAME, "iframe")
            # driver.switch_to.frame(iframe)
            # WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.ID, r'sub-frame-error-details')))
            # # document = driver.execute_script("return document")
            # login_error = driver.find_elements(By.ID, r'sub-frame-error-details')
            # if len(login_error)!=0:
            #     human_verify = True
            # driver.switch_to.default_content()
        if human_verify:
            driver.quit()
            number += 1
            print("被网站屏蔽了，不允许登录，所以需要采用另一种登录方式，需要额外的磁盘空间，需要用到edge浏览器")
            csdn()
            return
        crawlsleep(10)
        driver.refresh()
        html = driver.find_element(By.TAG_NAME, "html").text
        if '真人' in html:
            driver.quit()
            human_verify = True
            number += 1
            print("被网站屏蔽了，不允许登录，所以需要采用另一种登录方式，需要额外的磁盘空间，需要用到edge浏览器")
            csdn()
            return
        # WebDriverWait(driver, timeout=60).until(lambda d: len(d.find_elements(By.CLASS_NAME, "toolbar-subMenu-box")) > 1)
        # crawlsleep(100)
        # save_cookie(driver, cookie_path)
        # print("cookie 已经保存好了的")
        # driver.quit()
        # exit(0)

    # driver.get(csdn_person_website)
    if crawl_article:
        if not os.path.exists(os.path.join(articledir, 'article.txt')):
            crawl_article_links(driver)
            logfp.write(nowtime() + ', article weblink爬取已经好了的\n')
        else:
            if crawl_links_scratch:
                os.rename(os.path.join(articledir, 'article.txt'), os.path.join(articledir, 'article_%s.txt'%nowtime()))
                crawl_article_links(driver)
                logfp.write(nowtime() + ', article weblink爬取已经好了的\n')
            else:
                pass
        crawl_article_detail(driver)
        logfp.write(nowtime() + ', article爬取已经好了的\n')
    driver.quit()

if __name__ == "__main__":
    #version four.one_zero.zero
    if 'darwin' not in sys.platform:
        driverpath = os.path.join(abspath, 'msedgedriver' +os.sep + 'msedgedriver.exe')
    else:
        driverpath = os.path.join(abspath, 'msedgedriver' +os.sep + 'msedgedriver')
    savepath = deepcopy(abspath)
    verify_txt = os.path.join(savepath, r'verify.txt')
    human_verify = False
    if os.path.exists(verify_txt):
        with open(verify_txt, 'r', encoding='utf-8') as obj:
            k = obj.readline()
            if '0' in k or 'n' in k or 'N' in k or len(k)==0:
                human_verify = False
            else:
                human_verify = True
    else:
        with open(verify_txt, 'w', encoding='utf-8') as obj:
            obj.write("0\n")
    cookiedir = os.path.join(savepath, 'cookie')
    articledir = os.path.join(savepath, 'article')
    logdir = os.path.join(savepath, 'log')
    logfile = os.path.join(logdir, nowtime() + '_log.txt')
    os.makedirs(cookiedir, exist_ok=True)
    os.makedirs(articledir,   exist_ok=True)
    os.makedirs(logdir,   exist_ok=True)
    logfp = open(logfile, 'w', encoding='utf-8')
    cookie_path =os.path.join(cookiedir, 'cookie_csdn.pkl')
    
    parser = argparse.ArgumentParser(description=r'crawler zhihu.com, 爬取CSDN的想法, 回答, 文章, 包括数学公式')
    parser.add_argument('--csdn_person_website', type=str, \
                        default = r'https://blog.csdn.net/m0_50617544?type=blog', \
                        help=r'')
    parser.add_argument('--sleep_time', type=float, default = 6, \
                        help=r'crawler sleep time during crawling, 爬取时的睡眠时间, 避免给CSDN服务器带来太大压力, \
                        可以日间调试好，然后深夜运行爬取人少, 给其他小伙伴更好的用户体验, 避免CSDN顺着网线过来找人, 默认: 6s')
    # parser.add_argument('--formula_time', type=float, default=0.6-0.2, \
    #                     help=r'crawler math formula sleep time,default:0.6-0.2, 爬取数学公式页面, 需要的sleep时间, 默认0.6-0.2')
    parser.add_argument('--computer_time_sleep', type=float, default=0, \
                        help=r'computer running sleep time 默认:0, 电脑运行速度的sleep时间, 默认:0')
    parser.add_argument('--article', action="store_true", help=r'crawl article, 是否爬取CSDN的文章, 保存到pdf、markdown以及相关图片等，已经爬取过的不会重复爬取，\
                    断了再次爬取的话，可以配置到--links_scratch，事先保存好website')
    # parser.add_argument('--article_to_jpg_pdf_markdown', action="store_true", help=r'save article to pdf, 文章保存到pdf和markdown以及图片等')
    parser.add_argument('--MarkDown', action="store_true", help=r'save MarkDown')
    parser.add_argument('--links_scratch', action="store_true", \
                        help=r'crawl links scratch for answer or article, 是否使用已经保存好的website和title, 否则再次爬取website')
    args = parser.parse_args()
    sleeptime = args.sleep_time
    crawl_article = args.article
    crawl_links_scratch = args.links_scratch
    # article_to_jpg_pdf_markdown = args.article_to_jpg_pdf_markdown
    addtime = args.computer_time_sleep
    csdn_person_website = args.csdn_person_website
    MarkDown_FORMAT = args.MarkDown
    
    crawl_article = True
    MarkDown_FORMAT = True
    # crawl_links_scratch = True
    # python crawler.py --article --MarkDown --links_scratch
    csdn()
    logfp.close()
