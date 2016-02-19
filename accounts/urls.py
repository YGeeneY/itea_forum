from django.conf.urls import url


from .views import logout_view, RegisterView, LoginView

urlpatterns = [
    url(r"^logout/$", logout_view, name='logout'),
    url(r"^login/$", LoginView.as_view(), name='login'),
    url(r"^register/$", RegisterView.as_view(), name='register'),
]
