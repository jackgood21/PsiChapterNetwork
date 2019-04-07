from django.urls import path
from . import views
from django.contrib.auth.views import LoginView, LogoutView
from django.conf import settings
from django.conf.urls.static import static
from .views import UserListView, UserDetailView

urlpatterns = [

    path("", views.landing, name= "landing"),
    path("user/<int:pk>/", UserDetailView.as_view(), name= "user-detail"),
    path('home/', UserListView.as_view(), name="sigchi-home"),
    path('about/', views.about, name="sigchi-about"),
    path('contact/', views.contact, name="contact"),
    path('login/', LoginView.as_view(template_name='users/login.html'),name="login"),
    path('logout/', LogoutView.as_view(template_name='users/logout.html'),name="logout"),

]


if settings.DEBUG:
    urlpatterns+= static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
