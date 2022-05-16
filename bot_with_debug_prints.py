# Pretty much the same, this is file with useful print's for debug.


from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from bs4 import BeautifulSoup
import requests
import random

HEADERS2 = {
    'accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    'referer': 'https://www.kinopoisk.ru/',
    'cookie': 'yandexuid=9340739331645942432; yuidss=9340739331645942432; ymex=1961302432.yrts.1645942432#1961302432.yrtsi.1645942432; gdpr=0; _ym_uid=1645949360955899169; is_gdpr=0; is_gdpr_b=CLfGQxDTaSgC; my=YwA=; yandex_gid=214; _ym_d=1652247493; yabs-frequency=/5/0000000000000000/1LmOhY66wcE4HY4YxKy43AJ6ReH68m00/; computer=1; FgkKdCjPqoMFm=1; i=eJf5R2Xe26D/vvq4yYOijutNrz4PHcC/JH+sF6JJu/wwgQexUK94TSL2mRXblLjxNJtVXz3vbSkkUxonVk+h9D9h6sA=; skid=9152519791652354546; _ym_isad=1; yandex_login=; ys=c_chck.3538942991',
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.60 Safari/537.36'
}
HEADERS = {
    'cookie': 'mda_exp_enabled=1; yandex_login=pereg.sergey; yandexuid=6332085291630942024; gdpr=0; _ym_uid=1631552610117021587; yuidss=6332085291630942024; i=jokAsPWUvwFQUOZHFyS0Id80GhrYlA1cxLD9Yna/Ptzvrk1ffxcUadXggisvs8wJ9VcVKKmfetgRy4duAJIUe3ih/qk=; mykp_button=movies; my_perpages=%5B%5D; mustsee_sort_v5=00.10.200.21.31.41.121.131.51.61.71.81.91.101.111; _yasc=zc8bpKYWvvUMsPreMXXlLzTluWb8UymQSgMdZuOLJciW9g==; desktop_session_key=c57b0da9388339b2669b9ab39dbebc2db1bfdb764e31cb792b7d1d9a17e110377105942421d62f56928fa4bf026d7a0c943c2e889823bcbfc3d2005e6febfd47b9d6ab66c9e5cbcf0d79d1d47e65b904beb63cdcf5825bdb71d011990a5c12c1; desktop_session_key.sig=3rLO6UwxeeeKMaRxqPWyveoTsM0; ys=udn.cDrQodC10YDQs9C10Lkg0J/QtdGA0LXQs9GD0LTQvtCy#c_chck.2013928299; _csrf=f7PFD-bUKD-ezv2AIBCPJNHa; ya_sess_id=3:1652017915.5.0.1631216691905:xphX1Q:15.1.2:1|675380481.0.2|30:207067.260217.BqiPcq3apN9jVYnGBRCw4YCKswI; mda2_beacon=1652017915895; sso_status=sso.passport.yandex.ru:blocked; _ym_isad=1; yp=1652104330.yu.6332085291630942024; ymex=1654609930.oyu.6332085291630942024; location=1; PHPSESSID=5d22189297de7899eeb7fb054bdf85a9; user_country=ru; yandex_gid=10716; tc=5961; uid=15887248; crookie=AHpzlSzEido/MY3Xdyc2WLAIuPCw6C0Sf3542e+t3ahS7hSQBJi+v70RPDrTf+KicQf69LT4mtPC7I+uIKXjLoYGmZc=; cmtchd=MTY1MjAxNzk1MTczOA==; _csrf_csrf_token=9vr4DJ4yAepPwNdqjQMg_5fUk3RscWWCVGxncI4GkMo; mobile=no; _ym_visorc=b; _ym_d=1652025873',
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.60 Safari/537.36'
}
bot = Bot(token='5104064495:AAHA7MZhmh6INQE5J1MbyDFfE-Xe43CBcio')
dp = Dispatcher(bot)

def convert_link_to_soup(link):
    response = requests.get(link, headers=HEADERS)
    soup = BeautifulSoup(response.content, "lxml")
    html = str(response.content)
    return html, soup


def get_kinopoisk_html(message):
    response = requests.get("https://www.google.com/search?q=kinpoisk+{}".format(message), headers=HEADERS)
    html = response.content.decode('ISO-8859-1')
    start = html.find("https://www.kinopoisk")
    end = html[start:].find('&')
    end = min(end, html[start:].find("\""))
    print(html[start:start + end], "AAAAAAAAAAA")
    response = requests.get(html[start:start + end], headers=HEADERS)
    soup = BeautifulSoup(response.content, "lxml")
    html = str(response.content)
    print(html)
    return html, soup


def get_imdb_html(message):
    response = requests.get("https://www.google.com/search?q=imdb+{}".format(message), headers=HEADERS)
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


def get_everything_about_movie(html, soup):
    try:
        kinopoisk_rating, imdb_rating = get_rating(html)
    except Exception:
        # await bot.send_message(message.chat.id, "I don't know this movie:(")
        raise "bad_request"
    markup = types.InlineKeyboardMarkup()
    lst = []
    ivi_link = get_ivi_link(html)
    kion_link = get_kion_link(html)
    appleTV_link = get_appleTV(html)

    if ivi_link is not None:
        item1 = types.InlineKeyboardButton(text='Watch at IVI', url=str(get_ivi_link(html)))
        lst.append(item1)
    if kion_link is not None:
        item2 = types.InlineKeyboardButton(text='Watch at KION', url=str(get_kion_link(html)))
        lst.append(item2)
    if appleTV_link is not None:
        item3 = types.InlineKeyboardButton(text='Watch at appleTV', url=str(get_appleTV(html)))
        lst.append(item3)
    markup.add(*lst)

    get_kion_link(html)
    get_appleTV(html)
    synopsis = get_synopsis(soup)
    # print(str(get_ivi_link(html)))
    poster = get_poster(soup)
    return kinopoisk_rating, imdb_rating, poster, synopsis, markup


def get_rating(html):
    print()
    print()
    print()
    html = str(html)
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
    if link_start == -1:
        return None
    link_end = link_start + html[link_start:].find("\"")
    print(html[link_start:link_end])
    return html[link_start:link_end]


def get_kion_link(html):
    link_start = html.find('https://kion')
    if link_start == -1:
        return None
    link_end = link_start + html[link_start:].find("\"")
    print(html[link_start:link_end])
    return html[link_start:link_end]


def get_appleTV(html):
    link_start = html.find('https://tv.apple')
    if link_start == -1:
        return None
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
    if result is None:
        result = soup.find("img",
                           class_="film-poster styles_root__24Jga styles_rootInDark__64LVq image styles_root__DZigd")
    return result.get("src")


def writer(kp_rating, imdb_rating, synopsis):
    message = ""
    if (float(kp_rating) + float(imdb_rating)) / 2 >= 8.2:
        message += "Фильм крайне рекомендуется к просмотру!\n"
    message += "Рейтинг на Кинопоиске: " + kp_rating + '\n' + "Рейтинг на IMDB: " + imdb_rating + '\n' + 'Синопсис:\n'
    message += synopsis
    return message


async def print_data_to_user(html, soup, message):
    try:
        kinopoisk_rating, imdb_rating = get_rating(html)
    except Exception:
        await bot.send_message(message.chat.id, "Уверены, что это фильм? Я о таком не слышал;)")
        raise "bad_request"

    kinopoisk_rating, imdb_rating, poster, synopsis, markup = get_everything_about_movie(html, soup)

    if poster is not None:
        print("https:" + poster)
        await message.reply_photo("https:" + poster)
    print(synopsis)
    await bot.send_message(message.chat.id, writer(kinopoisk_rating, imdb_rating, synopsis), reply_markup=markup)


@dp.message_handler(commands=["recommend_me_a_good_movie"])
async def get_random_movie_from_top500(message):
    rand = random.randint(1, 500)
    page_number = (rand - 1) // 50 + 1
    response = requests.get("https://www.kinopoisk.ru/lists/movies/top500/?page={}".format(page_number),
                            headers=HEADERS)
    soup = BeautifulSoup(response.content, "lxml")
    print(rand)
    result = soup.find_all("div", class_="styles_main__Y8zDm styles_mainWithNotCollapsedBeforeSlot__x4cWo")[
        rand % 50].find("a", href=True).get("href")
    print("https://www.kinopoisk.ru" + result)
    response = requests.get("https://www.kinopoisk.ru" + result, headers=HEADERS2)
    print(response.content)
    soup = BeautifulSoup(response.content, "lxml")
    html = response.content
    html = str(html)
    await print_data_to_user(html, soup, message)


@dp.message_handler(commands=["start"])
async def launch(message):
    await bot.send_message(message.chat.id,
                           "Добро пожаловать!\n Вы можете запросить информацию по любому фильму. Для этого просто введите его название.\n"
                           "Если Вы не знаете, что посмотреть, просто наберите /recommend_me_a_good_movie")


@dp.message_handler(commands=["help"])
async def launch(message):
    await bot.send_message(message.chat.id,
                           "Здесь вы можете запросить информацию по любому фильму. Для этого просто введите его название.\n"
                           "Если Вы не знаете, что посмотреть, просто наберите /recommend_me_a_good_movie")


@dp.message_handler(content_types=["text"])
async def launch(message):
    response = requests.get("https://www.kinopoisk.ru/film/326/", headers=HEADERS2)
    print(response.content)
    html, soup = get_kinopoisk_html(message.text)
    try:
        kinopoisk_rating, imdb_rating = get_rating(html)
    except Exception:
        await bot.send_message(message.chat.id, "Уверены, что это фильм? Я о таком не слышал;)")
        raise "bad_request"

    await print_data_to_user(html, soup, message)


if __name__ == '__main__':
    executor.start_polling(dp)
