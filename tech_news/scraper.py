import requests
from parsel import Selector
import time
import re


# Requisito 1
def fetch(url):
    time.sleep(1)
    try:
        response = requests.get(
            url, headers={"user-agent": "Fake user-agent"}, timeout=3
        )
        if response.status_code == 200:
            return response.text
        else:
            return None
    except requests.ReadTimeout:
        return None


# Requisito 2
def scrape_updates(html_content):
    reponse = Selector(text=html_content)
    urls = reponse.css("h2.entry-title a::attr(href)").getall()
    return urls


# Requisito 3
def scrape_next_page_link(html_content):
    reponse = Selector(text=html_content)
    next_page = reponse.css("a.next.page-numbers::attr(href)").get()
    return next_page


# Requisito 4
def scrape_news(html_content):
    reponse = Selector(text=html_content)
    reading_time = reponse.css("li.meta-reading-time::text").get()
    return {
        "url": reponse.css("link[rel='canonical']::attr(href)").get(),
        "title": (reponse.css("h1.entry-title::text").get()).strip(),
        "timestamp": reponse.css("li.meta-date::text").get(),
        "writer": reponse.css("a.url.fn.n::text").get(),
        "reading_time": int(re.findall(r"\d+", reading_time)[0]),
        "summary": "".join(
            reponse.css(".entry-content > p:first-of-type *::text").getall()
        ).strip(),
        "category": reponse.css("span.label::text").get(),
    }


# Requisito 5
def get_tech_news(amount):
    """Seu código deve vir aqui"""
