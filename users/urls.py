from django.urls import path
from . import views
from .views import *

urlpatterns = [
    # path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('register/', views.register_view, name='register'),
    path('verify-otp/', views.verify_otp_view, name='verify_otp'),
    path("ai-chat/", views.ai_chat, name="ai_chat"),
    path("login/", login_view, name="login"),
    path("dashboard/", dashboard, name="dashboard"),
    path("manage-users/", manage_users, name="manage_users"),
    path("suspend-user/<int:user_id>/", views.suspend_user, name="suspend_user"),
    path("activate-user/<int:user_id>/", views.activate_user, name="activate_user"),
    path("delete-user/<int:user_id>/", views.delete_user, name="delete_user"),
    path("change-role/<int:user_id>/", views.change_role, name="change_role")
]
