"""
URL configuration for SimpleBudget project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from django.urls import path
from accounts import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', views.AuthViews.login_view, name='login'),
    path('signup/', views.AuthViews.signup_view, name='signup'),
    path('recovery/', views.AuthViews.recovery_view, name='recovery'),
    path('reset/<str:username>/', views.AuthViews.reset_view, name='reset'),
    path('', views.HomeView.as_view(), name='home'),
    path('logout/', views.AuthViews.logout_view, name='logout'),
    path('expenses/', views.ExpenseView.as_view(), name='expenses'),
    path('budget/', views.BudgetView.as_view(), name='budget'),
    path('new/', views.OldHomeView.as_view(), name='old')
]
