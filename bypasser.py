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
# tnlink

def tnlink(url):
    client = requests.session()
    DOMAIN = "https://internet.usanewstoday.club"
    url = url[:-1] if url[-1] == '/' else url
    code = url.split("/")[-1]
    final_url = f"{DOMAIN}/{code}"
    ref = "https://usanewstoday.club/"
    h = {"referer": ref}
    while len(client.cookies) == 0:
        resp = client.get(final_url,headers=h)
        time.sleep(2)
    soup = BeautifulSoup(resp.content, "html.parser")
    inputs = soup.find_all("input")
    data = { input.get('name'): input.get('value') for input in inputs }
    h = { "x-requested-with": "XMLHttpRequest" }
    time.sleep(8)
    r = client.post(f"{DOMAIN}/links/go", data=data, headers=h)
    try: return r.json()['url']
    except: return "Something went wrong :("


###############################################################
# psa 

def try2link_bypass(url):
	client = cloudscraper.create_scraper(allow_brotli=False)
	
	url = url[:-1] if url[-1] == '/' else url
	
	params = (('d', int(time.time()) + (60 * 4)),)
	r = client.get(url, params=params, headers= {'Referer': 'https://newforex.online/'})
	
	soup = BeautifulSoup(r.text, 'html.parser')
	inputs = soup.find(id="go-link").find_all(name="input")
	data = { input.get('name'): input.get('value') for input in inputs }	
	time.sleep(7)
	
	headers = {'Host': 'try2link.com', 'X-Requested-With': 'XMLHttpRequest', 'Origin': 'https://try2link.com', 'Referer': url}
	
	bypassed_url = client.post('https://try2link.com/links/go', headers=headers,data=data)
	return bypassed_url.json()["url"]
		

def try2link_scrape(url):
	client = cloudscraper.create_scraper(allow_brotli=False)	
	h = {
	'upgrade-insecure-requests': '1', 'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36',
	}
	res = client.get(url, cookies={}, headers=h)
	url = 'https://try2link.com/'+re.findall('try2link\.com\/(.*?) ', res.text)[0]
	return try2link_bypass(url)
    

def psa_bypasser(psa_url):
    client = cloudscraper.create_scraper(allow_brotli=False)
    r = client.get(psa_url)
    soup = BeautifulSoup(r.text, "html.parser").find_all(class_="dropshadowboxes-drop-shadow dropshadowboxes-rounded-corners dropshadowboxes-inside-and-outside-shadow dropshadowboxes-lifted-both dropshadowboxes-effect-default")
    links = ""
    for link in soup:
        try:
            exit_gate = link.a.get("href")
            links = links + try2link_scrape(exit_gate) + '\n'
        except: pass
    return links


##################################################################################################################
# rocklinks

def rocklinks(url):
    client = cloudscraper.create_scraper(allow_brotli=False)
    if 'rocklinks.net' in url:
        DOMAIN = "https://blog.disheye.com"
    else:
        DOMAIN = "https://rocklinks.net"

    url = url[:-1] if url[-1] == '/' else url

    code = url.split("/")[-1]
    if 'rocklinks.net' in url:
        final_url = f"{DOMAIN}/{code}?quelle=" 
    else:
        final_url = f"{DOMAIN}/{code}"

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
    except: return "Something went wrong :("


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
            link = down.headers["location"]
            glink = rocklinks(link)
            if glink and "gdtot" in glink:
                t = rget(glink)
                soupt = BeautifulSoup(t.text, "html.parser")
                title = soupt.select('meta[property^="og:description"]')
                no += 1
                gd_txt += f"{no}. {(title[0]['content']).replace('Download ' , '')}\n{glink}\n\n"
        return gd_txt
    
    elif "animeremux" in link:
        gd_txt, no = "", 0
        r = rget(link)
        soup = BeautifulSoup (r.text, "html.parser")
        links = soup.select('a[href*="urlshortx.com"]')
        gd_txt = f"Total Links Found : {len(links)}\n\n"
        for a in links:
            link = a["href"]
            x = link.split("url=")[-1]
            t = rget(x)
            soupt = BeautifulSoup(t.text, "html.parser")
            title = soupt.title
            no += 1
            gd_txt += f"{no}. {title.text}\n{x}\n\n"
            asleep(1.5)
        return gd_txt

    else:
        res = rget(link)
        soup = BeautifulSoup(res.text, 'html.parser')
        mystx = soup.select(r'a[href^="magnet:?xt=urn:btih:"]')
        for hy in mystx:
            links.append(hy['href'])
        return links


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
# ez4short

def ez4(url):
    client = cloudscraper.create_scraper(allow_brotli=False)
    DOMAIN = "https://ez4short.com"
    ref = "https://techmody.io/"
    h = {"referer": ref}
    resp = client.get(url,headers=h)
    soup = BeautifulSoup(resp.content, "html.parser")
    inputs = soup.find_all("input")
    data = { input.get('name'): input.get('value') for input in inputs }
    h = { "x-requested-with": "XMLHttpRequest" }
    time.sleep(8)
    r = client.post(f"{DOMAIN}/links/go", data=data, headers=h)
    try: return r.json()['url']
    except: return "Something went wrong :("



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
        return "Error"#{'error': True, 'src_url': url}
    
    gd_id = re.findall('gd=(.*)', res, re.DOTALL)[0]
    info_parsed['gdrive_url'] = f"https://drive.google.com/open?id={gd_id}"
    info_parsed['src_url'] = url

    return info_parsed['gdrive_url']


##################################################
# mediafire

def mediafire(url):

    res = requests.get(url, stream=True)
    contents = res.text

    for line in contents.splitlines():
        m = re.search(r'href="((http|https)://download[^"]+)', line)
        if m:
            return m.groups()[0]


####################################################
# zippyshare

def zippyshare(url):
    resp = requests.get(url).text
    surl = resp.split("document.getElementById('dlbutton').href = ")[1].split(";")[0]
    parts = surl.split("(")[1].split(")")[0].split(" ")
    val = str(int(parts[0]) % int(parts[2]) + int(parts[4]) % int(parts[6]))
    surl = surl.split('"')
    burl = url.split("zippyshare.com")[0]
    furl = burl + "zippyshare.com" + surl[1] + val + surl[-2]
    return furl


####################################################
# filercrypt

def getlinks(dlc,client):
    headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:103.0) Gecko/20100101 Firefox/103.0',
    'Accept': 'application/json, text/javascript, */*',
    'Accept-Language': 'en-US,en;q=0.5',
    'X-Requested-With': 'XMLHttpRequest',
    'Origin': 'http://dcrypt.it',
    'Connection': 'keep-alive',
    'Referer': 'http://dcrypt.it/',
    }

    data = {
        'content': dlc,
    }

    response = client.post('http://dcrypt.it/decrypt/paste', headers=headers, data=data).json()["success"]["links"]
    links = ""
    for link in response:
        links = links + link + "\n"
    return links[:-1]


def filecrypt(url):

    client = cloudscraper.create_scraper(allow_brotli=False)
    headers = {
    "authority": "filecrypt.co",
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "accept-language": "en-US,en;q=0.9",
    "cache-control": "max-age=0",
    "content-type": "application/x-www-form-urlencoded",
    "dnt": "1",
    "origin": "https://filecrypt.co",
    "referer": url,
    "sec-ch-ua": '"Google Chrome";v="105", "Not)A;Brand";v="8", "Chromium";v="105"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "Windows",
    "sec-fetch-dest": "document",
    "sec-fetch-mode": "navigate",
    "sec-fetch-site": "same-origin",
    "sec-fetch-user": "?1",
    "upgrade-insecure-requests": "1",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36" 
    }
    

    resp = client.get(url, headers=headers)
    soup = BeautifulSoup(resp.content, "html.parser")

    buttons = soup.find_all("button")
    for ele in buttons:
        line = ele.get("onclick")
        if line !=None and "DownloadDLC" in line:
            dlclink = "https://filecrypt.co/DLC/" + line.split("DownloadDLC('")[1].split("'")[0] + ".html"
            break

    resp = client.get(dlclink,headers=headers)
    return getlinks(resp.text,client)


#####################################################
# dropbox

def dropbox(url):
    return url.replace("www.","").replace("dropbox.com","dl.dropboxusercontent.com").replace("?dl=0","")


######################################################
# shareus

def shareus(url):
    token = url.split("=")[-1]
    bypassed_url = "https://us-central1-my-apps-server.cloudfunctions.net/r?shortid="+ token
    response = requests.get(bypassed_url).text
    return response


#######################################################
# shortingly

def shortingly(url):
    client = cloudscraper.create_scraper(allow_brotli=False)
    DOMAIN = "https://shortingly.in"
    url = url[:-1] if url[-1] == '/' else url
    code = url.split("/")[-1]
    final_url = f"{DOMAIN}/{code}"
    ref = "https://tech.gyanitheme.com/"
    h = {"referer": ref}
    resp = client.get(final_url,headers=h)
    soup = BeautifulSoup(resp.content, "html.parser")
    inputs = soup.find_all("input")
    data = { input.get('name'): input.get('value') for input in inputs }
    h = { "x-requested-with": "XMLHttpRequest" }
    time.sleep(5)
    r = client.post(f"{DOMAIN}/links/go", data=data, headers=h)
    try: return r.json()['url']
    except: return "Something went wrong :("

#######################################################
# Gyanilinks - gtlinks.me

def gyanilinks(url):
    DOMAIN = "https://go.theforyou.in/"
    client = cloudscraper.create_scraper(allow_brotli=False)
    url = url[:-1] if url[-1] == '/' else url
    code = url.split("/")[-1]
    final_url = f"{DOMAIN}/{code}"
    resp = client.get(final_url)
    soup = BeautifulSoup(resp.content, "html.parser")
    try: inputs = soup.find(id="go-link").find_all(name="input")
    except: return "Incorrect Link"
    data = { input.get('name'): input.get('value') for input in inputs }
    h = { "x-requested-with": "XMLHttpRequest" }
    time.sleep(5)
    r = client.post(f"{DOMAIN}/links/go", data=data, headers=h)
    try: return r.json()['url']
    except: return "Something went wrong :("


#######################################################
# Flashlink

def flashlink(url):
  DOMAIN = "https://files.cordtpoint.co.in"
  url = url[:-1] if url[-1] == '/' else url
  code = url.split("/")[-1]
  final_url = f"{DOMAIN}/{code}"
  client = cloudscraper.create_scraper(allow_brotli=False)
  resp = client.get(final_url)
  soup = BeautifulSoup(resp.content, "html.parser")
  inputs = soup.find(id="go-link").find_all(name="input")
  data = { input.get('name'): input.get('value') for input in inputs }
  h = { "x-requested-with": "XMLHttpRequest" }
  time.sleep(15)
  r = client.post(f"{DOMAIN}/links/go", data=data, headers=h)
  return r.json()['url']


#######################################################
# short2url

def short2url(url):
    client = cloudscraper.create_scraper(allow_brotli=False)
    DOMAIN = "https://techyuth.xyz/blog"
    url = url[:-1] if url[-1] == '/' else url
    code = url.split("/")[-1]
    final_url = f"{DOMAIN}/{code}"
    ref = "https://blog.coin2pay.xyz/"
    h = {"referer": ref}
    resp = client.get(final_url, headers=h)
    soup = BeautifulSoup(resp.content, "html.parser")
    inputs = soup.find_all("input")
    data = { input.get('name'): input.get('value') for input in inputs }
    h = { "x-requested-with": "XMLHttpRequest" }
    time.sleep(10)
    r = client.post(f"{DOMAIN}/links/go", data=data, headers=h)
    try:
        return r.json()['url']
    except: return "Something went wrong :("


#######################################################
# anonfiles

def anonfile(url):

    headersList = { "Accept": "*/*"}
    payload = ""

    response = requests.request("GET", url, data=payload,  headers=headersList).text.split("\n")
    for ele in response:
        if "https://cdn" in ele and "anonfiles.com" in ele and url.split("/")[-2] in ele:
            break

    return ele.split('href="')[1].split('"')[0]


##########################################################
# pixl

def pixl(url):
    count = 1
    dl_msg = ""
    currentpage = 1
    settotalimgs = True
    totalimages = ""
    client = cloudscraper.create_scraper(allow_brotli=False)
    resp = client.get(url)
    if resp.status_code == 404:
        return "File not found/The link you entered is wrong!"
    soup = BeautifulSoup(resp.content, "html.parser")
    if "album" in url and settotalimgs:
        totalimages = soup.find("span", {"data-text": "image-count"}).text
        settotalimgs = False
    thmbnailanch = soup.findAll(attrs={"class": "--media"})
    links = soup.findAll(attrs={"data-pagination": "next"})
    try:
        url = links[0].attrs["href"]
    except BaseException:
        url = None
    for ref in thmbnailanch:
        imgdata = client.get(ref.attrs["href"])
        if not imgdata.status_code == 200:
            time.sleep(5)
            continue
        imghtml = BeautifulSoup(imgdata.text, "html.parser")
        downloadanch = imghtml.find(attrs={"class": "btn-download"})
        currentimg = downloadanch.attrs["href"]
        currentimg = currentimg.replace(" ", "%20")
        dl_msg += f"{count}. {currentimg}\n"
        count += 1
    currentpage += 1
    fld_msg = f"Your provided Pixl.is link is of Folder and I've Found {count - 1} files in the folder.\n"
    fld_link = f"\nFolder Link: {url}\n"
    final_msg = fld_link + "\n" + fld_msg + "\n" + dl_msg
    return final_msg


############################################################
# sirigan  ( unused )

def siriganbypass(url):
    client = requests.Session()
    res = client.get(url)
    url = res.url.split('=', maxsplit=1)[-1]

    while True:
        try: url = base64.b64decode(url).decode('utf-8')
        except: break

    return url.split('url=')[-1]


############################################################
# shorte

def sh_st_bypass(url):    
    client = requests.Session()
    client.headers.update({'referer': url})
    p = urlparse(url)
    
    res = client.get(url)

    sess_id = re.findall('''sessionId(?:\s+)?:(?:\s+)?['|"](.*?)['|"]''', res.text)[0]
    
    final_url = f"{p.scheme}://{p.netloc}/shortest-url/end-adsession"
    params = {
        'adSessionId': sess_id,
        'callback': '_'
    }
    time.sleep(5) # !important
    
    res = client.get(final_url, params=params)
    dest_url = re.findall('"(.*?)"', res.text)[1].replace('\/','/')
    
    return {
        'src': url,
        'dst': dest_url
    }['dst']


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
# sharer pw

def parse_info_sharer(res):
    f = re.findall(">(.*?)<\/td>", res.text)
    info_parsed = {}
    for i in range(0, len(f), 3):
        info_parsed[f[i].lower().replace(' ', '_')] = f[i+2]
    return info_parsed

def sharer_pw(url,Laravel_Session, XSRF_TOKEN, forced_login=False):
    client = cloudscraper.create_scraper(allow_brotli=False)
    client.cookies.update({
        "XSRF-TOKEN": XSRF_TOKEN,
        "laravel_session": Laravel_Session
    })
    res = client.get(url)
    token = re.findall("_token\s=\s'(.*?)'", res.text, re.DOTALL)[0]
    ddl_btn = etree.HTML(res.content).xpath("//button[@id='btndirect']")
    info_parsed = parse_info_sharer(res)
    info_parsed['error'] = True
    info_parsed['src_url'] = url
    info_parsed['link_type'] = 'login'
    info_parsed['forced_login'] = forced_login
    headers = {
        'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'x-requested-with': 'XMLHttpRequest'
    }
    data = {
        '_token': token
    }
    if len(ddl_btn):
        info_parsed['link_type'] = 'direct'
    if not forced_login:
        data['nl'] = 1
    try: 
        res = client.post(url+'/dl', headers=headers, data=data).json()
    except:
        return info_parsed
    if 'url' in res and res['url']:
        info_parsed['error'] = False
        info_parsed['gdrive_link'] = res['url']
    if len(ddl_btn) and not forced_login and not 'url' in info_parsed:
        # retry download via login
        return sharer_pw(url,Laravel_Session, XSRF_TOKEN, forced_login=True)
    return info_parsed["gdrive_link"]


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
# adfly

def decrypt_url(code):
    a, b = '', ''
    for i in range(0, len(code)):
        if i % 2 == 0: a += code[i]
        else: b = code[i] + b
    key = list(a + b)
    i = 0
    while i < len(key):
        if key[i].isdigit():
            for j in range(i+1,len(key)):
                if key[j].isdigit():
                    u = int(key[i]) ^ int(key[j])
                    if u < 10: key[i] = str(u)
                    i = j					
                    break
        i+=1
    key = ''.join(key)
    decrypted = base64.b64decode(key)[16:-16]
    return decrypted.decode('utf-8')


def adfly(url):
    client = cloudscraper.create_scraper(allow_brotli=False)
    res = client.get(url).text
    out = {'error': False, 'src_url': url}
    try:
        ysmm = re.findall("ysmm\s+=\s+['|\"](.*?)['|\"]", res)[0]
    except:
        out['error'] = True
        return out
    url = decrypt_url(ysmm)
    if re.search(r'go\.php\?u\=', url):
        url = base64.b64decode(re.sub(r'(.*?)u=', '', url)).decode()
    elif '&dest=' in url:
        url = unquote(re.sub(r'(.*?)dest=', '', url))
    out['bypassed_url'] = url
    return out


##############################################################################################        
# gplinks

def gplinks(url: str):
    client = cloudscraper.create_scraper(allow_brotli=False)
    token = url.split("/")[-1]
    domain ="https://gplinks.co/"
    referer = "https://mynewsmedia.co/"
    vid = client.get(url, allow_redirects= False).headers["Location"].split("=")[-1]
    url = f"{url}/?{vid}"
    response = client.get(url, allow_redirects=False)
    soup = BeautifulSoup(response.content, "html.parser")
    inputs = soup.find(id="go-link").find_all(name="input")
    data = { input.get('name'): input.get('value') for input in inputs }
    time.sleep(10)
    headers={"x-requested-with": "XMLHttpRequest"}
    bypassed_url = client.post(domain+"links/go", data=data, headers=headers).json()["url"]
    try: return bypassed_url
    except: return 'Something went wrong :('


######################################################################################################
# droplink

def droplink(url):
    client = cloudscraper.create_scraper(allow_brotli=False)
    res = client.get(url, timeout=5)
    
    ref = re.findall("action[ ]{0,}=[ ]{0,}['|\"](.*?)['|\"]", res.text)[0]
    h = {"referer": ref}
    res = client.get(url, headers=h)

    bs4 = BeautifulSoup(res.content, "html.parser")
    inputs = bs4.find_all("input")
    data = {input.get("name"): input.get("value") for input in inputs}
    h = {
            "content-type": "application/x-www-form-urlencoded",
            "x-requested-with": "XMLHttpRequest",
        }
    
    p = urlparse(url)
    final_url = f"{p.scheme}://{p.netloc}/links/go"
    time.sleep(3.1)
    res = client.post(final_url, data=data, headers=h).json()

    if res["status"] == "success": return res["url"]
    return 'Something went wrong :('


#####################################################################################################################
# link vertise

def linkvertise(url):
    params = {'url': url,}
    response = requests.get('https://bypass.pm/bypass2', params=params).json()
    if response["success"]: return response["destination"]
    else: return response["msg"]


###################################################################################################################
# others

def others(url):
    return "API Currently not Available"


#################################################################################################################
# ouo

# RECAPTCHA v3 BYPASS
# code from https://github.com/xcscxr/Recaptcha-v3-bypass
def RecaptchaV3(ANCHOR_URL="https://www.google.com/recaptcha/api2/anchor?ar=1&k=6Lcr1ncUAAAAAH3cghg6cOTPGARa8adOf-y9zv2x&co=aHR0cHM6Ly9vdW8uaW86NDQz&hl=en&v=1B_yv3CBEV10KtI2HJ6eEXhJ&size=invisible&cb=4xnsug1vufyr"):
    url_base = 'https://www.google.com/recaptcha/'
    post_data = "v={}&reason=q&c={}&k={}&co={}"
    client = requests.Session()
    client.headers.update({
        'content-type': 'application/x-www-form-urlencoded'
    })
    matches = re.findall('([api2|enterprise]+)\/anchor\?(.*)', ANCHOR_URL)[0]
    url_base += matches[0]+'/'
    params = matches[1]
    res = client.get(url_base+'anchor', params=params)
    token = re.findall(r'"recaptcha-token" value="(.*?)"', res.text)[0]
    params = dict(pair.split('=') for pair in params.split('&'))
    post_data = post_data.format(params["v"], token, params["k"], params["co"])
    res = client.post(url_base+'reload', params=f'k={params["k"]}', data=post_data)
    answer = re.findall(r'"rresp","(.*?)"', res.text)[0]    
    return answer


# code from https://github.com/xcscxr/ouo-bypass/
def ouo(url):
    client = requests.Session()
    tempurl = url.replace("ouo.press", "ouo.io")
    p = urlparse(tempurl)
    id = tempurl.split('/')[-1]
    
    res = client.get(tempurl)
    next_url = f"{p.scheme}://{p.hostname}/go/{id}"

    for _ in range(2):
        if res.headers.get('Location'):
            break
        bs4 = BeautifulSoup(res.content, 'lxml')
        inputs = bs4.form.findAll("input", {"name": re.compile(r"token$")})
        data = { input.get('name'): input.get('value') for input in inputs }
        
        ans = RecaptchaV3()
        data['x-token'] = ans
        h = {
            'content-type': 'application/x-www-form-urlencoded'
        }
        res = client.post(next_url, data=data, headers=h, allow_redirects=False)
        next_url = f"{p.scheme}://{p.hostname}/xreallcygo/{id}"

    return res.headers.get('Location')


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
# urls open

def urlsopen(url):
    client = cloudscraper.create_scraper(allow_brotli=False)
    DOMAIN = "https://blogpost.viewboonposts.com/ssssssagasdgeardggaegaqe"
    url = url[:-1] if url[-1] == '/' else url
    code = url.split("/")[-1]
    final_url = f"{DOMAIN}/{code}"
    ref = "https://blog.textpage.xyz/"
    h = {"referer": ref}
    resp = client.get(final_url,headers=h)
    soup = BeautifulSoup(resp.content, "html.parser")
    inputs = soup.find_all("input")
    data = { input.get('name'): input.get('value') for input in inputs }
    h = { "x-requested-with": "XMLHttpRequest" }
    time.sleep(2)
    r = client.post(f"{DOMAIN}/links/go", data=data, headers=h)
    try: return r.json()['url']
    except: return "Something went wrong :("
    

####################################################################################################
# URLShortX - xpshort

def xpshort(url):
    client = cloudscraper.create_scraper(allow_brotli=False)
    DOMAIN = "https://xpshort.com"
    url = url[:-1] if url[-1] == '/' else url
    code = url.split("/")[-1]
    final_url = f"{DOMAIN}/{code}"
    ref = "https://www.jankarihoga.com/"
    h = {"referer": ref}
    resp = client.get(final_url,headers=h)
    soup = BeautifulSoup(resp.content, "html.parser")
    inputs = soup.find_all("input")
    data = { input.get('name'): input.get('value') for input in inputs }
    h = { "x-requested-with": "XMLHttpRequest" }
    time.sleep(8)
    r = client.post(f"{DOMAIN}/links/go", data=data, headers=h)
    try: return r.json()['url']
    except: return "Something went wrong :("


#####################################################################################################
# dulink

def dulink(url):
    client = cloudscraper.create_scraper(allow_brotli=False)
    DOMAIN = "https://du-link.in"
    url = url[:-1] if url[-1] == '/' else url
    ref = "https://profitshort.com/"
    h = {"referer": ref}
    resp = client.get(url, headers=h)
    soup = BeautifulSoup(resp.content, "html.parser")
    inputs = soup.find_all("input")
    data = { input.get('name'): input.get('value') for input in inputs }
    h = { "x-requested-with": "XMLHttpRequest" }
    r = client.post(f"{DOMAIN}/links/go", data=data, headers=h)
    try: return r.json()['url']
    except: return "Something went wrong :("

#####################################################################################################
# krownlinks

def krownlinks(url):
    client = requests.session()
    DOMAIN = "https://tech.bloggertheme.xyz"
    url = url[:-1] if url[-1] == '/' else url
    code = url.split("/")[-1]
    final_url = f"{DOMAIN}/{code}"
    resp = client.get(final_url)
    soup = BeautifulSoup(resp.content, "html.parser")
    try: inputs = soup.find(id="go-link").find_all(name="input")
    except: return "Incorrect Link"
    data = { input.get('name'): input.get('value') for input in inputs }
    h = { "x-requested-with": "XMLHttpRequest" }
    time.sleep(10)
    r = client.post(f"{DOMAIN}/links/go", data=data, headers=h)
    try: return r.json()['url']
    except: return "Something went wrong :("


####################################################################################################
# adrinolink

def adrinolink (url):
    if "https://adrinolinks.in/" not in url: url = "https://adrinolinks.in/" + url.split("/")[-1]
    client = cloudscraper.create_scraper(allow_brotli=False)
    DOMAIN = "https://adrinolinks.in"
    ref = "https://amritadrino.com/"
    h = {"referer": ref}
    resp = client.get(url,headers=h)
    soup = BeautifulSoup(resp.content, "html.parser")
    inputs = soup.find_all("input")
    data = { input.get('name'): input.get('value') for input in inputs }
    h = { "x-requested-with": "XMLHttpRequest" }
    time.sleep(8)
    r = client.post(f"{DOMAIN}/links/go", data=data, headers=h)
    try: return r.json()['url']
    except: return "Something went wrong :("


#####################################################################################################
# mdiskshortners

def mdiskshortners(url):
    client = cloudscraper.create_scraper(allow_brotli=False)
    DOMAIN = "https://mdiskshortners.in/"
    url = url[:-1] if url[-1] == '/' else url
    code = url.split("/")[-1]
    final_url = f"{DOMAIN}/{code}"
    ref = "https://www.adzz.in/"
    h = {"referer": ref}
    resp = client.get(final_url,headers=h)
    soup = BeautifulSoup(resp.content, "html.parser")
    inputs = soup.find_all("input")
    data = { input.get('name'): input.get('value') for input in inputs }
    h = { "x-requested-with": "XMLHttpRequest" }
    time.sleep(2)
    r = client.post(f"{DOMAIN}/links/go", data=data, headers=h)
    try: return r.json()['url']
    except: return "Something went wrong :("


##################################################################################################### 
# tinyfy

def tiny(url):
    client = requests.session()
    DOMAIN = "https://tinyfy.in"
    url = url[:-1] if url[-1] == '/' else url
    code = url.split("/")[-1]
    final_url = f"{DOMAIN}/{code}"
    ref = "https://www.yotrickslog.tech/"
    h = {"referer": ref}
    resp = client.get(final_url,headers=h)
    soup = BeautifulSoup(resp.content, "html.parser")
    inputs = soup.find_all("input")
    data = { input.get('name'): input.get('value') for input in inputs }
    h = { "x-requested-with": "XMLHttpRequest" }
    r = client.post(f"{DOMAIN}/links/go", data=data, headers=h)
    try: return r.json()['url']
    except: return "Something went wrong :("


##################################################################################################### 
# earnl

def earnl(url):
    client = requests.session()
    DOMAIN = "https://v.earnl.xyz"
    url = url[:-1] if url[-1] == '/' else url
    code = url.split("/")[-1]
    final_url = f"{DOMAIN}/{code}"
    ref = "https://link.modmakers.xyz/"
    h = {"referer": ref}
    resp = client.get(final_url,headers=h)
    soup = BeautifulSoup(resp.content, "html.parser")
    inputs = soup.find_all("input")
    data = { input.get('name'): input.get('value') for input in inputs }
    h = { "x-requested-with": "XMLHttpRequest" }
    time.sleep(5)
    r = client.post(f"{DOMAIN}/links/go", data=data, headers=h)
    try:
        return r.json()['url']
    except: return "Something went wrong :("


##################################################################################################### 
# moneykamalo

def moneykamalo(url):
    client = requests.session()
    DOMAIN = "https://go.moneykamalo.com"
    url = url[:-1] if url[-1] == '/' else url
    code = url.split("/")[-1]
    final_url = f"{DOMAIN}/{code}"
    ref = "https://techkeshri.com/"
    h = {"referer": ref}
    resp = client.get(final_url,headers=h)
    soup = BeautifulSoup(resp.content, "html.parser")
    inputs = soup.find_all("input")
    data = { input.get('name'): input.get('value') for input in inputs }
    h = { "x-requested-with": "XMLHttpRequest" }
    time.sleep(5)
    r = client.post(f"{DOMAIN}/links/go", data=data, headers=h)
    try:
        return r.json()['url']
    except: return "Something went wrong :("


##################################################################################################### 
# easysky

def easysky(url):
    client = cloudscraper.create_scraper(allow_brotli=False)
    DOMAIN = "https://techy.veganab.co/"
    url = url[:-1] if url[-1] == '/' else url
    code = url.split("/")[-1]
    final_url = f"{DOMAIN}/{code}"
    ref = "https://veganab.co/"
    h = {"referer": ref}
    resp = client.get(final_url,headers=h)
    soup = BeautifulSoup(resp.content, "html.parser")
    inputs = soup.find_all("input")
    data = { input.get('name'): input.get('value') for input in inputs }
    h = { "x-requested-with": "XMLHttpRequest" }
    time.sleep(8)
    r = client.post(f"{DOMAIN}/links/go", data=data, headers=h)
    try: return r.json()['url']
    except: return "Something went wrong :("


##################################################################################################### 
# indiurl

def indi(url):
    client = requests.session()
    DOMAIN = "https://file.earnash.com/"
    url = url[:-1] if url[-1] == '/' else url
    code = url.split("/")[-1]
    final_url = f"{DOMAIN}/{code}"
    ref = "https://indiurl.cordtpoint.co.in/"
    h = {"referer": ref}
    resp = client.get(final_url,headers=h)
    soup = BeautifulSoup(resp.content, "html.parser")
    inputs = soup.find_all("input")
    data = { input.get('name'): input.get('value') for input in inputs }
    h = { "x-requested-with": "XMLHttpRequest" }
    time.sleep(10)
    r = client.post(f"{DOMAIN}/links/go", data=data, headers=h)
    try:
        return r.json()['url']
    except: return "Something went wrong :("


##################################################################################################### 
# linkbnao

def linkbnao(url):
    client = cloudscraper.create_scraper(allow_brotli=False)
    DOMAIN = "https://vip.linkbnao.com"
    url = url[:-1] if url[-1] == '/' else url
    code = url.split("/")[-1]
    final_url = f"{DOMAIN}/{code}"
    ref = "https://ffworld.xyz/"
    h = {"referer": ref}
    resp = client.get(final_url,headers=h)
    soup = BeautifulSoup(resp.content, "html.parser")
    inputs = soup.find_all("input")
    data = { input.get('name'): input.get('value') for input in inputs }
    h = { "x-requested-with": "XMLHttpRequest" }
    time.sleep(2)
    r = client.post(f"{DOMAIN}/links/go", data=data, headers=h)
    try:
        return r.json()['url']
    except: return "Something went wrong :("


##################################################################################################### 
# omegalinks

def mdiskpro(url):
    client = cloudscraper.create_scraper(allow_brotli=False)
    DOMAIN = "https://mdisk.pro"
    ref = "https://m.meclipstudy.in/"
    h = {"referer": ref}
    resp = client.get(url,headers=h)
    soup = BeautifulSoup(resp.content, "html.parser")
    inputs = soup.find_all("input")
    data = { input.get('name'): input.get('value') for input in inputs }
    h = { "x-requested-with": "XMLHttpRequest" }
    time.sleep(8)
    r = client.post(f"{DOMAIN}/links/go", data=data, headers=h)
    try:
        return r.json()['url']
    except: return "Something went wrong :("


##################################################################################################### 
# rslinks

def rslinks(url):
      client = requests.session()
      download = get(url, stream=True, allow_redirects=False)
      v = download.headers["location"]
      code = v.split('ms9')[-1]
      final = f"http://techyproio.blogspot.com/p/short.html?{code}=="
      try: return final
      except: return "Something went wrong :("


##################################################################################################### 
# bitly + tinyurl

def bitly_tinyurl(url: str) -> str:
	response = requests.get(url).url
	try: return response
	except: return "Something went wrong :("

##################################################################################################### 
# thinfi

def thinfi(url: str) -> str :
	response = requests.get(url)
	soup = BeautifulSoup(response.content,  "html.parser").p.a.get("href")
	try: return soup
	except: return "Something went wrong :("

##################################################################################################### 
# helpers

# check if present in list
def ispresent(inlist,url):
    for ele in inlist:
        if ele in url:
            return True
    return False


# shortners
def shortners(url):
   
        
    

    # kolop
    elif "https://kolop." in url:
        if KCRYPT  == "":
            return "🚫 __You can't use this because__ **KOLOP_CRYPT** __ENV is not set__"
        
        print("entered kolop:",url)
        return kolop_dl(url, KCRYPT)

    # hubdrive
    elif "https://hubdrive." in url:
        if HCRYPT == "":
            return "🚫 __You can't use this because__ **HUBDRIVE_CRYPT** __ENV is not set__"
 
        print("entered hubdrive:",url)
        return hubdrive_dl(url, HCRYPT)

    # drivefire
    elif "https://drivefire." in url:
        if DCRYPT == "":
            return "🚫 __You can't use this because__ **DRIVEFIRE_CRYPT** __ENV is not set__"

        print("entered drivefire:",url)
        return drivefire_dl(url, DCRYPT)
        
    # filecrypt
    elif (("https://filecrypt.co/") in url or ("https://filecrypt.cc/" in url)):
        print("entered filecrypt:",url)
        return filecrypt(url)
        
    # shareus
    elif "https://shareus.io/" in url:
        print("entered shareus:",url)
        return shareus(url)
        
    # shortingly
    elif "https://shortingly.in/" in url:
        print("entered shortingly:",url)
        return shortingly(url)

    # gyanilinks
    elif "https://gyanilinks.com/" in url or "https://gtlinks.me/" in url:
        print("entered gyanilinks:",url)
        return gyanilinks(url)

    # flashlink
    elif "https://go.flashlink.in/" in url:
        print("entered flashlink:",url)
        return flashlink(url)

    # short2url
    elif "https://short2url.in/" in url:
        print("entered short2url:",url)
        return short2url(url)
        
    # shorte
    elif "https://shorte.st/" in url:
        print("entered shorte:",url)
        return sh_st_bypass(url)
        
    # psa
    elif "https://psa.pm/" in url:
        print("entered psa:",url)
        return psa_bypasser(url)
        
    # sharer pw
    elif "https://sharer.pw/" in url:
        if XSRF_TOKEN == "" or Laravel_Session == "":
            return "🚫 __You can't use this because__ **XSRF_TOKEN** __and__ **Laravel_Session** __ENV is not set__"
       
        print("entered sharer:",url)
        return sharer_pw(url, Laravel_Session, XSRF_TOKEN)

    # gdtot url
    elif "gdtot.cfd/" in url:
        print("entered gdtot:",url)
        return gdtot(url,GDTot_Crypt)
        
    # adfly
    elif "https://adf.ly/" in url:
        print("entered adfly:",url)
        out = adfly(url)
        return out['bypassed_url']
 
    # gplinks
    elif "https://gplinks.co/" in url:
        print("entered gplink:",url)
        return gplinks(url)
        
    # droplink
    elif "https://droplink.co/" in url:
        print("entered droplink:",url)
        return droplink(url)
        
    # linkvertise
    elif "https://linkvertise.com/" in url:
        print("entered linkvertise:",url)
        return linkvertise(url)
        
    # rocklinks
    elif "https://rocklinks.net/" in url:
        print("entered rocklinks:",url)
        return rocklinks(url)
        
    # ouo
    elif "https://ouo.press/" in url:
        print("entered ouo:",url)
        return ouo(url)

    # try2link
    elif "https://try2link.com/" in url:
        print("entered try2links:",url)
        return try2link_bypass(url)

    # urlsopen
    elif "https://urlsopen." in url:
        print("entered urlsopen:",url)
        return urlsopen(url)

    # xpshort
    elif "https://xpshort.com/" in url or "https://push.bdnewsx.com/" in url or "https://techymozo.com/" in url:
        print("entered xpshort:",url)
        return xpshort(url)

    # dulink
    elif "https://du-link.in/" in url:
        print("entered dulink:",url)
        return dulink(url)

    # ez4short
    elif "https://ez4short.com/" in url:
        print("entered ez4short:",url)
        return ez4(url)
    
    # krownlinks
    elif "https://krownlinks.me/" in url:
        print("entered krownlinks:",url)
        return krownlinks(url)
    
    # adrinolink
    elif "https://adrinolinks." in url:
        print("entered adrinolink:",url)
        return adrinolink(url)
    
    # tnlink
    elif "https://link.tnlink.in/" in url:
        print("entered tnlink:",url)
        return tnlink(url)

    # mdiskshortners
    elif "https://mdiskshortners.in/" in url:
        print("entered mdiskshortners:",url)
        return mdiskshortners(url)

    # tinyfy
    elif "tinyfy.in" in url:
        print("entered tinyfy:",url)
        return tiny(url)

    # earnl
    elif "go.earnl.xyz" in url:
        print("entered earnl:",url)
        return earnl(url)

    # moneykamalo
    elif "earn.moneykamalo.com" in url:
        print("entered moneykamalo:",url)
        return moneykamalo(url)

    # easysky
    elif "m.easysky.in" in url:
        print("entered easysky:",url)
        return easysky(url)

    # indiurl
    elif "go.indiurl.in.net" in url:
        print("entered indiurl:",url)
        return indi(url)

    # linkbnao
    elif "linkbnao.com" in url:
        print("entered linkbnao:",url)
        return linkbnao(url)

    # omegalinks
    elif "mdisk.pro" in url:
        print("entered mdiskpro:",url)
        return mdiskpro(url)

    # rslinks
    elif "rslinks.net" in url:
        print("entered rslinks:",url)
        return rslinks(url)

    # bitly + tinyurl
    elif "bit.ly" in url or "tinyurl.com" in url:
        print("entered bitly_tinyurl:",url)
        return bitly_tinyurl(url)

    # thinfi
    elif "thinfi.com" in url:
        print("entered thinfi:",url)
        return thinfi(url)
        
    # htpmovies sharespark cinevood
    elif "https://htpmovies." in url or 'https://sharespark.me/' in url or "https://cinevood." in url or "https://atishmkv." in url \
        or "https://teluguflix" in url or 'https://taemovies' in url or "https://toonworld4all" in url or "https://animeremux" in url:
        print("entered htpmovies sharespark cinevood atishmkv:",url)
        return scrappers(url)

    # gdrive look alike
    elif ispresent(gdlist,url):
        print("entered gdrive look alike:",url)
        return unified(url)

    # others
    elif ispresent(otherslist,url):
        print("entered others:",url)
        return others(url)

    # else
    else: return "Not in Supported Sites"
    

################################################################################################################################
