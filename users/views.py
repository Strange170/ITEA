from django.urls import reverse_lazy
from django.views import generic
from .forms import CustomUserCreationForm
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import user_passes_test, login_required
from .models import CustomUser
from django.contrib import messages
from django.contrib.auth import get_user_model

class SignUpView(generic.CreateView):
    form_class = CustomUserCreationForm
    template_name = 'users/signup.html'
    success_url = reverse_lazy('login')

def is_admin(user):
    return user.is_authenticated and user.user_type == 'admin'

@user_passes_test(is_admin)
def pending_sellers_view(request):
    pending_users = CustomUser.objects.filter(user_type='pending')
    return render(request, 'users/pending_sellers.html', {'pending_users': pending_users})

@user_passes_test(is_admin)
def approve_seller(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id, user_type='pending')
    user.user_type = 'seller'
    user.save()
    return redirect('pending_sellers')

CustomUser = get_user_model()

@user_passes_test(is_admin)
def manage_users_view(request):
    users = CustomUser.objects.exclude(user_type='admin')

    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        new_type = request.POST.get('user_type')

        if user_id and new_type in ['buyer', 'seller']:
            user = CustomUser.objects.get(id=user_id)
            user.user_type = new_type
            user.save()
            messages.success(request, f"{user.username} updated to {new_type.title()}.")

        return redirect('manage_users')

    return render(request, 'users/manage_users.html', {'users': users})

@user_passes_test(is_admin)
def upgrade_to_seller(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)
    user.user_type = 'seller'
    user.save()
    messages.success(request, f'{user.username} upgraded to Seller.')
    return redirect('manage_users')

@user_passes_test(is_admin)
def delete_user(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)
    user.delete()
    messages.success(request, f'User {user.username} deleted successfully.')
    return redirect('manage_users')