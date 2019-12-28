from sqlite_orm.field import IntegerField, BooleanField, TextField
from sqlite_orm.table import BaseTable


class Post(BaseTable):
    __table_name__ = 'posts'

    id = IntegerField(primary_key=True, auto_increment=True)
    name = TextField(not_null=True)
    active = BooleanField(not_null=True, default_value=1)

    @staticmethod
    def update_posts(posts):
        print(posts.status_code)
        pass
