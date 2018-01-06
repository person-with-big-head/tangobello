import math
from bottle import get, redirect

from tangobello.models import BasketArticleList, Authors, Categories, Tags, ShowStatusEnum
from tangobello.serializers import basket_article_list_serializer
from tangobello.utils import template
from tangobello.plugins import boilerplate_plugin


@get('/archive/<year:int>', skip=[boilerplate_plugin])
@template('archive.html')
def category(year):

    # get posts list.
    article_list = (BasketArticleList.select()
                    .join(Authors, on=(Authors.author_id == BasketArticleList.author))
                    .join(Categories, on=(Categories.category_id == BasketArticleList.category))
                    .where(BasketArticleList.updated_at.year == year,
                           BasketArticleList.show_status == ShowStatusEnum.PUBLIC_POST.value)
                    .order_by(-BasketArticleList.updated_at).limit(10))

    # get page number
    page_num = math.ceil(len(BasketArticleList.filter(
        BasketArticleList.updated_at.year == year,
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
        'year': year,
    }


@get('/archive/<year:int>/page/<page:int>', skip=[boilerplate_plugin])
@template('archive.html')
def category(year, page):
    if page == 1:
        redirect('/archive/' + str(year))

    # get posts list.
    article_list = (BasketArticleList.select()
                    .join(Authors, on=(Authors.author_id == BasketArticleList.author))
                    .join(Categories, on=(Categories.category_id == BasketArticleList.category))
                    .where(BasketArticleList.updated_at.year == year,
                           BasketArticleList.show_status == ShowStatusEnum.PUBLIC_POST.value)
                    .order_by(-BasketArticleList.updated_at).paginate(page, 10))

    # get page number
    page_num = math.ceil(len(BasketArticleList.filter(
        BasketArticleList.updated_at.year == year,
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
        'popular_post': popular_articles,
        'year': year
    }
