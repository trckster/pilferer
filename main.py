from dotenv import dotenv_values
from vk import get_posts_from_vk
from tg import publish_post_to_channel_if_needed
from post import Post
from sqlite_orm.database import Database
from os import path


def main():
    env = dotenv_values()

    posts = get_posts_from_vk(env['VK_TOKEN'], env['VK_GROUP_ID'])
    Post.update_posts(posts)

    result = publish_post_to_channel_if_needed(env['TG_TOKEN'], env['TG_CHANNEL_ID'])
    print(result)


if __name__ == '__main__':
    if not path.exists('pilferer.db'):
        print('Creating database...')
        with Database('pilferer.db') as database:
            database.query(Post).create().execute()
            print('Database created in root of the project')

    main()
