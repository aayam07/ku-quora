from django.urls import path
from . import views


urlpatterns = [
    path('',views.signup_view,name='signup'),
    path('signin/',views.signin_view,name='signin'),
    path('logout/',views.logout_view,name='logout'),
    path('profile/<int:user_id>',views.profile_view,name='profile'),
    path('followings/',views.followings_view,name='followings'),
    path('followings_list/',views.followings_list_view,name='followings_list'),
    path('verify/<token>',views.verify_account_view,name='verify_account')

] 
