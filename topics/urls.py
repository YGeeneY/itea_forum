from django.conf.urls import url

from .views import MessageListView, TopAddView, TopicView, MessageAddView

urlpatterns = [
    url(r"^$", TopicView.as_view(), name='topic'),
    url(r"^add/$", TopAddView.as_view(), name='add_topic'),
    url(r"^(?P<pk>[0-9]+)/$", MessageListView.as_view(), name='topic_messages'),
    url(r"^create/(?P<pk>[0-9]+)$", MessageAddView.as_view(), name='add_topic_message',),
]