import json

from bottle import get
from elasticsearch import Elasticsearch
from tangobello.utils import template
from tangobello.plugins import boilerplate_plugin


@get('/search/<search_keyword>', skip=[boilerplate_plugin])
@template('search.html')
def search(search_keyword):
    es = Elasticsearch('139.224.105.129')
    body = {
        "query": {
            "multi_match": {
                "query": search_keyword,
                "fields": ["article_content", "article_title"]
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
                "article_title": {}
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

        # post date
        # post.post_date = post['_source']['post_date']

        # article_img_list
        post['_source']['article_img_list'] = json.loads(post['_source']['article_img_list'])

    return {
        'posts': posts
    }
