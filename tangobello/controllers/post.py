import math
from bottle import get, redirect, abort

from tangobello.utils import template
from tangobello.plugins import boilerplate_plugin
from tangobello.models import (BasketArticleList, PoolArticle,
                               Authors, Categories, ShowStatusEnum, Tags)
from tangobello.serializers import basket_article_list_serializer


@get('/', skip=[boilerplate_plugin])
@template('posts.html')
def index():
    # get posts list.
    article_list = (BasketArticleList.select().join(Authors, on=(Authors.author_id == BasketArticleList.author))
                    .join(Categories, on=(Categories.category_id == BasketArticleList.category))
                    .where(BasketArticleList.show_status == ShowStatusEnum.PUBLIC_POST.value)
                    .order_by(-BasketArticleList.updated_at).limit(10))

    # get page number
    page_num = math.ceil(len(BasketArticleList.filter(
        BasketArticleList.show_status == ShowStatusEnum.PUBLIC_POST.value)) / 10)

    # get tags
    tags = Tags.select()

    # get popular articles.
    popular_articles = (BasketArticleList.select().join(Authors, on=(Authors.author_id == BasketArticleList.author))
                        .where(BasketArticleList.show_status == ShowStatusEnum.PUBLIC_POST.value)
                        .order_by(-BasketArticleList.updated_at).limit(5))

    return {
        'article_list': basket_article_list_serializer.dump(article_list, many=True).data,
        'current_page': 1,
        'max_page': page_num,
        'tags': tags,
        'popular_posts': popular_articles,
    }


@get('/posts/page/<page:int>', skip=[boilerplate_plugin])
@template('posts.html')
def posts(page):

    # if get the first page of the posts,
    # redirect to the index page.
    if page == 1:
        redirect('/')

    # get current page posts.
    article_list = (BasketArticleList.select().join(Authors, on=(Authors.author_id == BasketArticleList.author))
                    .join(Categories, on=(Categories.category_id == BasketArticleList.category))
                    .where(BasketArticleList.show_status == ShowStatusEnum.PUBLIC_POST.value)
                    .order_by(-BasketArticleList.updated_at).paginate(page, 10))

    # get page number
    page_num = math.ceil(len(BasketArticleList.filter(
        BasketArticleList.show_status == ShowStatusEnum.PUBLIC_POST.value)) / 10)

    # get tags
    tags = Tags.select()

    # get popular articles.
    popular_articles = (BasketArticleList.select().join(Authors, on=(Authors.author_id == BasketArticleList.author))
                        .where(BasketArticleList.show_status == ShowStatusEnum.PUBLIC_POST.value)
                        .order_by(-BasketArticleList.updated_at).limit(5))

    return {
        'article_list': basket_article_list_serializer.dump(article_list, many=True).data,
        'current_page': page,
        'max_page': page_num,
        'tags': tags,
        'popular_posts': popular_articles
    }


@get('/post/<post_id>', skip=[boilerplate_plugin])
@template('post.html')
def post(post_id):
    post_ = (PoolArticle.select().join(Authors, on=(Authors.author_id == PoolArticle.author))
             .join(Categories, on=(Categories.category_id == PoolArticle.category))
             .join(BasketArticleList, on=(BasketArticleList.post_id == PoolArticle.post_id))
             .where(PoolArticle.post_id == post_id,
                    BasketArticleList.show_status == ShowStatusEnum.PUBLIC_POST.value))

    if not post_:
        abort(404, 'Page Not Found')

    return {
        'post': basket_article_list_serializer.dump(post_[0]).data,
    }
