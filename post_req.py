import requests
from pathlib import Path
from bs4 import BeautifulSoup
import csv
import time
import logging

header={
'authority': 'www.monlamdic.com',
'method': 'POST',
'path': '/',
'scheme': 'https',
'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
'accept-encoding': 'gzip, deflate, br',
'accept-language': 'en-US;q=0.8',
'cache-control': 'max-age=0',
'content-length': '175',
'content-type': 'application/x-www-form-urlencoded',
'cookie': 'PHPSESSID=7a1f54060475238d662a42e50b39df0c',
'origin': 'https://www.monlamdic.com',
'referer': 'https://www.monlamdic.com/',
'sec-fetch-dest': 'document',
'sec-fetch-mode': 'navigate',
'sec-fetch-site': 'same-origin',
'sec-fetch-user': '?1',
'sec-gpc': '1',
'upgrade-insecure-requests': '1',
'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.61 Safari/537.36'
}

url = "https://www.monlamdic.com"
var = ""

def make_request():
    data = {"dictionarys":"བོད་ཡིག","dic-keyword":var,"submit_search":""}
    res = requests.post(url,headers = header,data=data)
    return res.text

def extract_page(page):
    soup =BeautifulSoup(page,'html.parser')
    dic_body = soup.select_one("div.dic-body-bag.row.bg-white.border-0.rounded-3")
    text_definitions = dic_body.findChildren(recursive=False)
    csv_col = [var] 
    for index,definition in enumerate(text_definitions):
        if index == 0:
            first_definition = definition.select_one("div#dic-body")
            if  pos := first_definition.select_one("p.gap"):
                first_word = first_definition.text.replace(pos.text,"")
                pos = get_pos(pos.text)
            else:
                first_word = first_definition.text  
                pos = get_pos(first_definition.text)

            first_word = filter_texts(first_word)
            first_word = first_word.replace(pos,"")
            csv_col.extend([pos,first_word])
        else:
            definition = filter_texts(definition.text)
            csv_col.append(definition)
    return csv_col      

def get_pos(pos):
    ext_pos = ""
    if "མིང་ཚིག" in pos:
        ext_pos += "མིང་ཚིག,"
    if "བསྣན་ཚིག" in pos: 
        ext_pos+="བསྣན་ཚིག,"
    if "བྱ་ཚིག" in pos:
        ext_pos+="བྱ་ཚིག,"   
    if "རྒྱན་ཚིག" in pos:
        ext_pos+="རྒྱན་ཚིག," 
    if "འབོད་ཚིག" in pos:
        ext_pos+="འབོད་ཚིག," 
    if "འཇལ་ཚིག" in pos:
        ext_pos+="འཇལ་ཚིག," 
    if ext_pos == "":
        ext_pos = pos
    ext_pos = filter_texts(ext_pos)

    return ext_pos[:-1]    

def filter_texts(word):
    word = word.replace("\r\n","")
    word = word.replace("\n","")
    word = word.replace("xa0","")
    word = word.replace("དཔེ་རིས།","")
    word = ' '.join(word.split())
    return word.strip()



def get_search_word():
    file = open("./dic/dic_split_2.csv")
    csvreader = csv.reader(file)
    do_bool = False
    for row in csvreader:
        last_word = ""
        if last_word == "":
            do_bool = True 
        if do_bool:
            yield row[0]
        if last_word == row[0]:
            do_bool = True 

def write_csv(csv_col):
    with open("new_monlam.csv","a") as f:
        csv_writer = csv.writer(f)
        csv_writer.writerow(csv_col)
        
def set_up_logger(logger_name):
        logger = logging.getLogger(logger_name)
        formatter = logging.Formatter("%(message)s")
        fileHandler = logging.FileHandler(f"{logger_name}.log")
        fileHandler.setFormatter(formatter)
        logger.setLevel(logging.INFO)
        logger.addHandler(fileHandler)

        return logger

def main():
    global var
    search_words = get_search_word()
    processed_words = set_up_logger("processed_words")
    err = set_up_logger("err")
    for index,search_word in enumerate(search_words): 
        try:
            var = search_word   
            page = make_request()
            print(search_word)
            csv_col = extract_page(page)
            write_csv(csv_col)
            processed_words.info(search_word)
        except:
            err.info(search_word)


def main_test():
    global var
    search_word = "ཀཔྱཀ་"
    var = search_word   
    page = make_request()
    print(search_word)
    csv_col = extract_page(page)
    write_csv(csv_col)
        
if __name__ == "__main__":
    start_time = time.time()
    main()
    print("--- %s seconds ---" % (time.time() - start_time))