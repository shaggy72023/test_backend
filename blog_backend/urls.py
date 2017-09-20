from django.conf.urls import patterns, include, url


urlpatterns = patterns('',
    url(r'^api/', include(patterns('',
        url(r'^posts', include('bb_post.api.urls')),
        url(r'^users', include('bb_user.api.urls')),
        url(r'^comments', include('bb_comment.api.urls')),

    ))),
)
