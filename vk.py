import requests


def get_posts_from_vk(token, group_id):
    url = f'https://api.vk.com/method/wall.get?access_token={token}&owner_id=-{group_id}&v=5.103'
    resp = requests.get(url)

    return resp
