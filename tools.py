import os
import re
import argparse
from markdown2 import Markdown
from tangobello.models import Post, Tag
from tangobello import db
from tangobello.app import load_config


DIR_NAME = 'posts'


def convert(filename):
    dest_filename = "".join([filename.split(".")[0], ".html"])
    post_path = os.path.join(os.getcwd(), DIR_NAME, filename)

    with open(post_path) as md_file:
        content = md_file.read()
        markdowner = Markdown()
        convert_content = markdowner.convert(content)
        dest_path = os.path.join(os.getcwd(), DIR_NAME, dest_filename)
        f = open(dest_path, "w+")
        f.write(convert_content)

    return dest_filename


def clean(dest_filename):
    post_path = os.path.join(os.getcwd(), DIR_NAME, dest_filename)
    if os.path.exists(post_path):
        os.remove(post_path)


def get_shortcut(body):
    all_p = re.findall("<blockquote>(.*?)</blockquote>", body, re.DOTALL)
    if all_p:
        return all_p[0].strip(" ").replace("\n", "").replace("<p>", "").replace("</p>", "")


def post(filename, dest_filename, author, is_show, tag):
    post_path = os.path.join(os.getcwd(), DIR_NAME, filename)
    dest_path = os.path.join(os.getcwd(), DIR_NAME, dest_filename)
    with open(post_path) as md_file, open(dest_path) as html_file:
        title = md_file.readline()
        html_file.readline()
        body = html_file.read()

        assert title is not None and title != ""
        title = title.replace("#", "").replace("\n", "").strip(" ")

        shortcut = get_shortcut(body)
        assert shortcut is not None

        tag_exists = Tag.select(Tag.name == tag)
        if not tag_exists:
            return

        already_exists = Post.select().where(Post.title == title)
        if already_exists:
            Post.update(shortcut=shortcut, body=body, tags=tag).where(Post.title == title).execute()
        else:
            Post.insert(title=title, author=author, shortcut=shortcut, body=body, is_show=is_show, tags=tag).execute()


def execute():
    load_config()
    db.init()

    parser = argparse.ArgumentParser(description="Upload post file to the blog site.")

    parser.add_argument('-C', '--convert', help="Convert markdown file to html file.",
                        action="store_true")

    parser.add_argument("filename", help="The filename to be uploaded.", type=str)
    parser.add_argument('-a', "--author", help="The author of the post.",
                        type=str, dest="author")
    parser.add_argument('-s', "--show", help="Weather the post should be displayed.",
                        type=int, dest="is_show")
    parser.add_argument('-c', '--clean', help="Weather clean th directory.",
                        action="store_true")
    parser.add_argument('-t', '--tag', help="The tag of the post.",
                        type=str, dest="tag")

    args = parser.parse_args()

    if args.convert:
        filename = convert(args.filename)

        if args.clean:
            clean(filename)

        post(args.filename, filename, args.author, args.is_show, args.tag)


if __name__ == '__main__':
    execute()
