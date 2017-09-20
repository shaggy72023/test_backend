# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.db import migrations


def add_example_comments(apps, schema_editor):
    user1 = User.objects.create_user(username='testuser1', password='111111', email='example@mail.com')
    user2 = User.objects.create_user(username='testuser2', password='111111', email='example1@mail.com')

    Comment = apps.get_model('bb_comment', 'Comment')
    Comment.objects.bulk_create([
        Comment(author_id=user1.id, post_id=1, content="Test comment for first post"),
        Comment(author_id=user2.id, post_id=1, content="Another test comment for first post"),
        Comment(author_id=user2.id, post_id=2, content="Test comment for second post"),
        Comment(author_id=user1.id, post_id=3, content="Another test comment for second post")
    ])


def revert_example_comments(apps, schema_editor):

    user1 = User.objects.get(username='testuser1')
    user1.delete()
    user2 = User.objects.get(username='testuser2')
    user2.delete()


class Migration(migrations.Migration):

    dependencies = [
        ('bb_comment', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(add_example_comments, reverse_code=revert_example_comments)
    ]
