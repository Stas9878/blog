from django.urls import path
from django.contrib.auth import views as auth_view
from .forms import LoginForm
from .views import *

urlpatterns = [
    path('<int:pk>', personal_profile, name='personal_profile'),
    path('signup/', SignUpView.as_view(), name='signup'),
    path('login/', CustomLoginView.as_view(redirect_authenticated_user=True, 
                                           template_name='registration/login.html'), 
                                           name='login'),
    path('logout/', auth_view.LogoutView.as_view(template_name='registration/logout.html'), name='logout'),
    path('profile/', profile, name='users-profile'),
    path('password_change/', ChangePassword.as_view(), name='password_change'),
    
]