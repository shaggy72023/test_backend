from django.forms import ModelForm
from bb_comment.models import Comment


class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['author', 'post', 'content']
