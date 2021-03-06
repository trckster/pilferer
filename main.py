from dotenv import dotenv_values
from vk import get_posts_from_vk
from tg import publish_post_to_channel_if_needed
from post import Post
from os import path
from post import db
from datetime import datetime


def main():
    print()
    print('Starting process at {}'.format(datetime.now()))
    env = dotenv_values()

    posts = get_posts_from_vk(env['VK_TOKEN'], env['VK_GROUP_ID'], env['VK_POSTS_COUNT_LOAD'])
    Post.update_posts(posts)

    publish_post_to_channel_if_needed(env['TG_TOKEN'], env['TG_CHANNEL_ID'], env['WITH_PROXY'])


if __name__ == '__main__':
    if not path.exists('pilferer.db'):
        print('Creating database...')
        db.create_tables([Post])
        print('Created.')

    main()
