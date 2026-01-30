from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path
from .views import confirm_logout, user_profile, SignUpView, author_group, common_group

urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('login/', LoginView.as_view(template_name='sign/login.html'), name='login'),
    path('logout/', LogoutView.as_view(template_name='sign/logout.html'), name='logout'),
    path('confirm/logout', confirm_logout, name='confirm_logout'),
    path('/profile/', user_profile, name='user_profile'),
    path('/author_group/', author_group, name='author_group'),
    path('common_group/', common_group, name='common_group'),
]