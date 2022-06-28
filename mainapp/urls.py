from django.urls import path
from django.contrib.auth.views import PasswordChangeView,PasswordChangeDoneView
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('search/', views.search, name='search'),
    path('post/<slug:slug>/', views.post, name='post-details'),
    path('post-create/', views.post_create, name='post-create'),
    path('post-update/<slug:slug>/', views.post_update, name='post-update'),
    path('post-delete/<slug:slug>/', views.post_delete, name='post-delete'),
    path('setting/change_password/',PasswordChangeView.as_view(template_name='password_change.html'), name='change_password'),
    path('setting/password_change_done/', PasswordChangeDoneView.as_view(template_name='password_change_done.html'),name='password_change_done'),
    path('setting/<str:username>/', views.setting, name='setting'),
    
    
]