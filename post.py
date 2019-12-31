from peewee import *
from json import dumps

db = SqliteDatabase('pilferer.db')


class Post(Model):
    id = IntegerField()
    date = DateTimeField()
    text = TextField()
    # I know, that sucks, but I will store poll as json
    poll = TextField()

    class Meta:
        database = db
        table_name = 'posts'

    @staticmethod
    def update_posts(posts):
        for post in posts:
            if post['marked_as_ads']:
                continue

            if not len(post['attachments']):
                continue

            if post['attachments'][0]['type'] != 'poll':
                continue

            ok = Post(
                id=post['id'],
                date=post['date'],
                text=post['text'],
                poll=dumps(post['attachments'][0]['poll'])
            )
            print('Start saving')
            ok.save()

            exit(0)
