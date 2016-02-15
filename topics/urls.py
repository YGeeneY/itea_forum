from django.conf.urls import url

from .views import add, index, detail
from .auth_view import logout_view, login_view, RegisterView

urlpatterns = [
    url(r"^index/$", index, name='index'),
    url(r"^add/$", add, name='add'),
    url(r"^(?P<id>[0-9]+)/$", detail),
    url(r"^logout/$", logout_view, name='logout'),
    url(r"^login/$", login_view, name='login'),
    url(r"^register/$", RegisterView.as_view(), name='register'),
]