
import sys
version = (3, 0)
cur_version = sys.version_info
if cur_version >= version:  
    import urllib.request
    from urllib.request import Request, urlopen
    from urllib.request import URLError, HTTPError
    from urllib.parse import quote
    import http.client
    from http.client import IncompleteRead, BadStatusLine
    http.client._MAXHEADERS = 1000
else:  
    import urllib2
    from urllib2 import Request, urlopen
    from urllib2 import URLError, HTTPError
    from urllib import quote
    import httplib
    from httplib import IncompleteRead, BadStatusLine
    httplib._MAXHEADERS = 1000
import time 
import os
import argparse
import ssl
import datetime
import json
import re
import codecs
import socket

args_list = ["keyword", "keyword_from_file", "proxy", "similar_images", "prefix_keyword", "suffix_keyword",
             "limit", "format", "color", "color_type", "usage_rights", "size",
              "time_range", "delay", "url", "single_image","exact_size", "no_directory", "specific_site", 
              "aspect_ratio", "type", "time",
             "output_directory", "image_directory",
             "print_urls", "print_size", "print_paths", "metadata", "extract_metadata", "socket_timeout",
             "thumbnail", "save_source","silent_mode", "thumbnail_only", "language", "safe_search", "no_numbering","prefix", "chromedriver", "related_images", 
             "offset", "no_download","ignore_urls"]


def input_from_user():
    config = argparse.Argumentimage_search()
    config.add_argument('-cf', '--config_file', help='config file name', default='', type=str, required=False)
    config_file_check = config.parse_known_args()
    object_check = vars(config_file_check[0])

    if object_check['config_file'] != '':
        records = []
   json_file = json.load(open(config_file_check[0].config_file))
        for record in range(0,len(json_file['Records'])):
            args = {}
            for i in args_list:
                args[i] = None
            for key, value in json_file['Records'][record].items():
                args[key] = value
            records.append(args)
        records_count = len(records)
    
        args = image_search.parse_args()
        args = vars(args)
        records = []
        records.append(args)
    return records


class googleimagesdownload:
    def __init__(self):
        pass


    def download_page(self,url):
        version = (3, 0)
        cur_version = sys.version_info
        if cur_version >= version:  
            try:
                search_headers = {}
                search_headers['User-Agent'] = "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36"
                image_search = urllib.request.Request(url, headers=search_headers)
                resp = urllib.request.urlopen(image_search)
                respData = str(resp.read())
                return respData
            except Exception as e:
                print("The URL could not be openned \n"
                      "Ensure that your proxy setings are upto date")
                sys.exit()
        else:  
            try:
                search_headers = {}
                search_headers['User-Agent'] = "Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.27 Safari/537.17"
                request = urllib2.Request(url, headers=search_headers)
                try:
                    res = urllib2.urlopen(request)
                except URLError:  
                    context = ssl._create_unverified_context()
                    res = urlopen(request, context=context)
                pages = res.read()
                return pages
            except:
                print(" PAge not Found\n"
                      "Error ")
                sys.exit()
                return "Page Not found"


    def download_extended_page(self,url,chromedriver):
        from selenium import webdriver
        from selenium.webdriver.common.keys import Keys
        if sys.version_info[0] < 3:
            reload(sys)
            sys.setdefaultencoding('utf8')
        options1 = webdriver.ChromeOptions()
        options1.add_argument('--no-sandbox')
        options1.add_argument("--headless")

        try:
            browser1 = webdriver.Chrome(chromedriver, chrome_options=options)
        except Exception as e:
            print("Error (exception: %s)" % e)
            sys.exit()
        browser1.set_window_size(1024, 768)

    
        browser1.get(url)
        time.sleep(1)
        print("the program is downloading your images...")

        element = browser1.find_element_by_tag_name("body")

        for i in range(30):
            element.send_keys(Keys.PAGE_DOWN)
            time.sleep(0.3)

        try:
            browser1.find_element_by_id("smb").click()
            for i in range(50):
                element.send_keys(Keys.PAGE_DOWN)
                time.sleep(0.3)  
        except:
            for i in range(10):
                element.send_keys(Keys.PAGE_DOWN)
                time.sleep(0.3)  
        print("Reached end of Page.")
        time.sleep(0.5)

        source = browser1.page_source
     
        browser1.close()

        return source


    def replace_with_byte(self,match):
        return chr(int(match.group(0)[1:], 8))

    def repair(self,brokenjson):
        invalid_escape = re.compile(r'\\[0-7]{1,3}') 
        return invalid_escape.sub(self.replace_with_byte, brokenjson)

    def get_next_tab(self,s):
        line1 = s.find('class="dtviD"')
        if line1 == -1: 
            end_quote = 0
            link = "no_tabs"
            return link,'',end_quote
        else:
            line1 = s.find('class="dtviD"')
            start_content = s.find('href="', line1 + 1)
            end_content = s.find('">', start_content + 1)
            url_item = "https://www.google.com" + str(s[start_content + 6:end_content])
            url_item = url_item.replace('&amp;', '&')

            line1_2 = s.find('class="dtviD"')
            s = s.replace('&amp;', '&')
            start_content_2 = s.find(':', line1_2 + 1)
            end_content_2 = s.find('&usg=', start_content_2 + 1)
            items_names = str(s[start_content_2 + 1:end_content_2])

            chars = items_names.find(',g_1:')
            chars_end = items_names.find(":", chars + 6)
            if chars_end == -1:
                updated_item_name = (items_names[chars + 5:]).replace("+", " ")
            else:
                updated_item_name = (items_names[chars+5:chars_end]).replace("+", " ")

            return url_item, updated_item_name, end_content


 
    def get_all_tabs(self,page):
        tabs = {}
        while True:
            item,item_name,end_content = self.get_next_tab(page)
            if item == "no_tabs":
                break
            else:
                if len(item_name) > 100 or item_name == "background-color":
                    break
                else:
                    tabs[item_name] = item  
                    time.sleep(0.1)  
                    page = page[end_content:]
        return tabs



    def object_format(self,object):
       form_o = {}
       form_o['image_formats'] = object['ity']
       form_o['image_height'] = object['oh']
       form_o['image_width'] = object['ow']
       form_o['image_link'] = object['ou']
       form_o['image_description'] = object['pt']
       form_o['image_host'] = object['rh']
       form_o['image_source'] = object['ru']
       form_o['image_thumbnail_url'] = object['tu']
        return form_o

    def single_image(self,img_urls):
        directory_1 = "downloads"
        extensions = (".jpg", ".gif", ".png", ".bmp", ".svg", ".webp", ".ico")
        url = img_urls
        try:
            os.makedirs(directory_1)
        except OSError as e:
            if e.errno != 17:
                raise
            pass
        req = Request(url, headers={
            "User-Agent": "Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.27 Safari/537.17"})

        res = urlopen(req, None, 10)
        data = res.read()
        res.close()

       i_names = str(url[(url.rfind('/')) + 1:])
        if '?' ini_names:
           i_names =i_names[:image_name.find('?')]
       
        if any(map(lambda extension: extension ini_names, extensions)):
            file_name = directory_1 + "/" +i_names
        else:
            file_name = directory_1 + "/" +i_names + ".jpg"
           i_names =i_names + ".jpg"

        try:
            output_file = open(file_name, 'wb')
            output_file.write(data)
            output_file.close()
        except IOError as e:
            raise e
        except OSError as e:
            raise e
        print("completed ====> " +i_names.encode('raw_unicode_escape').decode('utf-8'))
        return

    def similar_images(self,similar_images):
        version = (3, 0)
        cur_version = sys.version_info
        if cur_version >= version:  
            try:
                searchUrl = 'https://www.google.com/searchbyimage?site=search&sa=X&img_urls=' + similar_images
                search_headers = {}
                search_headers['User-Agent'] = "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36"

                req1 = urllib.request.Request(searchUrl, headers=search_headers)
                resp1 = urllib.request.urlopen(req1)
                content = str(resp1.read())
                l1 = content.find('AMhZZ')
                l2 = content.find('&', l1)
                urll = content[l1:l2]

                newurl = "https://www.google.com/search?tbs=sbi:" + urll + "&site=search&sa=X"
                req2 = urllib.request.Request(newurl, headers=search_headers)
                resp2 = urllib.request.urlopen(req2)
                l3 = content.find('/search?sa=X&amp;q=')
                l4 = content.find(';', l3 + 19)
                urll2 = content[l3 + 19:l4]
                return urll2
            except:
                return "Error in the applications"
        else:  
            try:
                searchUrl = 'https://www.google.com/searchbyimage?site=search&sa=X&img_urls=' + similar_images
                search_headers = {}
                search_headers['User-Agent'] = "Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.27 Safari/537.17"

                req1 = urllib2.Request(searchUrl, headers=search_headers)
                resp1 = urllib2.urlopen(req1)
                content = str(resp1.read())
                l1 = content.find('AMhZZ')
                l2 = content.find('&', l1)
                urll = content[l1:l2]

                newurl = "https://www.google.com/search?tbs=sbi:" + urll + "&site=search&sa=X"
                req2 = urllib2.Request(newurl, headers=search_headers)
                resp2 = urllib2.urlopen(req2)
                l3 = content.find('/search?sa=X&amp;q=')
                l4 = content.find(';', l3 + 19)
                urll2 = content[l3 + 19:l4]
                return(urll2)
            except:
                return "Could not connect to cloud"


    def build_url_parameters(self,args):
        if args['language']:
            lang = "&lr="
            l_params = {"Arabic":"lang_ar","Chinese (Simplified)":"lang_zh-CN","Chinese (Traditional)":"lang_zh-TW","Czech":"lang_cs","Danish":"lang_da","Dutch":"lang_nl","English":"lang_en","Estonian":"lang_et","Finnish":"lang_fi","French":"lang_fr","German":"lang_de","Greek":"lang_el","Hebrew":"lang_iw ","Hungarian":"lang_hu","Icelandic":"lang_is","Italian":"lang_it","Japanese":"lang_ja","Korean":"lang_ko","Latvian":"lang_lv","Lithuanian":"lang_lt","Norwegian":"lang_no","Portuguese":"lang_pt","Polish":"lang_pl","Romanian":"lang_ro","Russian":"lang_ru","Spanish":"lang_es","Swedish":"lang_sv","Turkish":"lang_tr"}
            lang_url = lang+l_params[args['language']]
        else:
            lang_url = ''

        if args['time_range']:
            json_acceptable_string = args['time_range'].replace("'", "\"")
            d = json.loads(json_acceptable_string)
            time_range = ',cdr:1,cd_min:' + d['time_min'] + ',cd_max:' + d['time_max']
        else:
            time_range = ''

        if args['exact_size']:
            size_array = [x.strip() for x in args['exact_size'].split(',')]
            exact_size = ",isz:ex,iszw:" + str(size_array[0]) + ",iszh:" + str(size_array[1])
        else:
            exact_size = ''

        built_url = "&tbs="
        counter = 0
        params = {'color':[args['color'],{'yellow':'ic:specific,isc:yellow', 'orange':'ic:specific,isc:orange','green':'ic:specific,isc:green', 'teal':'ic:specific,isc:teel', 'blue':'ic:specific,isc:blue', 'purple':'ic:specific,isc:purple', 'pink':'ic:specific,isc:pink', 'white':'ic:specific,isc:white', 'gray':'ic:specific,isc:gray', 'black':'ic:specific,isc:black', 'brown':'ic:specific,isc:brown'}],
                  'color_type':[args['color_type'],{'black-and-white':'ic:gray','full-color':'ic:color', 'transparent':'ic:trans'}],
                  'usage_rights':[args['usage_rights'],{'labeled-for-reuse-with-modifications':'sur:fmc','labeled-for-reuse':'sur:fc','labeled-for-noncommercial-reuse-with-modification':'sur:fm','labeled-for-nocommercial-reuse':'sur:f'}],
                  'size':[args['size'],{'large':'isz:l','medium':'isz:m','icon':'isz:i','>400*300':'isz:lt,islt:qsvga','>640*480':'isz:lt,islt:vga','>800*600':'isz:lt,islt:svga','>1024*768':'visz:lt,islt:xga','>2MP':'isz:lt,islt:2mp','>4MP':'isz:lt,islt:4mp','>6MP':'isz:lt,islt:6mp','>8MP':'isz:lt,islt:8mp','>10MP':'isz:lt,islt:10mp','>12MP':'isz:lt,islt:12mp','>15MP':'isz:lt,islt:15mp','>20MP':'isz:lt,islt:20mp','>40MP':'isz:lt,islt:40mp','>70MP':'isz:lt,islt:70mp'}],
                  'type':[args['type'],{'face':'itp:face','photo':'itp:photo','clipart':'itp:clipart','line-drawing':'itp:lineart','animated':'itp:animated'}],
                  'time':[args['time'],{'past-24-hours':'qdr:d','past-7-days':'qdr:w','past-month':'qdr:m','past-year':'qdr:y'}],
                  'aspect_ratio':[args['aspect_ratio'],{'tall':'iar:t','square':'iar:s','wide':'iar:w','panoramic':'iar:xw'}],
                  'format':[args['format'],{'jpg':'ift:jpg','gif':'ift:gif','png':'ift:png','bmp':'ift:bmp','svg':'ift:svg','webp':'webp','ico':'ift:ico','raw':'ift:craw'}]}
        for key, value in params.items():
            if value[0] is not None:
                ext_param = value[1][value[0]]
                
                if counter == 0:
              
                    built_url = built_url + ext_param
                    counter += 1
                else:
                    built_url = built_url + ',' + ext_param
                    counter += 1
        built_url = lang_url+built_url+exact_size+time_range
        return built_url

    def build_search_url(self,search_term,params,url,similar_images,specific_site,safe_search):
       
        safe_search_string = "&safe=active"
    
        if url:
            url = url
        elif similar_images:
            print(similar_images)
            keywordem = self.similar_images(similar_images)
            url = 'https://www.google.com/search?q=' + keywordem + '&espv=2&biw=1366&bih=667&site=webhp&source=lnms&tbm=isch&sa=X&ei=XosDVaCXD8TasATItgE&ved=0CAcQ_AUoAg'
        elif specific_site:
            url = 'https://www.google.com/search?q=' + quote(
                search_term.encode('utf-8')) + '&as_sitesearch=' + specific_site + '&espv=2&biw=1366&bih=667&site=webhp&source=lnms&tbm=isch' + params + '&sa=X&ei=XosDVaCXD8TasATItgE&ved=0CAcQ_AUoAg'
        else:
            url = 'https://www.google.com/search?q=' + quote(
                search_term.encode('utf-8')) + '&espv=2&biw=1366&bih=667&site=webhp&source=lnms&tbm=isch' + params + '&sa=X&ei=XosDVaCXD8TasATItgE&ved=0CAcQ_AUoAg'

        if safe_search:
            url = url + safe_search_string

        return url

    def file_size(self,file_path):
        if os.path.isfile(file_path):
            file_info = os.stat(file_path)
            size = file_info.st_size
            for x in ['bytes', 'KB', 'MB', 'GB', 'TB']:
                if size < 1024.0:
                    return "%3.1f %s" % (size, x)
                size /= 1024.0
            return size

 
    def keyword_from_file(self,file_name):
        search_keyword = []
        with codecs.open(file_name, 'r', encoding='utf-8-sig') as f:
            if '.csv' in file_name:
                for line in f:
                    if line in ['\n', '\r\n']:
                        pass
                    else:
                        search_keyword.append(line.replace('\n', '').replace('\r', ''))
            elif '.txt' in file_name:
                for line in f:
                    if line in ['\n', '\r\n']:
                        pass
                    else:
                        search_keyword.append(line.replace('\n', '').replace('\r', ''))
            else:
                print("Invalid file type: Valid file types are either .txt or .csv \n"
                      "exiting...")
                sys.exit()
        return search_keyword


    def create_directories(self,directory_1, dir_name,thumbnail,thumbnail_only):
        dir_name_thumbnail = dir_name + " - thumbnail"
        
        try:
            if not os.path.exists(directory_1):
                os.makedirs(directory_1)
                time.sleep(0.2)
                path = (dir_name)
                sub_directory = os.path.join(directory_1, path)
                if not os.path.exists(sub_directory):
                    os.makedirs(sub_directory)
                if thumbnail or thumbnail_only:
                    sub_directory_thumbnail = os.path.join(directory_1, dir_name_thumbnail)
                    if not os.path.exists(sub_directory_thumbnail):
                        os.makedirs(sub_directory_thumbnail)
            else:
                path = (dir_name)
                sub_directory = os.path.join(directory_1, path)
                if not os.path.exists(sub_directory):
                    os.makedirs(sub_directory)
                if thumbnail or thumbnail_only:
                    sub_directory_thumbnail = os.path.join(directory_1, dir_name_thumbnail)
                    if not os.path.exists(sub_directory_thumbnail):
                        os.makedirs(sub_directory_thumbnail)
        except OSError as e:
            if e.errno != 17:
                raise
            pass
        return

    def download_image_thumbnail(self,img_urls,directory_1,dir_name,return_image_name,print_urls,socket_timeout,print_size,no_download,save_source,img_src,ignore_urls):
        if print_urls or no_download:
            print("Image URL: " + img_urls)
        if no_download:
            return "success","Error"
        try:
            req = Request(img_urls, headers={
                "User-Agent": "Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.27 Safari/537.17"})
            try:
              
                if socket_timeout:
                    timeout = float(socket_timeout)
                else:
                    timeout = 10

                res = urlopen(req, None, timeout)
                data = res.read()
                res.close()

                path = directory_1 + "/" + dir_name + " - thumbnail" + "/" + return_image_name

                try:
                    output_file = open(path, 'wb')
                    output_file.write(data)
                    output_file.close()
                    if save_source:
                        list_path = directory_1 + "/" + save_source + ".txt"
                        list_file = open(list_path,'a')
                        list_file.write(path + '\t' + img_src + '\n')
                        list_file.close()
                except OSError as e:
                    status = 'fail'
                    messages = "OSError on an image" + " Error: " + str(e)
                except IOError as e:
                    status = 'fail'
                    messages = "IOError" + " Error: " + str(e)

                status = 'success'
                messages = "Completed Image Thumbnail ====> " + return_image_name

                
                if print_size:
                    print("Image Size: " + str(self.file_size(path)))

            except UnicodeEncodeError as e:
                status = 'fail'
                messages = "UnicodeEncodeError" + " Error: " + str(e)

        except HTTPError as e:  
            status = 'fail'
            messages = "HTTPError" + " Error: " + str(e)

        except URLError as e:
            status = 'fail'
            messages = "URLError on an image...trying next one..." + " Error: " + str(e)

        except ssl.CertificateError as e:
            status = 'fail'
            messages = "CertificateError on an image...trying next one..." + " Error: " + str(e)

        except IOError as e: 
            status = 'fail'
            messages = "IOError on an image...trying next one..." + " Error: " + str(e)
        return status, messages


  
    def image_download(self,img_urls,image_formats,directory_1,dir_name,count,print_urls,socket_timeout,prefix,print_size,no_numbering,no_download,save_source,img_src,silent_mode,thumbnail_only,format,ignore_urls):
        if not silent_mode:
            if print_urls or no_download:
                print("Image URL: " + img_urls)
        if ignore_urls:
            if any(url in img_urls for url in ignore_urls.split(',')):
                return "fail", "Image ignored due to 'ignore url' parameter", None, img_urls
        if thumbnail_only:
            return "success", "Skipping image download...", str(img_urls[(img_urls.rfind('/')) + 1:]), img_urls
        if no_download:
            return "success","Printed url without downloading",None,img_urls
        try:
            req = Request(img_urls, headers={
                "User-Agent": "Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.27 Safari/537.17"})
            try:
                
                if socket_timeout:
                    timeout = float(socket_timeout)
                else:
                    timeout = 10

                res = urlopen(req, None, timeout)
                data = res.read()
                res.close()

                extensions = [".jpg", ".jpeg", ".gif", ".png", ".bmp", ".svg", ".webp", ".ico"]
               
               i_names = str(img_urls[(img_urls.rfind('/')) + 1:])
                if format:
                    if not image_formats or image_formats != format:
                        status = 'fail'
                        messages = "Wrong image format returned. Skipping..."
                        return_image_name = ''
                        absolute_path = ''
                        return status, messages, return_image_name, absolute_path

                if image_formats == "" or not image_formats or "." + image_formats not in extensions:
                    status = 'fail'
                    messages = "Invalid or missing image format. Skipping..."
                    return_image_name = ''
                    absolute_path = ''
                    return status, messages, return_image_name, absolute_path
                elifi_names.lower().find("." + image_formats) < 0:
                   i_names =i_names + "." + image_formats
                else:
                   i_names =i_names[:image_name.lower().find("." + image_formats) + (len(image_formats) + 1)]

         



                if prefix:
                    prefix = prefix + " "
                else:
                    prefix = ''

                if no_numbering:
                    path = directory_1 + "/" + dir_name + "/" + prefix +i_names
                else:
                    path = directory_1 + "/" + dir_name + "/" + prefix + str(count) + "." +i_names

                try:
                    output_file = open(path, 'wb')
                    output_file.write(data)
                    output_file.close()
                    if save_source:
                        list_path = directory_1 + "/" + save_source + ".txt"
                        list_file = open(list_path,'a')
                        list_file.write(path + '\t' + img_src + '\n')
                        list_file.close()
                    absolute_path = os.path.abspath(path)
                except OSError as e:
                    status = 'fail'
                    messages = "OSError on an image...trying next one..." + " Error: " + str(e)
                    return_image_name = ''
                    absolute_path = ''

           
                status = 'success'
                messages = "Completed Image ====> " + prefix + str(count) + "." +i_names
                return_image_name = prefix + str(count) + "." +i_names

                if not silent_mode:
                    if print_size:
                        print("Image Size: " + str(self.file_size(path)))

            except UnicodeEncodeError as e:
                status = 'fail'
                messages = "UnicodeEncodeError on an image...trying next one..." + " Error: " + str(e)
                return_image_name = ''
                absolute_path = ''

            except URLError as e:
                status = 'fail'
                messages = "URLError on an image...trying next one..." + " Error: " + str(e)
                return_image_name = ''
                absolute_path = ''
                
            except BadStatusLine as e:
                status = 'fail'
                messages = "BadStatusLine on an image...trying next one..." + " Error: " + str(e)
                return_image_name = ''
                absolute_path = ''

        except HTTPError as e:  
            status = 'fail'
            messages = "HTTPError on an image...trying next one..." + " Error: " + str(e)
            return_image_name = ''
            absolute_path = ''

        except URLError as e:
            status = 'fail'
            messages = "URLError on an image...trying next one..." + " Error: " + str(e)
            return_image_name = ''
            absolute_path = ''

        except ssl.CertificateError as e:
            status = 'fail'
            messages = "CertificateError on an image...trying next one..." + " Error: " + str(e)
            return_image_name = ''
            absolute_path = ''

        except IOError as e:  
            status = 'fail'
            messages = "IOError on an image...trying next one..." + " Error: " + str(e)
            return_image_name = ''
            absolute_path = ''

        except IncompleteRead as e:
            status = 'fail'
            messages = "IncompleteReadError on an image...trying next one..." + " Error: " + str(e)
            return_image_name = ''
            absolute_path = ''

        return status,messages,return_image_name,absolute_path


    def _get_next_item(self,s):
        line1 = s.find('rg_meta notranslate')
        if line1 == -1:  
            end_quote = 0
            link = "no_links"
            return link, end_quote
        else:
            line1 = s.find('class="rg_meta notranslate">')
            start_object = s.find('{', line1 + 1)
            end_object = s.find('</div>', start_object + 1)
            object_raw = str(s[start_object:end_object])
         
            version = (3, 0)
            cur_version = sys.version_info
            if cur_version >= version: 
                try:
                    object_decode = bytes(object_raw, "utf-8").decode("unicode_escape")
                    final_object = json.loads(object_decode)
                except:
                    final_object = ""
            else: 
                try:
                    final_object = (json.loads(self.repair(object_raw)))
                except:
                    final_object = ""
            return final_object, end_object
    
    def _get_images(self,page,directory_1,dir_name,limit,args):
        items = []
        abs_path = []
        CountError = 0
        i = 0
        count = 1
        while count < limit+1:
            object, end_content = self._get_next_item(page)
            if object == "no_links":
                break
            elif object == "":
                page = page[end_content:]
            elif args['offset'] and count < int(args['offset']):
                    count += 1
                    page = page[end_content:]
            else:
                
                object = self.object_format(object)
                if args['metadata']:
                    if not args["silent_mode"]:
                        print("\nImage Metadata: " + str(object))

                status,messages,return_image_name,absolute_path = self.image_download(object['image_link'],object['image_formats'],directory_1,dir_name,count,args['print_urls'],args['socket_timeout'],args['prefix'],args['print_size'],args['no_numbering'],args['no_download'],args['save_source'],object['image_source'],args["silent_mode"],args["thumbnail_only"],args['format'],args['ignore_urls'])
                if not args["silent_mode"]:
                    print(messages)
                if status == "success":

              
                    if args['thumbnail'] or args["thumbnail_only"]:
                        status, messages_thumbnail = self.image_download_thumbnail(object['image_thumbnail_url'],directory_1,dir_name,return_image_name,args['print_urls'],args['socket_timeout'],args['print_size'],args['no_download'],args['save_source'],object['image_source'],args['ignore_urls'])
                        if not args["silent_mode"]:
                            print(messages_thumbnail)

                    count += 1
                    object['image_filename'] = return_image_name
                    items.append(object) 
                    abs_path.append(absolute_path)
                else:
                    CountError += 1

                if args['delay']:
                    time.sleep(int(args['delay']))

                page = page[end_content:]
            i += 1
        if count < limit:
            print("\n\nUnfortunately all " + str(
                limit) + "error. " + str(
                count-1) + " is all we got for this search filter!")
        return items,CountError,abs_path



    def download(self,args):
        paths_agg = {}

        if __name__ != "__main__":
        
            if 'config_file' in args:
                records = []
                json_file = json.load(open(args['config_file']))
                for record in range(0, len(json_file['Records'])):
                    args = {}
                    for i in args_list:
                        args[i] = None
                    for key, value in json_file['Records'][record].items():
                        args[key] = value
                    records.append(args)
                total_errors = 0
                for rec in records:
                    paths, errors = self.extract_download(rec)
                    for i in paths:
                        paths_agg[i] = paths[i]
                    if not args["silent_mode"]:
                        if args['print_paths']:
                            print(paths.encode('raw_unicode_escape').decode('utf-8'))
                    total_errors = total_errors + errors
                return paths_agg,total_errors
           
            else:
                paths, errors = self.extract_download(args)
                for i in paths:
                    paths_agg[i] = paths[i]
                if not args["silent_mode"]:
                    if args['print_paths']:
                        print(paths.encode('raw_unicode_escape').decode('utf-8'))
                return paths_agg, errors
       
        else:
            paths, errors = self.extract_download(args)
            for i in paths:
                paths_agg[i] = paths[i]
            if not args["silent_mode"]:
                if args['print_paths']:
                    print(paths.encode('raw_unicode_escape').decode('utf-8'))
        return paths_agg, errors

    def extract_download(self,args):
        paths = {}
        CountError = None
        for arg in args_list:
            if arg not in args:
                args[arg] = None
  
        if args['keyword']:
            search_keyword = [str(item) for item in args['keyword'].split(',')]

        if args['keyword_from_file']:
            search_keyword = self.keyword_from_file(args['keyword_from_file'])


        if args['time'] and args['time_range']:
            raise ValueError('Either time or time range should be used in a query. Both cannot be used at the same time.')


        if args['size'] and args['exact_size']:
            raise ValueError('Either "size" or "exact_size" should be used in a query. Both cannot be used at the same time.')

       
        if args['image_directory'] and args['no_directory']:
            raise ValueError('You can either specify image directory or specify no image directory, not both!')
        if args['suffix_keyword']:
            suffix_keyword = [" " + str(sk) for sk in args['suffix_keyword'].split(',')]
        else:
            suffix_keyword = ['']

    
        if args['prefix_keyword']:
            prefix_keyword = [str(sk) + " " for sk in args['prefix_keyword'].split(',')]
        else:
            prefix_keyword = ['']

      
        if args['limit']:
            limit = int(args['limit'])
        else:
            limit = 100

        if args['url']:
            current_time = str(datetime.datetime.now()).split('.')[0]
            search_keyword = [current_time.replace(":", "_")]

        if args['similar_images']:
            current_time = str(datetime.datetime.now()).split('.')[0]
            search_keyword = [current_time.replace(":", "_")]

       
        if args['single_image'] is None and args['url'] is None and args['similar_images'] is None and \
                        args['keyword'] is None and args['keyword_from_file'] is None:
            print('-------------------------------\n'
                  'Uh oh! keyword is a required argument \n\n'
                  'Please refer to the documentation on guide to writing queries \n'
                  'https://github.com/hardikvasa/google-images-download#examples'
                  '\n\nexiting!\n'
                  '-------------------------------')
            sys.exit()

        if args['output_directory']:
            directory_1 = args['output_directory']
        else:
            directory_1 = "downloads"

     
        if args['proxy']:
            os.environ["http_proxy"] = args['proxy']
            os.environ["https_proxy"] = args['proxy']
          
        total_errors = 0
        for pky in prefix_keyword:               
            for sky in suffix_keyword:            
                i = 0
                while i < len(search_keyword):  
                    iteration = "\n" + "Item no.: " + str(i + 1) + " -->" + " Item name = " + (pky) + (search_keyword[i]) + (sky)
                    if not args["silent_mode"]:
                        print(iteration.encode('raw_unicode_escape').decode('utf-8'))
                        print("Evaluating...")
                    else:
                        print("Downloading images for: " + (pky) + (search_keyword[i]) + (sky) + " ...")
                    search_term = pky + search_keyword[i] + sky

                    if args['image_directory']:
                        dir_name = args['image_directory']
                    elif args['no_directory']:
                        dir_name = ''
                    else:
                        dir_name = search_term + ('-' + args['color'] if args['color'] else '')  

                    if not args["no_download"]:
                        self.create_directories(directory_1,dir_name,args['thumbnail'],args['thumbnail_only'])    

                    params = self.build_url_parameters(args)     

                    url = self.build_search_url(search_term,params,args['url'],args['similar_images'],args['specific_site'],args['safe_search'])   


                    if limit < 101:
                        raw_html = self.download_page(url) 
                    else:
                        raw_html = self.download_extended_page(url,args['chromedriver'])

                    if not args["silent_mode"]:
                        if args['no_download']:
                            print("Getting URLs without downloading images...")
                        else:
                            print("Starting Download...")
                    items,CountError,abs_path = self._get_images(raw_html,directory_1,dir_name,limit,args)   

                   
                    paths[pky + search_keyword[i] + sky] = abs_path

                   
                    if args['extract_metadata']:
                        try:
                            if not os.path.exists("logs"):
                                os.makedirs("logs")
                        except OSError as e:
                            print(e)
                        json_file = open("logs/"+search_keyword[i]+".json", "w")
                        json.dump(items, json_file, indent=4, sort_keys=True)
                        json_file.close()

                    if args['related_images']:
                        print("\nGet the lsit of related Items")
                        tabs = self.get_all_tabs(raw_html)
                        for key, value in tabs.items():
                            final_search_term = (search_term + " - " + key)
                            print("\nNow Downloading - " + final_search_term)
                            if limit < 101:
                                new_raw_html = self.download_page(value)
                            else:
                                new_raw_html = self.download_extended_page(value,args['chromedriver'])
                            self.create_directories(directory_1, final_search_term,args['thumbnail'],args['thumbnail_only'])
                            self._get_images(new_raw_html, directory_1, search_term + " - " + key, limit,args)

                    i += 1
                    total_errors = total_errors + CountError
                    if not args["silent_mode"]:
                        print("\nErrors: " + str(CountError) + "\n")
        return paths, total_errors


def main():
    records = input_from_user()
    total_errors = 0
    t0 = time.time()  
    for args in records:

        if args['single_image']: 
            res = googleimagesdownload()
            res.single_image(args['single_image'])
        else:  
            res = googleimagesdownload()
            paths,errors = res.download(args)  
            total_errors = total_errors + errors

        t1 = time.time() 
        total_time = t1 - t0  
        if not args["silent_mode"]:
            print("\nEverything downloaded!")
            print("Total errors: " + str(total_errors))
            print("Total time taken: " + str(total_time) + " Seconds")

if __name__ == "__main__":
    main()


