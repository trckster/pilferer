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


def publish_post_to_channel_if_needed(token, telegram_channel_id, with_proxy):
    post = get_last_unpublished_post()

    if not post:
        print('Nothing to post')
        return

    print('Posting {}'.format(post.id))

    query = construct_query(post, token, telegram_channel_id)

    if not query:
        print('Post {} failed'.format(post.id))
        Post.update(posted=True).where(Post.id == post.id).execute()
        return

    if with_proxy:
        response = get(query, proxies=proxies)
    else:
        response = get(query)

    answer = loads(response.text)

    if not answer['ok']:
        print('>>>> Error: {}'.format(response.text))
        return

    Post.update(posted=True).where(Post.id == post.id).execute()


def construct_query(post, token, telegram_channel_id):
    domain = 'https://api.telegram.org/'
    bot_secret = 'bot{}'.format(token)

    question = post.text if len(post.text) else 'Что бы вы выбрали?'

    poll = loads(post.poll)

    if len(question) > 255:
        return None
    answers = []
    for answer in poll['answers']:
        if len(answer['text']) > 100:
            return None
        answers.append(answer['text'])

    options = dumps(answers)

    query = f'{domain}{bot_secret}/sendPoll?chat_id={telegram_channel_id}&question={question}&options={options}'

    return query


def get_last_unpublished_post():
    try:
        unpublished_post = Post.select().where(Post.posted == 0).order_by(Post.date.asc()).first()
        print(unpublished_post)
    except DoesNotExist:
        return None

    return unpublished_post
