from django.conf.urls import url
from django.contrib.auth.decorators import login_required

from .views import logout_view, RegisterView, LoginView, AccountView, InboxView, InboxDetailView, SelfAccountView, \
    PrivateMessageView

urlpatterns = [
    url(r"^$",
        login_required(SelfAccountView.as_view()),
        name='self_account'),

    url(r"^logout/$",
        logout_view,
        name='logout'),

    url(r"^login/$",
        LoginView.as_view(),
        name='login'),

    url(r"^register/$",
        RegisterView.as_view(),
        name='register'),

    url(r"^inbox/$",
        login_required(InboxView.as_view(template_name='landing/inbox.html')),
        name='inbox'),

    url(r"^inbox/(?P<pk>\d+)$",
        login_required(InboxDetailView.as_view()),
        name='inbox_detail'),

    url(r"^(?P<username>\w+)/send_message/$",
        PrivateMessageView.as_view(),
        name='send_mail'),

    url(r"^(?P<slug>\w+)/$",
        AccountView.as_view(),
        name='account'),
]
