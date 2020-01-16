import requests
from json import loads


def get_posts_from_vk(token, group_id):
    url = f'https://api.vk.com/method/wall.get?access_token={token}&owner_id={group_id}&v=5.103&count=2'
    response = requests.get(url)

    data = loads(response.text)
    posts = data['response']['items']

    return posts
