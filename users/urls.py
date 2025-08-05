from django.urls import path
from .views import SignUpView
from django.contrib.auth.views import LoginView, LogoutView

urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    
    path('login/', LoginView.as_view(
        template_name='users/login.html',
        redirect_authenticated_user=True
    ), name='login'),
    
    path('logout/', LogoutView.as_view(next_page='Home'), name='logout'),
]
