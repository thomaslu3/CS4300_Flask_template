from bs4 import BeautifulSoup as BSHTML
import urllib.request
import json
import re
import codecs
from urllib.request import Request, urlopen


def getImageURL(siteURL):
    req = Request(siteURL, headers={'User-Agent': 'Mozilla/5.0'})
    try:
        page = urlopen(req).read()

        # page = urllib.request.urlopen(siteURL)
        # page = urllib.request.urlopen(siteURL).read().decode('utf-8')
        soup = BSHTML(page, 'html.parser')
        # page_text = str(soup.prettify())
        # decoded_page_text = codecs.decode(page_text, 'unicode-escape')
        # print(decoded_page_text)
        # print(page_text)
        # imageURL = re.search(r"^{\"\@context\":\"http:\/\/schema\.org\".+\"url\":\"https:\/\/www\.food\.com\"\}\}$", decoded_page_text).group(1)
        # print(imageURL)
        # with open("output.html", "w", encoding = 'utf-8') as file:
        # # prettify the soup object and convert it into a string  
        #     file.write(str(soup.prettify()))
        images = soup.find_all('meta', {"name" : "og:image"})
        if(len(images) > 0 and not images[0]['content'] == "https://geniuskitchen.sndimg.com/fdc-new/img/fdc-shareGraphic.png"):
            return images[0]['content']
        else:
            return "../static/images/recipe-placeholder-image.svg"
    except:
        print("Failed to fetch image.")
        return "../static/images/recipe-placeholder-image.svg"