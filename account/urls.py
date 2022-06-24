from django.urls import path
from . import views
from django.contrib.auth import views as a_views
# from .forms import LoginForm
urlpatterns = [
    # path('login/',views.user_login, name='login'),

    path('dashboard/',views.dashboard, name='dashboard'),
    path('register/',views.register, name='register'),
    path('edit/',views.edit, name='edit'),
    path('users/',views.user_list, name='user_list'),
    path('users/follow',views.user_follow, name='user_follow'),
    path('users/<username>',views.user_detail, name='user_detail'),

    #login and logout url
    path('login/',a_views.LoginView.as_view(template_name='account/login.html'), name='login'),
    path('logout/',a_views.LogoutView.as_view(template_name='account/logout.html'), name='logout'),
    path('logout-then-login/',a_views.logout_then_login, name='logout_then_login'),

    # path('login/',a_views.LoginView.as_view(template_name='account/login.html',
    # authentication_form=LoginForm), name='login'),
    
    # path('logout/',a_views.LogoutView.as_view(), name='logout'),


    # change password urls
    path('password-change/', a_views.PasswordChangeView.as_view(template_name='account/change_password.html'), name='change_password'),
    path('password-change/done', a_views.PasswordChangeDoneView.as_view(template_name='account/change_password_done.html'), name='password_change_done'),



    # reset Password urls
    path('password-reset/', a_views.PasswordResetView.as_view(template_name='account/password_reset.html'), name='password_reset'),
    path('password-reset/done/', a_views.PasswordResetDoneView.as_view(template_name='account/password_reset_done.html'), name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/', a_views.PasswordResetConfirmView.as_view(template_name='account/password_reset_confirm.html'), name='password_reset_confirm'),
    path('password-reset/complete/', a_views.PasswordResetCompleteView.as_view(template_name='account/password_reset_complete.html'), name='password_reset_complete'),




]