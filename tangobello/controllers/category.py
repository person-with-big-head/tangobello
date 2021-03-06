import math
from bottle import get, redirect

from tangobello.models import BasketArticleList, Authors, Categories, Tags, ShowStatusEnum
from tangobello.serializers import basket_article_list_serializer
from tangobello.utils import template
from tangobello.plugins import boilerplate_plugin


@get('/category/<category_id>', skip=[boilerplate_plugin])
@template('category.html')
def category(category_id):

    # get category information
    category_info = (Categories.get(Categories.category_id == category_id))

    # get posts list.
    article_list = (BasketArticleList.select().join(Authors, on=(Authors.author_id == BasketArticleList.author))
                    .where(BasketArticleList.category == category_info.category_id,
                           BasketArticleList.show_status == ShowStatusEnum.PUBLIC_POST.value)
                    .order_by(-BasketArticleList.updated_at).limit(10))

    for post in article_list:
        post.category = category_info

    # get page number
    page_num = math.ceil(len(BasketArticleList.filter(
        BasketArticleList.category == category_info.category_id,
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
        'category': category_info,
        'tags': tags,
        'popular_posts': popular_articles,
    }


@get('/category/<category_id>/page/<page:int>', skip=[boilerplate_plugin])
@template('category.html')
def category(category_id, page):
    if page == 1:
        redirect('/category/' + category_id)

    # get category information
    category_info = (Categories.get(Categories.category_id == category_id))

    # get posts list.
    article_list = (BasketArticleList.select().join(Authors, on=(Authors.author_id == BasketArticleList.author))
                    .where(BasketArticleList.category == category_info.category_id,
                           BasketArticleList.show_status == ShowStatusEnum.PUBLIC_POST.value)
                    .order_by(-BasketArticleList.updated_at).paginate(page, 10))

    for post in article_list:
        post.category = category_info

    # get page number
    page_num = math.ceil(len(BasketArticleList.filter(
        BasketArticleList.category == category_info.category_id,
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
        'category': category_info,
        'tags': tags,
        'popular_post': popular_articles,
    }
