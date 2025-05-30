from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register_view, name='register'),
    path('home/', views.home_view, name='home'),
    path('add_student/', views.add_student_view, name='add_student'),
    path('edit_student/<int:student_id>/', views.edit_student_view, name='edit_student'),
    path('delete_student/<int:student_id>/', views.delete_student_view, name='delete_student')
]
