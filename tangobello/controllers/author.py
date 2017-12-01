from bottle import get

from tangobello.models import Posts, Authors, Categories
from tangobello.serializers import post_serializer
from tangobello.utils import template
from tangobello.plugins import boilerplate_plugin


@get('/author/<author_name>', skip=[boilerplate_plugin])
@template('site/author.html')
def author(author_name):

    # get author information
    author_info = (Authors.get(Authors.author_name == author_name))

    # get posts list.
    article_list = (Posts.select().join(Categories, on=(Categories.category_id == Posts.category))
                    .where(Posts.author == author_info.author_id).order_by(Posts.post_date).limit(10))

    for post in article_list:
        post.author = author_info

    # get page number
    page_num = int(len(Posts.select(Posts.post_id)) / 10)

    return {
        'article_list': post_serializer.dump(article_list, many=True).data,
        'current_page': 1,
        'max_page': page_num,
        'author': author_info
    }
