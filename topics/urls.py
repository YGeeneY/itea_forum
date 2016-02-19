from django.conf.urls import url

from .views import MessageListView, AddView, IndexView, MessageAddView

urlpatterns = [
    url(r"^$", IndexView.as_view(), name='index'),
    url(r"^add/$", AddView.as_view(), name='add'),
    url(r"^(?P<pk>[0-9]+)/$", MessageListView.as_view(), name='topic'),
    url(r"^create/(?P<pk>[0-9]+)$", MessageAddView.as_view(), name='m_add',),

]



