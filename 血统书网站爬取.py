import time
import re
import os
import aiohttp
import asyncio
from bs4 import BeautifulSoup
import pandas as pd
from aiohttp import web
from urllib import parse


async def main():
    url1 = "https://studbook.jp/users/ja/Search_chichi_shushiba_list.php?pageID="
    url2 = "&hid=32005331082&order=tanetsuke_desc&TanetsukeYear=0"
    num_iterations = int(input("请输入需要的页数（整数）\n"))
    farms = []
    mother_urls = []
    mothers = []
    times = []
    star = []
    for page in range(num_iterations):
        url = url1 + str(page + 1) + url2
        raw_text = await fetch_content(url)
        soup = BeautifulSoup(raw_text, "html.parser")
        rows = soup.find_all('tr')
        for i in range(3, len(rows)-4, 4):
            row_text = str(rows[i])
            if '2022' in row_text:
                break
            if '★' in row_text:
                star.append('★')
            elif '☆' in row_text:
                star.append('☆')
            else:
                star.append(' ')
            farm = rows[i].find_all('td')
            farms.append(clean_text(farm[len(farm) - 2].text))
            times.append(clean_text(farm[len(farm) - 1].text))
            horses = rows[i].find_all('a')
            mothers.append(clean_text(horses[0].text))
            mother_urls.append(get_url(horses[0]))

        await asyncio.sleep(60)
    df = pd.DataFrame({
        '印': star,
        '牝马': mothers,
        '牝马所在页面': mother_urls,
        '牧场': farms,
        '配种日期与生产预定日': times
    })
    target_directory = "D:/111/"
    os.makedirs(target_directory, exist_ok=True)
    file_path = os.path.join(target_directory, "output.xlsx")
    df.to_excel(file_path, index=False, engine='openpyxl')


async def fetch_content(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.text()


def clean_text(text):
    # 去除非打印字符，如全角空格
    text = re.sub(r'\u3000', ' ', text)
    # 去除前后多余的空白字符
    text = text.strip()
    # 去除多余的换行符或空行
    text = re.sub(r'\s+', ' ', text)
    # 返回处理后的文本
    return text


def get_url(horse_info):
    href = horse_info.get('href')
    target = "https://studbook.jp/users/ja/" + href
    return target


if __name__ == "__main__":
    asyncio.run(main())
