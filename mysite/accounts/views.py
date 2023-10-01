from django.urls import reverse_lazy
from django.views import generic
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.views import LoginView, PasswordChangeView
from django.contrib.auth.decorators import login_required
from django.contrib.messages.views import SuccessMessageMixin
from .forms import *


class SignUpView(generic.CreateView):
    form_class = SignUpForm
    success_url = reverse_lazy('login')
    initial = None #Принимает {'key': 'value'}
    template_name = 'registration/signup.html'

    def dispatch(self,request,*args, **kwargs):
        # перенаправит на домашнюю страницу, 
        # если пользователь попытается получить доступ 
        # к странице регистрации после авторизации
        if request.user.is_authenticated:
            return redirect(to='/')
        
        return super(SignUpView, self).dispatch(request,*args,**kwargs)
    def get(self, request, *args, **kwargs):
        form = self.form_class(initial=self.initial)
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()

            username = form.cleaned_data.get('username')
            messages.success(request, f'Аккаунт с логином {username} создан')
            return redirect(to='login') # редирект на страницу логина после регистрации
        return render(request, self.template_name, {'form': form})

class CustomLoginView(LoginView):
    form_class = LoginForm

    def form_valid(self, form):
        remember_me = form.cleaned_data['remember_me']

        if not remember_me:
            # Установим время истечения сеанса равным 0 секундам. 
            # Таким образом, он автоматически закроет сеанс после закрытия браузера. 
            # И обновим данные.
            self.request.session.set_expiry(0)
            self.request.session.modified = True
        # В противном случае сеанс браузера будет таким же как время 
        # сеанса cookie "SESSION_COOKIE_AGE", определенное в settings.py
        return super(CustomLoginView, self).form_valid(form)

@login_required
def profile(request):

    if request.method == 'POST':
        user_form = UpdateUserForm(request.POST, instance=request.user)
        profile_form = UpdateProfileForm(request.POST, request.FILES, instance=request.user.profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Ваши данные обновлены')
            return redirect(to='users-profile')
    else:
        user_form = UpdateUserForm(instance=request.user)
        profile_form = UpdateProfileForm(instance=request.user.profile)
    
    return render(request, 'registration/profile.html',context={
        'user_form': user_form,
        'profile_form': profile_form
    })

class ChangePassword(SuccessMessageMixin, PasswordChangeView):
    template_name = 'registration/password_change.html'
    success_message = 'Пароль успешно изменён'
    success_url = reverse_lazy('users-profile')

def personal_profile(request, pk):
    info = Profile.objects.get(user_id=pk)
    user = User.objects.get(id=pk)

    return render(request, 'registration/personal_profile.html',
                  context={'info': info,
                           'user_page': user})