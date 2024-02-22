from django.urls import path
from .views import save_trespassing_info , user_login, signup, user_logout, dashboard

        
urlpatterns = [
    path('api/save-trespassing-info/', save_trespassing_info, name='save_trespassing_info'),
     path('signup/', signup, name='signup'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
    path('dashboard/',dashboard, name='dashboard'),

]
# in myapp/urls.py

