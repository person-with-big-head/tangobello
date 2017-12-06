import elasticsearch
from bottle import get

from tangobello.models import PoolArticle, Authors, Categories, BasketArticleList


def execute():
    es = elasticsearch.Elasticsearch('139.224.105.129')

    posts = (PoolArticle.select(PoolArticle, BasketArticleList.article_summary.alias('summary'))
             .join(Authors, on=(Authors.author_id == PoolArticle.author))
             .join(Categories, on=(Categories.category_id == PoolArticle.category))
             .join(BasketArticleList, on=(PoolArticle.post_id == BasketArticleList.post_id)))

    for post in posts.naive():
        print(post.post_id)
        body = {
            "article_title": post.article_title,
            "article_content": post.article_content,
            "article_img_list": post.article_img_list,
            "post_date": (post.post_date).strftime("%Y-%m-%d %H:%M:%S"),
            "author_id": post.author.author_id,
            "author_name": post.author.author_name,
            "author_avatar": post.author.author_avatar,
            "post_comment_count": post.post_comment_count,
            "post_like_count": post.post_like_count,
            "article_summary": post.summary
        }
        es.index(index='pool_articles', doc_type='info', id=post.post_id, body=body)


@get('/test')
def test():
    execute()
    return 'done'
