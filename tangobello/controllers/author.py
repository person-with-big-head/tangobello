import math
from urllib.parse import quote

from bottle import get, redirect

from tangobello.models import BasketArticleList, Authors, Categories
from tangobello.serializers import basket_article_list_serializer
from tangobello.utils import template
from tangobello.plugins import boilerplate_plugin


@get('/author/<author_id>', skip=[boilerplate_plugin])
@template('author.html')
def author(author_id):

    # get author information
    author_info = (Authors.get(Authors.author_id == author_id))

    # get posts list.
    article_list = (BasketArticleList.select()
                    .join(Categories, on=(Categories.category_id == BasketArticleList.category))
                    .where(BasketArticleList.author == author_info.author_id)
                    .order_by(BasketArticleList.updated_at).limit(10))

    for post in article_list:
        post.author = author_info

    # get page number
    page_num = math.ceil(len(BasketArticleList.select(BasketArticleList.post_id)) / 10)

    return {
        'article_list': basket_article_list_serializer.dump(article_list, many=True).data,
        'current_page': 1,
        'max_page': page_num,
        'author': author_info
    }


@get('/author/<author_id>/page/<page:int>', skip=[boilerplate_plugin])
@template('author.html')
def author(author_id, page):
    if page == 1:
        redirect('/author/' + quote(author_id))
    # get author information
    author_info = (Authors.get(Authors.author_id == author_id))

    # get posts list.
    article_list = (BasketArticleList.select()
                    .join(Categories, on=(Categories.category_id == BasketArticleList.category))
                    .where(BasketArticleList.author == author_info.author_id)
                    .order_by(BasketArticleList.updated_at).paginate(page, 10))

    for post in article_list:
        post.author = author_info

    # get page number
    page_num = math.ceil(len(BasketArticleList.select(BasketArticleList.post_id)) / 10)

    return {
        'article_list': basket_article_list_serializer.dump(article_list, many=True).data,
        'current_page': page,
        'max_page': page_num,
        'author': author_info
    }
