from bb_post.api.exceptions import PostUnknownAPIError
from bb_post.models import Post
from bb_comment.models import Comment


class PostAPIMixin(object):

    post = None
    post_comments = None

    def dispatch(self, *args, **kwargs):

        try:
            self.post = Post.objects.get(id=kwargs['post_id'])
            self.post_comments = Comment.objects.filter(post=self.post)

        except Post.DoesNotExist:
            raise PostUnknownAPIError()

        return super(PostAPIMixin, self).dispatch(*args, **kwargs)
