import requests as _req
from json import loads as _l
import wikipedia as _wk
from re import findall as _findall

_nyt_key = "c0c5040d449544c28e803d52c20eb5d0"
_nyt_url = "https://api.nytimes.com/svc/search/v2/articlesearch.json"


class MediaAggregatorMixin:
    """
    This is the base class for all current and future media aggregators.
    """
    def __init__(self):
        pass

    def get_news(self, query):
        pass

    def get_limit(self):
        pass


class Aggregator:
    def __init__(self):
        self._params = {"q": "", "api-key": _nyt_key}

    def get_news(self, query):
        self._params["q"] = str(query)
        response = _req.get(_nyt_url, params = self._params)
        return [x["web_url"] for x in response.json()["response"]["docs"] if x["type_of_material"] == "News"]

    def get_limit(self):
        return self._limit

def shorten_news(url, n = 5):
    from bs4 import BeautifulSoup as bs
    from summarizer import FrequencySummarizer as fs
    response = _req.get(url)
    if not response.ok:
        return False
    page = response.content
    soup = bs(page, "lxml")
    summary = fs().summarize("\n".join([x.text for x in soup.findAll("p") if len(x.text.split()) > 1]), n)
    summary.insert(0, soup.title.text)
    return ' '.join(summary)


def get_gkg(query):
    try:
        s = _wk.summary(query, sentences = 5)
        for x in _findall("\(.*\)", s):
            s = s.replace(x, "")
        return s
    except:
        return False