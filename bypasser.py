import re
from re import match as rematch, findall, sub as resub
import requests
from requests import get as rget
import base64
from urllib.parse import unquote, urlparse, parse_qs, quote
import time
import cloudscraper
from bs4 import BeautifulSoup, NavigableString, Tag
from lxml import etree
import hashlib
import json
from dotenv import load_dotenv
load_dotenv()
from asyncio import sleep as asleep
import os
import ddl


##########################################################
# ENVs

GDTot_Crypt = os.environ.get("CRYPT","b0lDek5LSCt6ZjVRR2EwZnY4T1EvVndqeDRtbCtTWmMwcGNuKy8wYWpDaz0%3D")
Laravel_Session = os.environ.get("Laravel_Session","")
XSRF_TOKEN = os.environ.get("XSRF_TOKEN","")
KCRYPT = os.environ.get("KOLOP_CRYPT","aWFicnVaNWh4TThRbzFqdkE2U2FKNmJOTWhvWkZmbWswaUFadTB5NXJ3RT0%3D")
HCRYPT = os.environ.get("HUBDRIVE_CRYPT","Q29hdlpLUEZTSEJLUjVZRkZQSExLODFuWGVudUlNK0ZPZlZmS1hENWxZVT0%3D")



############################################################
# Lists

otherslist = ["exe.io","exey.io","sub2unlock.net","sub2unlock.com","rekonise.com","letsboost.net","ph.apps2app.com","mboost.me",
"sub4unlock.com","ytsubme.com","social-unlock.com","boost.ink","goo.gl","shrto.ml","t.co"]

gdlist = ["appdrive","driveapp","drivehub","gdflix","drivesharer","drivebit","drivelinks","driveace",
"drivepro","driveseed"]


###############################################################
# index scrapper

def scrapeIndex(url, username="none", password="none"):

    def authorization_token(username, password):
        user_pass = f"{username}:{password}"
        return f"Basic {base64.b64encode(user_pass.encode()).decode()}"

          
    def decrypt(string): 
        return base64.b64decode(string[::-1][24:-20]).decode('utf-8')  

    
    def func(payload_input, url, username, password): 
        next_page = False
        next_page_token = "" 

        url = f"{url}/" if url[-1] != '/' else url

        try: headers = {"authorization":authorization_token(username,password)}
        except: return "username/password combination is wrong", None, None

        encrypted_response = requests.post(url, data=payload_input, headers=headers)
        if encrypted_response.status_code == 401: return "username/password combination is wrong", None, None

        try: decrypted_response = json.loads(decrypt(encrypted_response.text))
        except: return "something went wrong. check index link/username/password field again", None, None

        page_token = decrypted_response["nextPageToken"]
        if page_token is None: 
            next_page = False
        else: 
            next_page = True 
            next_page_token = page_token 


        if list(decrypted_response.get("data").keys())[0] != "error":
            file_length = len(decrypted_response["data"]["files"])
            result = ""

            for i, _ in enumerate(range(file_length)):
                files_type   = decrypted_response["data"]["files"][i]["mimeType"]
                if files_type != "application/vnd.google-apps.folder":
                        files_name   = decrypted_response["data"]["files"][i]["name"] 

                        direct_download_link = url + quote(files_name)
                        result += f"• {files_name} :\n{direct_download_link}\n\n"
            return result, next_page, next_page_token

    def format(result):
        long_string = ''.join(result)
        new_list = []

        while len(long_string) > 0:
            if len(long_string) > 4000:
                split_index = long_string.rfind("\n\n", 0, 4000)
                if split_index == -1:
                    split_index = 4000
            else:
                split_index = len(long_string)
                
            new_list.append(long_string[:split_index])
            long_string = long_string[split_index:].lstrip("\n\n")
        
        return new_list

    # main
    x = 0
    next_page = False
    next_page_token = "" 
    result = []

    payload = {"page_token":next_page_token, "page_index": x}	
    print(f"Index Link: {url}\n")
    temp, next_page, next_page_token = func(payload, url, username, password)
    if temp is not None: result.append(temp)
    
    while next_page == True:
        payload = {"page_token":next_page_token, "page_index": x}
        temp, next_page, next_page_token = func(payload, url, username, password)
        if temp is not None: result.append(temp)
        x += 1
        
    if len(result)==0: return None
    return format(result)


##############################################################
# 


###############################################################
# 
##################################################################################################################
# 

###############################################################
# htpmovies cinevood sharespark atishmkv

def htpmovies(link):
    client = cloudscraper.create_scraper(allow_brotli=False)
    r = client.get(link, allow_redirects=True).text
    j = r.split('("')[-1]
    url = j.split('")')[0]
    param = url.split("/")[-1]
    DOMAIN = "https://go.theforyou.in"
    final_url = f"{DOMAIN}/{param}"
    resp = client.get(final_url)
    soup = BeautifulSoup(resp.content, "html.parser")    
    try: inputs = soup.find(id="go-link").find_all(name="input")
    except: return "Incorrect Link"
    data = { input.get('name'): input.get('value') for input in inputs }
    h = { "x-requested-with": "XMLHttpRequest" }
    time.sleep(10)
    r = client.post(f"{DOMAIN}/links/go", data=data, headers=h)
    try:
        return r.json()['url']
    except: return "Something went Wrong !!"


def scrappers(link):
 
    try: link = rematch(r"((http|https)\:\/\/)?[a-zA-Z0-9\.\/\?\:@\-_=#]+\.([a-zA-Z]){2,6}([a-zA-Z0-9\.\&\/\?\:@\-_=#])*", link)[0]
    except TypeError: return 'Not a Valid Link.'
    links = []

    if "sharespark" in link:
        gd_txt = ""
        res = rget("?action=printpage;".join(link.split('?')))
        soup = BeautifulSoup(res.text, 'html.parser')
        for br in soup.findAll('br'):
            next_s = br.nextSibling
            if not (next_s and isinstance(next_s,NavigableString)):
                continue
            next2_s = next_s.nextSibling
            if next2_s and isinstance(next2_s,Tag) and next2_s.name == 'br':
              text = str(next_s).strip()
              if text:
                  result = resub(r'(?m)^\(https://i.*', '', next_s)
                  star = resub(r'(?m)^\*.*', ' ', result)
                  extra = resub(r'(?m)^\(https://e.*', ' ', star)
                  gd_txt += ', '.join(findall(r'(?m)^.*https://new1.gdtot.cfd/file/[0-9][^.]*', next_s)) + "\n\n"
        return gd_txt
  
    elif "htpmovies" in link and "/exit.php" in link:
        return htpmovies(link)
        
    elif "htpmovies" in link:
        prsd = ""
        links = []
        res = rget(link)
        soup = BeautifulSoup(res.text, 'html.parser')
        x = soup.select('a[href^="/exit.php?url="]')
        y = soup.select('h5')
        z = unquote(link.split('/')[-2]).split('-')[0] if link.endswith('/') else unquote(link.split('/')[-1]).split('-')[0]

        for a in x:
            links.append(a['href'])
            prsd = f"Total Links Found : {len(links)}\n\n"
      
        msdcnt = -1
        for b in y:
            if str(b.string).lower().startswith(z.lower()):
                msdcnt += 1
                url = f"https://htpmovies.lol"+links[msdcnt]
                prsd += f"{msdcnt+1}. <b>{b.string}</b>\n{htpmovies(url)}\n\n"
                asleep(5)
        return prsd

    elif "cinevood" in link:
        prsd = ""
        links = []
        res = rget(link)
        soup = BeautifulSoup(res.text, 'html.parser')
        x = soup.select('a[href^="https://kolop.icu/file"]')
        for a in x:
            links.append(a['href'])
        for o in links:
            res = rget(o)
            soup = BeautifulSoup(res.content, "html.parser")
            title = soup.title.string
            reftxt = resub(r'Kolop \| ', '', title)
            prsd += f'{reftxt}\n{o}\n\n'
        return prsd

    elif "atishmkv" in link:
        prsd = ""
        links = []
        res = rget(link)
        soup = BeautifulSoup(res.text, 'html.parser')
        x = soup.select('a[href^="https://gdflix.top/file"]')
        for a in x:
            links.append(a['href'])
        for o in links:
            prsd += o + '\n\n'
        return prsd

    elif "teluguflix" in link:
        gd_txt = ""
        r = rget(link)
        soup = BeautifulSoup (r.text, "html.parser")
        links = soup.select('a[href*="gdtot"]')
        gd_txt = f"Total Links Found : {len(links)}\n\n"
        for no, link in enumerate(links, start=1):
            gdlk = link['href']
            t = rget(gdlk)
            soupt = BeautifulSoup(t.text, "html.parser")
            title = soupt.select('meta[property^="og:description"]')
            gd_txt += f"{no}. <code>{(title[0]['content']).replace('Download ' , '')}</code>\n{gdlk}\n\n"
            asleep(1.5)
        return gd_txt
    
    elif "taemovies" in link:
        gd_txt, no = "", 0
        r = rget(link)
        soup = BeautifulSoup (r.text, "html.parser")
        links = soup.select('a[href*="shortingly"]')
        gd_txt = f"Total Links Found : {len(links)}\n\n"
        for a in links:
            glink = rocklinks(a["href"]) 
            t = rget(glink)
            soupt = BeautifulSoup(t.text, "html.parser")
            title = soupt.select('meta[property^="og:description"]')
            no += 1
            gd_txt += f"{no}. {(title[0]['content']).replace('Download ' , '')}\n{glink}\n\n"
        return gd_txt
    
    elif "toonworld4all" in link:
        gd_txt, no = "", 0
        r = rget(link)
        soup = BeautifulSoup(r.text, "html.parser")
        links = soup.select('a[href*="redirect/main.php?"]')
        for a in links:
            down = rget(a['href'], stream=True, allow_redirects=False)


###################################################
# script links

def getfinal(domain, url, sess):

    #sess = requests.session()
    res = sess.get(url)
    soup = BeautifulSoup(res.text,"html.parser")
    soup = soup.find("form").findAll("input")
    datalist = []
    for ele in soup:
        datalist.append(ele.get("value"))

    data = {
            '_method': datalist[0],
            '_csrfToken': datalist[1],
            'ad_form_data': datalist[2],
            '_Token[fields]': datalist[3],
            '_Token[unlocked]': datalist[4],
        }

    sess.headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:103.0) Gecko/20100101 Firefox/103.0',
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Accept-Language': 'en-US,en;q=0.5',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'X-Requested-With': 'XMLHttpRequest',
            'Origin': domain,
            'Connection': 'keep-alive',
            'Referer': url,
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            }

    # print("waiting 10 secs")
    time.sleep(10) # important
    response = sess.post(domain+'/links/go', data=data).json()
    furl = response["url"]
    return furl


def getfirst(url):

    sess = requests.session()
    res = sess.get(url)

    soup = BeautifulSoup(res.text,"html.parser")
    soup = soup.find("form")
    action = soup.get("action")
    soup = soup.findAll("input")
    datalist = []
    for ele in soup:
        datalist.append(ele.get("value"))
    sess.headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:103.0) Gecko/20100101 Firefox/103.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Origin': action,
        'Connection': 'keep-alive',
        'Referer': action,
        'Upgrade-Insecure-Requests': '1',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-User': '?1',
    }

    data = {'newwpsafelink': datalist[1], "g-recaptcha-response": RecaptchaV3()}
    response = sess.post(action, data=data)
    soup = BeautifulSoup(response.text, "html.parser")
    soup = soup.findAll("div", class_="wpsafe-bottom text-center")
    for ele in soup:
        rurl = ele.find("a").get("onclick")[13:-12]

    res = sess.get(rurl)
    furl = res.url
    # print(furl)
    return getfinal(f'https://{furl.split("/")[-2]}/',furl,sess)


####################################################################################################
# 



###############################################
# hubdrive

def parse_info_hubdrive(res):
    info_parsed = {}
    title = re.findall('>(.*?)<\/h4>', res.text)[0]
    info_chunks = re.findall('>(.*?)<\/td>', res.text)
    info_parsed['title'] = title
    for i in range(0, len(info_chunks), 2):
        info_parsed[info_chunks[i]] = info_chunks[i+1]
    return info_parsed

def hubdrive_dl(url,hcrypt):
    client = requests.Session()
    client.cookies.update({'crypt': hcrypt})
    
    res = client.get(url)
    info_parsed = parse_info_hubdrive(res)
    info_parsed['error'] = False
    
    up = urlparse(url)
    req_url = f"{up.scheme}://{up.netloc}/ajax.php?ajax=download"
    
    file_id = url.split('/')[-1]
    data = { 'id': file_id }
    headers = {'x-requested-with': 'XMLHttpRequest'}
    
    try:
        res = client.post(req_url, headers=headers, data=data).json()['file']
    except:
        return "Error"#{'error': True, 'src_url': url}
    
    gd_id = re.findall('gd=(.*)', res, re.DOTALL)[0]
    info_parsed['gdrive_url'] = f"https://drive.google.com/open?id={gd_id}"
    info_parsed['src_url'] = url
    return info_parsed['gdrive_url']


##################################################
# kolop

def parse_info_kolop(res):
    info_parsed = {}
    title = re.findall('>(.*?)<\/h4>', res.text)[0]
    info_chunks = re.findall('>(.*?)<\/td>', res.text)
    info_parsed['title'] = title
    for i in range(0, len(info_chunks), 2):
        info_parsed[info_chunks[i]] = info_chunks[i+1]
    return info_parsed

def kolop_dl(url,kcrypt):
    client = requests.Session()
    client.cookies.update({'crypt': kcrypt})
    
    res = client.get(url)
    info_parsed = parse_info_kolop(res)
    info_parsed['error'] = False
    
    up = urlparse(url)
    req_url = f"{up.scheme}://{up.netloc}/ajax.php?ajax=download"
    
    file_id = url.split('/')[-1]
    data = { 'id': file_id }
    headers = { 'x-requested-with': 'XMLHttpRequest'}
    
    try:
        res = client.post(req_url, headers=headers, data=data).json()['file']
    except:

####################################################



####################################################
# filercrypt


#####################################################

######################################################


#######################################################
# shortingly

# short2url


#######################################################




############################################################


############################################################

#############################################################
# gofile

def gofile_dl(url,password=""):
    api_uri = 'https://api.gofile.io'
    client = requests.Session()
    res = client.get(api_uri+'/createAccount').json()
    
    data = {
        'contentId': url.split('/')[-1],
        'token': res['data']['token'],
        'websiteToken': '12345',
        'cache': 'true',
        'password': hashlib.sha256(password.encode('utf-8')).hexdigest()
    }
    res = client.get(api_uri+'/getContent', params=data).json()

    content = []
    for item in res['data']['contents'].values():
        content.append(item)
    
    return {
        'accountToken': data['token'],
        'files': content
    }["files"][0]["link"]


################################################################

#################################################################
# gdtot

def gdtot(url: str, GdTot_Crypt: str) -> str:
    client = requests.Session()
    client.cookies.update({"crypt": GdTot_Crypt})
    res = client.get(url)
    base_url = re.match('^.+?[^\/:](?=[?\/]|$\n)', url).group(0)
    res = client.get(f"{base_url}/dld?id={url.split('/')[-1]}")
    url = re.findall(r'URL=(.*?)"', res.text)[0]
    info = {}
    info["error"] = False
    params = parse_qs(urlparse(url).query)
    if "gd" not in params or not params["gd"] or params["gd"][0] == "false":
        info["error"] = True
        if "msgx" in params:
            info["message"] = params["msgx"][0]
        else:
            info["message"] = "Invalid link"
    else:
        decoded_id = base64.b64decode(str(params["gd"][0])).decode("utf-8")
        drive_link = f"https://drive.google.com/open?id={decoded_id}"
        info["gdrive_link"] = drive_link
    if not info["error"]: return info["gdrive_link"]
    else: return ddl.gdtot(url)


##################################################################

######################################################################################################
#

####################################################################################################################        
# mdisk

def mdisk(url):
    header = {
        'Accept': '*/*',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate, br',
        'Referer': 'https://mdisk.me/',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36'
    	 }
    
    inp = url 
    fxl = inp.split("/")
    cid = fxl[-1]

    URL = f'https://diskuploader.entertainvideo.com/v1/file/cdnurl?param={cid}'
    res = requests.get(url=URL, headers=header).json()
    return res['download'] + '\n\n' + res['source']


##################################################################################################################        
# AppDrive or DriveApp etc. Look-Alike Link and as well as the Account Details (Required for Login Required Links only)

def unified(url):

    if ddl.is_share_link(url):
        if 'https://gdtot' in url: return ddl.gdtot(url)
        else: return ddl.sharer_scraper(url)

    try:
        Email = ""
        Password = ""

        account = {"email": Email, "passwd": Password}
        client = cloudscraper.create_scraper(allow_brotli=False)
        client.headers.update(
            {
                "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36"
            }
        )
        data = {"email": account["email"], "password": account["passwd"]}
        client.post(f"https://{urlparse(url).netloc}/login", data=data)
        res = client.get(url)
        key = re.findall('"key",\s+"(.*?)"', res.text)[0]
        ddl_btn = etree.HTML(res.content).xpath("//button[@id='drc']")
        info = re.findall(">(.*?)<\/li>", res.text)
        info_parsed = {}
        for item in info:
            kv = [s.strip() for s in item.split(":", maxsplit=1)]
            info_parsed[kv[0].lower()] = kv[1]
        info_parsed = info_parsed
        info_parsed["error"] = False
        info_parsed["link_type"] = "login"
        headers = {
            "Content-Type": f"multipart/form-data; boundary={'-'*4}_",
        }
        data = {"type": 1, "key": key, "action": "original"}
        if len(ddl_btn):
            info_parsed["link_type"] = "direct"
            data["action"] = "direct"
        while data["type"] <= 3:
            boundary = f'{"-"*6}_'
            data_string = ""
            for item in data:
                data_string += f"{boundary}\r\n"
                data_string += f'Content-Disposition: form-data; name="{item}"\r\n\r\n{data[item]}\r\n'
            data_string += f"{boundary}--\r\n"
            gen_payload = data_string
            try:
                response = client.post(url, data=gen_payload, headers=headers).json()
                break
            except BaseException:
                data["type"] += 1
        if "url" in response:
            info_parsed["gdrive_link"] = response["url"]
        elif "error" in response and response["error"]:
            info_parsed["error"] = True
            info_parsed["error_message"] = response["message"]
        else:
            info_parsed["error"] = True
            info_parsed["error_message"] = "Something went wrong :("
        if info_parsed["error"]:
            return info_parsed
        if "driveapp" in urlparse(url).netloc and not info_parsed["error"]:
            res = client.get(info_parsed["gdrive_link"])
            drive_link = etree.HTML(res.content).xpath(
                "//a[contains(@class,'btn')]/@href"
            )[0]
            info_parsed["gdrive_link"] = drive_link
        info_parsed["src_url"] = url
        if "drivehub" in urlparse(url).netloc and not info_parsed["error"]:
            res = client.get(info_parsed["gdrive_link"])
            drive_link = etree.HTML(res.content).xpath(
                "//a[contains(@class,'btn')]/@href"
            )[0]
            info_parsed["gdrive_link"] = drive_link
        if "gdflix" in urlparse(url).netloc and not info_parsed["error"]:
            res = client.get(info_parsed["gdrive_link"])
            drive_link = etree.HTML(res.content).xpath(
                "//a[contains(@class,'btn')]/@href"
            )[0]
            info_parsed["gdrive_link"] = drive_link

        if "drivesharer" in urlparse(url).netloc and not info_parsed["error"]:
            res = client.get(info_parsed["gdrive_link"])
            drive_link = etree.HTML(res.content).xpath(
                "//a[contains(@class,'btn')]/@href"
            )[0]
            info_parsed["gdrive_link"] = drive_link
        if "drivebit" in urlparse(url).netloc and not info_parsed["error"]:
            res = client.get(info_parsed["gdrive_link"])
            drive_link = etree.HTML(res.content).xpath(
                "//a[contains(@class,'btn')]/@href"
            )[0]
            info_parsed["gdrive_link"] = drive_link
        if "drivelinks" in urlparse(url).netloc and not info_parsed["error"]:
            res = client.get(info_parsed["gdrive_link"])
            drive_link = etree.HTML(res.content).xpath(
                "//a[contains(@class,'btn')]/@href"
            )[0]
            info_parsed["gdrive_link"] = drive_link
        if "driveace" in urlparse(url).netloc and not info_parsed["error"]:
            res = client.get(info_parsed["gdrive_link"])
            drive_link = etree.HTML(res.content).xpath(
                "//a[contains(@class,'btn')]/@href"
            )[0]
            info_parsed["gdrive_link"] = drive_link
        if "drivepro" in urlparse(url).netloc and not info_parsed["error"]:
            res = client.get(info_parsed["gdrive_link"])
            drive_link = etree.HTML(res.content).xpath(
                "//a[contains(@class,'btn')]/@href"
            )[0]
            info_parsed["gdrive_link"] = drive_link
        if info_parsed["error"]:
            return "Faced an Unknown Error!"
        return info_parsed["gdrive_link"]
    except BaseException:
        return "Unable to Extract GDrive Link"


#####################################################################################################
####################################################################################################
# helpers

# check if present in list
def ispresent(inlist,url):
    for ele in inlist:
        if ele in url:
            return True
    return False
