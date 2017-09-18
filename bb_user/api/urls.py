from django.conf.urls import patterns, url

from .views import user


urlpatterns = patterns('',
    url(r'^$', user.User.as_view()),
    url(r'^/(?P<user_id>\d+)$', user.User.as_view()),
    url(r'^/login$', user.LoginUser.as_view())
)
