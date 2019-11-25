import requests
from dotenv import load_dotenv
from os import getenv

load_dotenv()

token = getenv('VK_TOKEN')
owner_id = getenv('GROUP_ID')

url = f'https://api.vk.com/method/wall.get?access_token={token}&owner_id=-{owner_id}&v=5.103'

res = requests.get(url)
print(res.text)
