from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
app_name = 'blog'
urlpatterns = [
    # post views
    path('', views.post_list, name='post_list'),
    #path('', views.PostListViev.as_view(), name='post_list'),
    path('<int:year>/<int:month>/<int:day>/<slug:post>/', views.post_detail, name='post_detail'),
    path('tag/<slug:tag_slug>/',views.post_list, name='post_list_by_tag'),
    #path('login/', views.user_login, name='login'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('post-add/', views.post_add, name='post_add'),
    path('post-edit/<int:post_id>/',views.post_edit, name='post_edit'),
    path('post-delete/<int:post_id>/',views.post_delete, name='post_delete'),
    path('post_point_list/<int:post_id>/',views.post_point_list,name='post_point_list'),
    path('post_point_add/<int:post_id>/', views.post_point_add, name='post_point_add'),
    path('post_point_edit/<int:post_point_id>/',views.post_point_edit, name='post_point_edit'),
    path('post_point_delete/<int:post_point_id>/',views.post_point_delete, name='post_point_delete'),
    path('sign-up/', views.sign_up, name='sign-up'),
]