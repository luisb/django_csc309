from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import logout as auth_logout
from django.views import View
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required
import json
from django.contrib.auth.models import User

from .forms import RegisterForm, LoginForm, UpdateUserForm

# Create your views here.

class RegisterView(View):
    form_class = RegisterForm
    initial = {'key': 'value'}
    template_name = 'accounts/register.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('/')
        return super(RegisterView, self).dispatch(request, *args, **kwargs)
    
    def get(self, request, *args, **kwargs):
        form = self.form_class(initial=self.initial)
        return render(request, self.template_name, {'form': form})
    
    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)

        if form.is_valid():
            form.save()

            return redirect('login')
        
        return render(request, self.template_name, {'form': form})

class CustomLoginView(LoginView):
    form_class = LoginForm
    template_name = 'accounts/login.html'
    form = LoginForm()

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('/')
        return render(request, self.template_name, {'form': self.form})
        
def logout(request):
    auth_logout(request)
    messages.success(request, 'You have been logged out')
    return redirect('login')

@login_required
def profile_view(request):
    user = request.user
    queryset = User.objects.filter(id=user.id).values('id', 'username', 'email', 'first_name', 'last_name')
    s_qs = str(json.dumps(list(queryset))).lstrip('[').rstrip(']')
    return render(request, 'accounts/profile.html', {'data': s_qs})

@login_required
def profile_edit(request):
    if request.method == 'POST':
        user_form = UpdateUserForm(request.POST, instance=request.user)

        if user_form.is_valid():
            user_form.save()
            messages.success(request, 'Your profile is updated successfully')
            return redirect(to='profile-view')
    else:
        user_form = UpdateUserForm(instance=request.user)
    return render(request, 'accounts/profile_edit.html', {'user_form': user_form})
