def serialize_comments(serialized_post, comments):
    if comments:
        serialized_post['comments'] = {}

        for comment in comments:

            serialized_post['comments'].update({
                'comment {}'.format(comment.id): {
                    'author_email': comment.author.email,
                    'author_username': comment.author.username,
                    'content': comment.content
                }
            })

    return serialized_post
