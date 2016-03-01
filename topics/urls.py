from django.conf.urls import url
from django.contrib.auth.decorators import login_required

from .views import MessageListView, TopAddView, TopicView, MessageAddView

urlpatterns = [
    url(r"^$", TopicView.as_view(), name='topic'),
    url(r"^add/$", login_required(TopAddView.as_view()), name='add_topic'),
    url(r"^(?P<pk>[0-9]+)/$", MessageListView.as_view(), name='topic_messages'),
    url(r"^create/(?P<pk>[0-9]+)$", login_required(MessageAddView.as_view()), name='add_topic_message',),
]