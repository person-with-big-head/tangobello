import math
from bottle import get, redirect

from tangobello.models import BasketArticleList, Authors, Categories
from tangobello.serializers import post_serializer
from tangobello.utils import template
from tangobello.plugins import boilerplate_plugin


@get('/author/<author_name>', skip=[boilerplate_plugin])
@template('author.html')
def author(author_name):

    # get author information
    author_info = (Authors.get(Authors.author_name == author_name))

    # get posts list.
    article_list = (BasketArticleList.select()
                    .join(Categories, on=(Categories.category_id == BasketArticleList.category))
                    .where(BasketArticleList.author == author_info.author_id)
                    .order_by(BasketArticleList.post_date).limit(10))

    for post in article_list:
        post.author = author_info

    # get page number
    page_num = math.ceil(len(BasketArticleList.select(BasketArticleList.post_id)) / 10)

    return {
        'article_list': post_serializer.dump(article_list, many=True).data,
        'current_page': 1,
        'max_page': page_num,
        'author': author_info
    }


@get('/author/<author_name>/page/<page:int>', skip=[boilerplate_plugin])
@template('author.html')
def author(author_name, page):
    if page == 1:
        redirect('/author/' + author_name)
    # get author information
    author_info = (Authors.get(Authors.author_name == author_name))

    # get posts list.
    article_list = (BasketArticleList.select()
                    .join(Categories, on=(Categories.category_id == BasketArticleList.category))
                    .where(BasketArticleList.author == author_info.author_id)
                    .order_by(BasketArticleList.post_date).paginate(page, 10))

    for post in article_list:
        post.author = author_info

    # get page number
    page_num = math.ceil(len(BasketArticleList.select(BasketArticleList.post_id)) / 10)

    return {
        'article_list': post_serializer.dump(article_list, many=True).data,
        'current_page': page,
        'max_page': page_num,
        'author': author_info
    }
