from django.urls import path,include
from .views import *
urlpatterns=[
    path('auth/',UserAuthenticationViews.as_view()),
    path('login/',LoginAuthenticationViews.as_view()),

    path('posts/<str:pk>/',PostView.as_view()),
    path('addcomment/<str:pk>/',AddCommentView.as_view()),
    path('getuserpost/',GetMyPostsViews.as_view()),
    path('getpostdata/<str:pk>/',GetpostData.as_view()),

    path('allposts/',GetPostsView.as_view()),
    path('allposts/<str:pk>/',GetPostsView.as_view()),
    path('getdetails/',GetALLDetails.as_view()),

]
