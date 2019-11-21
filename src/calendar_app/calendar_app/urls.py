"""calendar_app URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from users import views as user_views

urlpatterns = [
    path('admin/', admin.site.urls),

    path('register/', user_views.register, name='register'),
    path('profile/', user_views.profile_home, name='profile_home'),

    path('profile/previous_month/<month_num>/<year_num>/', user_views.previous_month, name='profile_previous_month_home'),
    path('profile/next_month/<month_num>/<year_num>/', user_views.next_month, name='profile_next_month_home'),

    path('profile/<int:object_id>/delete/', user_views.event_delete_view, name='event_delete'),
    path('logout/', auth_views.LogoutView.as_view(template_name='users/login.html'), name='logout'),

    path('', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
