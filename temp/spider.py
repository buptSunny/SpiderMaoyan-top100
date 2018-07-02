import re
import requests
from requests.exceptions import   RequestException
from bs4 import BeautifulSoup
# 加上 headers 和 headers = headers 可以避免反爬虫

def find_last(string,str):
    last_position=-1
    while True:
        position=string.find(str,last_position+1)
        if position==-1:
            return last_position
        last_position=position


def get_one_page(url):

    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.117 Safari/537.36'
        }
        response = requests.get(url,headers = headers)
        if response.status_code==200:
            return response.text
        return None
    except RequestException:
        return None

def parse_one_page(html):
    soup = BeautifulSoup(html, "html.parser")
    names = [i.a.string for i in soup.select(".movie-item-info > .name")]
    stars = [i.string for i in soup.select(".movie-item-info > .star")]
    times = [i.string for i in soup.select(".movie-item-info > .releasetime")]
    integers = [i.string for i in soup.select(".score > .integer")]
    fractions = [i.string for i in soup.select(".score > .fraction")]
    star = []
    time = []
    score = []
    for s in stars:
        index = s.find('主演')
        lindex = find_last(s, '\n')
        star.append(s[index + 3:lindex])

    for s in times:
        index = s.find('上映时间')
        time.append(s[index + 5:])

    for x, y in zip(integers, fractions):
        score.append(x + y)

    return names, star, time, score

def write_to_file(names,stars,times,scores):
    file = open('result.txt','a',encoding='utf-8')
    file.write('%-30s %-50s %-30s %-30s' % ('电影', '主演', '上映时间', '评分:'))
    file.write('\n')

    for n,s,t,sc in zip(names,stars,times,scores):
        file.write('%-30s %-50s %-30s %-30s' % (n,s,t,sc))
        file.write('\n')
    file.close()

def main(offset):
    url = 'http://maoyan.com/board/4?offset='+str(offset)
    html = get_one_page(url)
    names,stars,times,scores = parse_one_page(html)
    print(names,stars,times,scores)
    write_to_file(names,stars,times,scores)
if __name__ =='__main__':
    file = open('result.txt','a',encoding='utf-8')
    for i in range(10):
        main(i*10)

