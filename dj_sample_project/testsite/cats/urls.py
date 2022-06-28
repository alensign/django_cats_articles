from django.urls import path,re_path
from .views import *

urlpatterns = [
    path('',CatsHome.as_view(), name = 'home'),
    path('about/',about,name='about'),
    path('addpage/',AddPage.as_view(), name = 'add_page'),
    path('contact/',contact,name='contact'),
    path('login/',Login.as_view(),name='login'),
    path('post/<slug:post_slug>',ShowPost.as_view(), name='post'),
    path('category/<slug:cat_slug>',CatsCategory.as_view(), name='category'),
    path('signup/',SignUp.as_view(), name='signup'),
    path('logout/', logout_user, name='logout'),
]