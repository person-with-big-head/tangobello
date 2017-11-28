# import json
# from bottle import get
#
# from tangobello.utils import template
# from tangobello.plugins import boilerplate_plugin
# from tangobello.hbase import connect
#
#
# def get_news(row_prefix, limit):
#     table = connect.table('dev_basket_news_list')
#     data = table.scan(row_prefix=row_prefix, limit=limit)
#     items = []
#     for k, v in data:
#         item = {}
#         for binary_key, binary_value in v.items():
#             item[binary_key.decode()] = binary_value.decode()
#         item['row_key'] = k.decode()
#         item['info:content_img_list'] = json.loads(item['info:content_img_list'])
#         items.append(item)
#     return items
#
#
# @get('/', skip=[boilerplate_plugin])
# @template('site/posts.html')
# def index():
#     # 轮播图, 5篇
#     carousels = get_news(b'98', 5)
#
#     # 今日话题, 6篇新闻
#     today_topics = get_news(b'99', 6)
#
#     # 军情
#     special_military = get_news(b'20', 8)
#
#     return {"carousels": carousels, "today_topics": today_topics,
#             "special_military": special_military}
