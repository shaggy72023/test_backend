from django.contrib.auth.models import User
from django.db import models

from bb_post.models import Post


class Comment(models.Model):

    author = models.ForeignKey(User)
    post = models.ForeignKey(Post)
    content = models.TextField()

    class Meta(object):
        app_label = 'bb_comment'
        db_table = 'comment'
