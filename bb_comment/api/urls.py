from django.conf.urls import patterns, url

from .views import comment


urlpatterns = patterns('',
    url(r'^$', comment.Comment.as_view()),
)
