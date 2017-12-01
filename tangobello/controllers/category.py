from bottle import get

from tangobello.models import Posts, Authors, Categories
from tangobello.serializers import post_serializer
from tangobello.utils import template
from tangobello.plugins import boilerplate_plugin


@get('/category/<category_name>', skip=[boilerplate_plugin])
@template('site/category.html')
def category(category_name):

    # get category information
    category_info = (Categories.get(Categories.category_name == category_name))

    # get posts list.
    article_list = (Posts.select().join(Authors, on=(Authors.author_id == Posts.author))
                    .where(Posts.category == category_info.category_id).order_by(Posts.post_date).limit(10))

    for post in article_list:
        post.category = category_info

    # get page number
    page_num = int(len(Posts.select(Posts.post_id)) / 10)
    #
    return {
        'article_list': post_serializer.dump(article_list, many=True).data,
        'current_page': 1,
        'max_page': page_num,
        'category': category_info
    }
