from requests import get
from post import Post
from peewee import *
from json import loads, dumps

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

    make_pre_post_with_text_if_needed(post, token, telegram_channel_id)

    query = construct_query_2(post, token, telegram_channel_id)

    response = get(query, proxies=proxies)

    answer = loads(response.text)

    if not answer['ok']:
        print('>>>> Error: {}'.format(response.text))
        return

    Post.update(posted=True).where(Post.id == post.id).execute()


def make_pre_post_with_text_if_needed(post, token, telegram_channel_id):
    if not len(post.text):
        return

    query = construct_query_1(post, token, telegram_channel_id)

    return get(query, proxies=proxies)


def construct_query_1(post, token, telegram_channel_id):
    domain = 'https://api.telegram.org/'
    bot_secret = 'bot{}'.format(token)

    message = post.text

    query = f'{domain}{bot_secret}/sendMessage?chat_id={telegram_channel_id}&text={message}'

    return query


def construct_query_2(post, token, telegram_channel_id):
    domain = 'https://api.telegram.org/'
    bot_secret = 'bot{}'.format(token)

    question = 'What?'

    options = dumps(['First one', 'Second one'])

    query = f'{domain}{bot_secret}/sendPoll?chat_id={telegram_channel_id}&question={question}&options={options}'

    return query


def get_last_unpublished_post():
    try:
        unpublished_post = Post.select().where(Post.posted == 0).order_by(Post.date.asc()).first()
        print(unpublished_post)
    except DoesNotExist:
        return None

    return unpublished_post
