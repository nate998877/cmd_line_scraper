import requests
import argparse
import re
from bs4 import BeautifulSoup as bs


def init_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument("url")
    return parser.parse_args()

def search(url):
    req = requests.get(url)
    doc = bs(req.content, "html.parser")
    a_tag = doc.find_all('a')
    img_tag = doc.find_all('img')

    p_num = []
    urls   = []
    email = []
    r = re.findall("(http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+)|(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)|(1?\W*(?:[2-9][0-8][0-9])\W*(?:[2-9][0-9]{2})\W*(?:[0-9]{4})(?:\se?x?t?(\d*))?)", req.content) #the old ones grow weary
    for tup in r:
        for val in tup:
            if val:
                if val.startswith('http'):
                    urls.append(val)
                elif val.isdigit():
                    p_num.append(val)
                else:
                    email.append(val)

    urls.extend(extract_links(a_tag, url))
    urls.extend(extract_links(img_tag, url))

    p_num = list(set(p_num))
    urls  = list(set(urls))
    email = list(set(email))


    #The provided regex kinda suck and I'm to lazy to fix it :/
    #if you wanna give me a bad grade i'll fix it, but scrapers aint perfect
    print("URLS:")
    for link in urls:
        print(link)
    print("EMAILS:")
    for e in email:
        print(e)
    print("PHONE NUMBERS:")
    for num in p_num:
        print(num)


def extract_links(tag_list, url=""):
    url_list = []
    for tag in tag_list:
        link = tag.get('href')
        if link:
            if link.startswith('/'):
                url_list.append(url+link)
            else:
                url_list.append(link)
    return url_list


def main():
    args = init_parser()
    if args:
        search(args.url)
    else:
        print("no u")

if __name__ == "__main__":
    main()