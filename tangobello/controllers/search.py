import json
import math

from bottle import get
from elasticsearch import Elasticsearch
from tangobello.utils import template, plain_query
from tangobello.plugins import boilerplate_plugin


@get('/search', skip=[boilerplate_plugin])
@template('search.html')
def search():
    args = plain_query()

    search_keyword = args.get('keyword')
    if not search_keyword:
        return {
            "posts": [],
            "search_keyword": None,
            "current_page": 1,
            "max_page": 0,
        }

    current_page = args.get('page')
    if not current_page:
        current_page = 1

    page_size = 10
    current_page = int(current_page)
    print(current_page)
    es = Elasticsearch('139.224.105.129')
    body = {
        "from": (current_page - 1) * 10,
        "size": page_size,
        "query": {
            "multi_match": {
                "query": search_keyword,
                "fields": ["article_summary", "article_title"]
            }
        },
        "highlight": {
            "pre_tags": [
                "<em class=\"highlight\">"
            ],
            "post_tags": [
                "</em>"
            ],
            "fields": {
                "article_title": {},
                "article_summary": {}
            }
        }
    }

    search_result = es.search(index='pool_articles', doc_type='info', body=body)
    posts = search_result['hits']['hits']
    for post in posts:
        # highlight
        highlight = post.get('highlight')
        if highlight and highlight.get('article_title'):
            post['_source']['article_title'] = highlight.get('article_title')[0]
        if highlight and highlight.get('article_summary'):
            post['_source']['article_summary'] = "".join(highlight.get('article_summary'))

        post['_source']['article_img_list'] = json.loads(post['_source']['article_img_list'])

    max_page = math.ceil(search_result['hits']['total'] / page_size)

    return {
        "posts": posts,
        "search_keyword": search_keyword,
        "current_page": current_page,
        "max_page": max_page
    }
