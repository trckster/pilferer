from requests import get
from post import Post
from peewee import *
from json import loads

# Thx hidemy.name for free proxy. Let it be hardcoded for the time
proxy_ip = '51.158.111.242:8811'

proxies = {
    'http': 'http://{}'.format(proxy_ip),
    'https': 'https://{}'.format(proxy_ip)
}


def publish_post_to_channel_if_needed(token, telegram_channel_id):
    post = get_last_unpublished_post()

    if not post:
        print('Nothing to post')
        return

    print('Posting {}'.format(post.id))

    response = get('https://api.telegram.org/bot{}/sendMessage?chat_id={}&text=testpost{}'.format(
        token,
        telegram_channel_id,
        post.id), proxies=proxies)

    answer = loads(response.text)

    if not answer['ok']:
        print('>>>> Error: {}'.format(response.text))
        return

    Post.update(posted=True).where(Post.id == post.id).execute()


def get_last_unpublished_post():
    try:
        unpublished_post = Post.select().where(Post.posted == 0).order_by(Post.date.asc()).first()
        print(unpublished_post)
    except DoesNotExist:
        return None

    return unpublished_post
