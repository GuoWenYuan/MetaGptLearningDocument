import requests
from bs4 import BeautifulSoup
from pydantic import BaseModel


class Spider(BaseModel):
    """爬虫工具"""

    #基础网页地址
    base_url: str



    @staticmethod
    def get_urls(base_url):
        response = requests.get(base_url)
        if response.status_code == 200:
            # 解析网页内容
            soup = BeautifulSoup(response.content, 'html.parser')

            href_attributes = [dd_a['href'] for dd_a in soup.select('div.book_last dd a')]

            # Print the extracted href attributes
            index = 0
            for href in href_attributes:
                print(href)
                index += 1
                if index == 2:
                    return
        else:
            print(f'Error: Unable to retrieve the webpage. Status code: {response.status_code}')

    @staticmethod
    def get_html(url):
        return requests.get(url).text


#Spider.get_urls('https://8a6214.bqg996.com/book/35164/list.html')
print(Spider.get_html('https://8a6214.bqg996.com//book/35164/1079.html'))