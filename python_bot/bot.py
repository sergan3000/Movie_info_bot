import googlesearch
import os
import asyncio
import aiohttp
import aiogram
from googlesearch import search
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from bs4 import BeautifulSoup
import json
import requests
import random
HEADERS2 = {
    'cookie': 'yandexuid=9340739331645942432; yuidss=9340739331645942432; ymex=1961302432.yrts.1645942432#1961302432.yrtsi.1645942432; gdpr=0; _ym_uid=1645949360955899169; yandex_login=sergan3000; is_gdpr=0; is_gdpr_b=CLfGQxDTaSgC; my=YwA=; yandex_gid=214; _ym_d=1652247493; yabs-frequency=/5/0000000000000000/1LmOhY66wcE4HY4YxKy43AJ6ReH68m00/; computer=1; FgkKdCjPqoMFm=1; i=eJf5R2Xe26D/vvq4yYOijutNrz4PHcC/JH+sF6JJu/wwgQexUK94TSL2mRXblLjxNJtVXz3vbSkkUxonVk+h9D9h6sA=; Session_id=3:1652339649.5.0.1645969978890:lAuvXQ:2b.1.2:1|566715140.0.2|3:252225.951214.06mmpltrDR31BUJ4YdZdkomNM9c; sessionid2=3:1652339649.5.0.1645969978890:lAuvXQ:2b.1.2:1|566715140.0.2|3:252225.951214.06mmpltrDR31BUJ4YdZdkomNM9c; skid=9152519791652354546; ys=udn.cDpzZXJnYW4zMDAw#c_chck.527365093',
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.60 Safari/537.36'
}
HEADERS = {
    'cookie': "yandexuid=9340739331645942432; yuidss=9340739331645942432; ymex=1961302432.yrts.1645942432#1961302432.yrtsi.1645942432; gdpr=0; _ym_uid=1645949360955899169; yandex_login=sergan3000; is_gdpr=0; is_gdpr_b=CLfGQxDTaSgC; my=YwA=; yandex_gid=214; _ym_d=1652247493; yabs-frequency=/5/0000000000000000/1LmOhY66wcE4HY4YxKy43AJ6ReH68m00/; computer=1; FgkKdCjPqoMFm=1; i=eJf5R2Xe26D/vvq4yYOijutNrz4PHcC/JH+sF6JJu/wwgQexUK94TSL2mRXblLjxNJtVXz3vbSkkUxonVk+h9D9h6sA=; Session_id=3:1652339649.5.0.1645969978890:lAuvXQ:2b.1.2:1|566715140.0.2|3:252225.951214.06mmpltrDR31BUJ4YdZdkomNM9c; sessionid2=3:1652339649.5.0.1645969978890:lAuvXQ:2b.1.2:1|566715140.0.2|3:252225.951214.06mmpltrDR31BUJ4YdZdkomNM9c; skid=9152519791652354546; ys=udn.cDpzZXJnYW4zMDAw#c_chck.1955606148; _ym_isad=1",
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.60 Safari/537.36'
}
bot = Bot(token='5285528755:AAEWKYjS0JyXqFhzaPhuBeEYo8sN62r8vvM')
dp = Dispatcher(bot)

def convert_link_to_soup(link):
    response = requests.get(link, headers=HEADERS)
    soup = BeautifulSoup(response.content, "lxml")
    html = str(response.content)
    return html, soup
# @dp.message_handler()
def get_kinopoisk_html(message):
    # response = requests.get("https://www.google.com/search?q=kinpoisk+forest+showshenck+redemption")
    response = requests.get("https://www.google.com/search?q=kinpoisk+{}".format(message), headers=HEADERS)
    soup = BeautifulSoup(response.content, 'html.parser')
    # print(response.encoding)
    html = response.content.decode('ISO-8859-1')
    # print(html)
    start = html.find("https://www.kinopoisk")
    print(start)
    i = start
    print(i)
    end = html[start:].find('&')
    print(html[start:start + end])
    return convert_link_to_soup(html[start:start + end])


def get_imdb_html(arg):
    response = requests.get("https://www.google.com/search?q=imdb+inception", headers=HEADERS)
    soup = BeautifulSoup(response.content, "lxml")
    print(response.encoding)
    html = response.content.decode('ISO-8859-1')
    print(html)
    start = html.find("https://www.imdb")
    i = start
    print(i)
    end = html[start:].find('&')
    print(html[start:start + end])
    response = requests.get(html[start:start + end], headers=HEADERS)
    # soup = BeautifulSoup(response.content, 'html.parser')
    html = str(response.content)
    return html, response.text


def find_content(str_start, str_middle, str_end, html):
    start = html.find(str_start)
    middle = html[start:].find(str_middle) + start
    end = html[middle:].find(str_end) + middle
    print(start, end, middle)
    return html[middle:end]


def get_rating(html):
    print()
    print()
    print()
    print(html)
    start = html.find("film-rating-value")
    if start == -1:
        raise "bad_request"
    rating_start = start + html[start:].find('>') + 1
    rating_finish = rating_start + html[rating_start:].find('<')
    kinopoisk_film_rating = html[rating_start:rating_finish]
    imdb_start = html.find("IMDb")
    imdb_rating_finish = imdb_start + html[imdb_start:].find("</span")
    imdb_rating_start = html[:imdb_rating_finish].rfind('>') + 1
    imdb_film_rating = html[imdb_rating_start: imdb_rating_finish]
    print(kinopoisk_film_rating, imdb_film_rating)
    return kinopoisk_film_rating, imdb_film_rating


def get_ivi_link(html):
    link_start = html.find('https://www.ivi')
    link_end = link_start + html[link_start:].find("\"")
    print(html[link_start:link_end])
    return html[link_start:link_end]


def get_kion_link(html):
    link_start = html.find('https://kion')
    link_end = link_start + html[link_start:].find("\"")
    print(html[link_start:link_end])
    return html[link_start:link_end]


def get_appleTV(html):
    link_start = html.find('https://tv.apple')
    link_end = link_start + html[link_start:].find("\"")
    print(html[link_start:link_end])
    return html[link_start:link_end]


def get_short_description(soup):
    result = soup.find_all("div", class_="styles_topText__p__5L")[0]
    return result.get_text()


def get_synopsis(soup):
    result = soup.find_all("div", class_="styles_filmSynopsis__Cu2Oz")[0]
    print(result)
    return result.get_text()


def get_poster(soup):
    result = soup.find("img",
                       class_="film-poster styles_root__24Jga styles_rootInLight__GwYHH image styles_root__DZigd")
    return result.get("src")
def get_everything_about_movie(html, soup):
    try:
        kinopoisk_rating, imdb_rating = get_rating(html)
    except Exception:
        # await bot.send_message(message.chat.id, "I don't know this movie:(")
        raise "bad_request"

    # except Exception:
    #     await bot.send_message(message.chat.id, "Hm. There is no such movie!")
    markup = types.InlineKeyboardMarkup()
    item1 = types.InlineKeyboardButton(text='Watch at IVI', url=str(get_ivi_link(html)))
    markup.add(item1)
    lst = []
    lst.append(item1)
    item2 = types.InlineKeyboardButton(text='Watch at KION', url=str(get_kion_link(html)))
    markup.add(item2)
    lst.append(item2)
    item3 = types.InlineKeyboardButton(text='Watch at appleTV', url=str(get_appleTV(html)))
    markup.add(*lst)

    get_kion_link(html)
    get_appleTV(html)
    synopsis = get_synopsis(soup)
    print(str(get_ivi_link(html)))
    poster = get_poster(soup)
    return poster, synopsis, markup
# @dp.message_handler(commands=["random_top_movie"])
# async def get_random_movie_from_top500(message):
#     rand = random.randint(1, 50)
#     rand = 1
#     page_number = (rand - 1) // 50 + 1
#     response = requests.get("https://www.kinopoisk.ru/lists/movies/top500/?page=1".format(page_number), headers=HEADERS)
#     soup = BeautifulSoup(response.content, "lxml")
#     print(rand)
#
#     result = soup.find_all("div", class_="styles_main__Y8zDm styles_mainWithNotCollapsedBeforeSlot__x4cWo")[rand % 50].find("a", href=True).get("href")
#     print("https://kinopoisk.ru"+ result)
#     html, soup = convert_link_to_soup("https://kinopoisk.ru" + result)
#
#     poster, synopsis, markup = get_everything_about_movie(html, soup)
#
#     if poster is not None:
#         await message.reply_photo("https:" + poster)
#
#     await bot.send_message(message.chat.id, synopsis, reply_markup=markup)

@dp.message_handler(commands=["start"])
async def launch(message):
    # markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    # item1 = types.KeyboardButton('Watch at IVI')
    #
    # markup.add(item1)
    # await bot.send_message(message.chat.id, "You can find information about any movie you are interested in",
    #                        reply_markup=markup)
    print(1)

# @dp.message_handler(content_types=["text"])
# async def launch(message):
#     html, soup = get_kinopoisk_html(message.text)
#     try:
#         kinopoisk_rating, imdb_rating = get_rating(html)
#     except Exception:
#         # await bot.send_message(message.chat.id, "I don't know this movie:(")
#         raise "bad_request"
#
#     # except Exception:
#     #     await bot.send_message(message.chat.id, "Hm. There is no such movie!")
#
#     poster, synopsis, markup = get_everything_about_movie(html, soup)
#
#     if poster is not None:
#         await message.reply_photo("https:" + poster)
#
#     await bot.send_message(message.chat.id, synopsis, reply_markup=markup)


if __name__ == '__main__':
    executor.start_polling(dp)
