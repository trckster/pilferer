from peewee import *
from json import dumps

db = SqliteDatabase('pilferer.db')


class Post(Model):
    id = IntegerField()
    date = DateTimeField()
    text = TextField()
    posted = BooleanField()
    # I know, that sucks, but I will store poll as json
    poll = TextField()

    class Meta:
        database = db
        table_name = 'posts'

    @staticmethod
    def update_posts(posts):
        for post in posts:
            if post['marked_as_ads']:
                print('Post {} is ad, skipping'.format(post['id']))
                continue

            if not len(post['attachments']):
                print('Post {} has no attachments, skipping'.format(post['id']))
                continue

            if post['attachments'][0]['type'] != 'poll':
                print('Post {} contains no poll, skipping'.format(post['id']))
                continue

            if Post.exists(post['id']):
                print('Post {} already exists, skipping'.format(post['id']))
                continue

            Post.create(
                id=post['id'],
                date=post['date'],
                text=post['text'],
                poll=dumps(post['attachments'][0]['poll']),
                posted=False
            )

    @staticmethod
    def exists(post_id):
        posts = Post.select().where(Post.id == post_id)

        return bool(posts)
