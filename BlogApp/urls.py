from django.urls import path
from . import views

urlpatterns = [
    path('',views.Home,name="home"),
    path('login',views.Login,name="login"),
    path('register',views.Register,name="register"),
    path('logout',views.Logout,name="logout"),
    path('create_vomit',views.Create_vomit,name="create_vomit"),
    path('search', views.Search, name='search'),
    path('send_friend_request/<str:to_user_username>', views.Send_friend_request, name='send_friend_request'),
]