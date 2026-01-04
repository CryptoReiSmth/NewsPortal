from django.urls import path
from .views import PostList, PostDetail, PostSearch

urlpatterns = [
    path('', PostList.as_view(), name='post_list'),
    path('<int:pk>', PostDetail.as_view(), name='post_detail'),
    path('search/', PostSearch.as_view(), name='postsearch'),
]
