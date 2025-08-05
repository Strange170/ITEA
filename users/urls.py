from django.urls import path
from .views import SignUpView
from django.contrib.auth.views import LoginView, LogoutView
from . import views


urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    
    path('login/', LoginView.as_view(
        template_name='users/login.html',
        redirect_authenticated_user=True
    ), name='login'),
    
    path('logout/', LogoutView.as_view(next_page='Home'), name='logout'),
    path('admin/pending-sellers/', views.pending_sellers_view, name='pending_sellers'),
    path('admin/approve-seller/<int:user_id>/', views.approve_seller, name='approve_seller'),
    path('admin/users/', views.manage_users_view, name='manage_users'),
    path('admin/users/upgrade/<int:user_id>/', views.upgrade_to_seller, name='upgrade_to_seller'),
    path('admin/users/delete/<int:user_id>/', views.delete_user, name='delete_user'),

]
