from django.urls import path
from .views import SignUpView, CustomLoginView
from django.contrib.auth.views import LogoutView
from . import views

urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),

    path('login/', CustomLoginView.as_view(), name='login'),

    path('logout/', LogoutView.as_view(next_page='Home'), name='logout'),

    path('profile/', views.profile_view, name='profile'),

    path('dashboard/', views.dashboard_view, name='dashboard'),

    path('admin/pending-sellers/', views.pending_sellers_view, name='pending_sellers'),
    path('admin/approve-seller/<int:user_id>/', views.approve_seller, name='approve_seller'),
    path('admin/users/', views.manage_users_view, name='manage_users'),
    path('admin/users/upgrade/<int:user_id>/', views.upgrade_to_seller, name='upgrade_to_seller'),
    path('admin/users/delete/<int:user_id>/', views.delete_user, name='delete_user'),







    
]
