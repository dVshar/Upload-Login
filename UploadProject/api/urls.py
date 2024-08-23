
from django.urls import path
from .views import *

urlpatterns = [
    path('check/login',AuthAPI.as_view({'get':'get_user_is_login'})),
    path('login',AuthAPI.as_view({'post':'login_user'})),

    path('users',User_Management.as_view({'get':'get_all_users','post':'add_new_user','delete':'delete_user'}))

]