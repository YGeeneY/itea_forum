from django.conf.urls import url

from .views import logout_view
from .views import RegisterView
from .views import LoginView
from .views import AccountView
from .views import InboxView
from .views import InboxDetailView
from .views import SelfAccountView
from .views import PrivateMessageView

urlpatterns = [
    url(r"^$", SelfAccountView.as_view(), name='self_account'),
    url(r"^logout/$", logout_view, name='logout'),
    url(r"^login/$", LoginView.as_view(), name='login'),
    url(r"^register/$", RegisterView.as_view(), name='register'),
    url(r"^inbox/$", InboxView.as_view(template_name='landing/inbox.html'), name='inbox'),
    url(r"^inbox/(?P<pk>\d+)$", InboxDetailView.as_view(), name='inbox_detail'),
    url(r"^(?P<username>\w+)/send_message/$", PrivateMessageView.as_view(), name='send_mail'),
    url(r"^(?P<username>\w+)/$", AccountView.as_view(), name='account'),
]