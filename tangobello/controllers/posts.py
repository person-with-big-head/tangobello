from bottle import get, redirect, abort

from tangobello.utils import template
from tangobello.plugins import boilerplate_plugin
from tangobello.models import BasketArticleList, PoolArticle, Authors, Categories
from tangobello.serializers import post_serializer


@get('/', skip=[boilerplate_plugin])
@template('posts.html')
def index():
    # get six top posts.
    six_top_posts = (BasketArticleList.select().join(Authors, on=(Authors.author_id == BasketArticleList.author))
                     .join(Categories, on=(Categories.category_id == BasketArticleList.category))
                     .where(BasketArticleList.is_top == 1).order_by(BasketArticleList.post_date).limit(6))

    # get posts list.
    article_list = (BasketArticleList.select().join(Authors, on=(Authors.author_id == BasketArticleList.author))
                    .join(Categories, on=(Categories.category_id == BasketArticleList.category))
                    .order_by(BasketArticleList.post_date).limit(10))

    # get page number
    page_num = int(len(BasketArticleList.select(BasketArticleList.post_id)) / 10)

    return {
        'article_list': post_serializer.dump(article_list, many=True).data,
        'six_top_posts': post_serializer.dump(six_top_posts, many=True).data,
        'current_page': 1,
        'max_page': page_num
    }


@get('/posts/page/<page:int>', skip=[boilerplate_plugin])
@template('posts.html')
def posts(page):
    # if get the first page of the posts,
    # redirect to the index page.
    if page == 1:
        redirect('/')

    # get six top posts.
    six_top_posts = (BasketArticleList.select().join(Authors, on=(Authors.author_id == BasketArticleList.author))
                     .join(Categories, on=(Categories.category_id == BasketArticleList.category))
                     .where(BasketArticleList.is_top == 1).order_by(BasketArticleList.post_date).limit(6))

    # get current page posts.
    article_list = (BasketArticleList.select().join(Authors, on=(Authors.author_id == BasketArticleList.author))
                    .join(Categories, on=(Categories.category_id == BasketArticleList.category))
                    .order_by(BasketArticleList.post_date).paginate(page, 10))

    # get page number
    page_num = int(len(BasketArticleList.select(BasketArticleList.post_id)) / 10)

    return {
        'article_list': post_serializer.dump(article_list, many=True).data,
        'six_top_posts': post_serializer.dump(six_top_posts, many=True).data,
        'current_page': page,
        'max_page': page_num
    }


@get('/post/<post_id:int>', skip=[boilerplate_plugin])
@template('post.html')
def post(post_id):
    # get the post by id from db.
    post_ = (PoolArticle.select().join(Authors, on=(Authors.author_id == PoolArticle.author))
             .join(Categories, on=(Categories.category_id == PoolArticle.category))
             .where(PoolArticle.post_id == post_id))

    if not post_:
        abort(404, 'Page Not Found')
    return {
        'post': post_serializer.dump(post_[0]).data
    }
