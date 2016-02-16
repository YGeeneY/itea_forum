from django.conf.urls import url

from .views import detail, AddView, IndexView, MessageAddView
from .auth_view import logout_view, RegisterView, LoginView

urlpatterns = [
    url(r"^index/$", IndexView.as_view(), name='index'),
    url(r"^add/$", AddView.as_view(), name='add'),
    url(r"^(?P<id>[0-9]+)/$", detail),
    url(r"^logout/$", logout_view, name='logout'),
    url(r"^login/$", LoginView.as_view(), name='login'),
    url(r"^register/$", RegisterView.as_view(), name='register'),
    url(r"^create/(?P<pk>[0-9]+)$", MessageAddView.as_view(), name='m_add'),

]