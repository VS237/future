from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('service/', views.service, name='service'),
    path('feature/', views.feature, name='feature'),
    path('testimonial/', views.testimonial, name='testimonial'),
    path('quote/', views.quote, name='quote'),
    path('contact/', views.contact, name='contact'),
    path('register/', views.register_user, name='register'),
    path("login/", views.login_user, name="login"),
    path("logout/", views.logout_user, name="logout"),

    path('management/dashboard/', views.admin_dashboard, name='dashboard'),
    path('contact-us/', views.contact_view, name='contact'), 
    path('management/message/delete/<int:message_id>/', views.delete_message, name='delete_message'),
]
