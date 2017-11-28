from bottle import get, redirect

from tangobello.utils import template
from tangobello.plugins import boilerplate_plugin
from tangobello.models import Posts, Authors, Categories
from tangobello.serializers import post_serializer


@get('/', skip=[boilerplate_plugin])
@template('site/posts.html')
def index():
    # get six top posts.
    six_top_posts = (Posts.select().join(Authors, on=(Authors.author_id == Posts.author))
                     .join(Categories, on=(Categories.category_id == Posts.category))
                     .order_by(Posts.post_date).limit(6))
    print(six_top_posts)
    for post in six_top_posts:
        print(post.category.category_name)
    return {'article_list': post_serializer.dump(six_top_posts, many=True).data}


@get('/posts/<page:int>', skip=[boilerplate_plugin])
@template('site/posts.html')
def posts(page):
    # if get the first page of the posts,
    # redirect to the index page.
    if page == 1:
        redirect('/')

    # get six top posts.
    six_top_posts = (Posts.select().join(Authors, on=(Authors.author_id == Posts.author))
                     .join(Categories, on=(Categories.category_id == Posts.category))
                     .order_by(Posts.post_date).limit(6))
    print(six_top_posts)
    for post in six_top_posts:
        print(post.category.category_name)
    return {'article_list': post_serializer.dump(six_top_posts, many=True).data}
