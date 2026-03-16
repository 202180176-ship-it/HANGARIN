from django.contrib import admin
from django.urls import path, include # <--- Make sure 'path' and 'include' are here
from django.shortcuts import redirect
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', lambda request: redirect('login')),
    path('admin/', admin.site.urls),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('', include('todo.urls')),
]