from django.urls import path
from . import views
from .scripts.mainapppage import MainPageView,bookingpageview


urlpatterns = [
    path('index/', MainPageView.as_view(), name='index'),
    path('register/', views.register, name='register'),
    path('bookingpageview/', bookingpageview.as_view(), name='bookingpageview'),
    path('login_view/', views.login_view, name='login_view'),
    path('destroyevent/<int:module_id>',views.destroyevent,name="destroyevent"),
    path('add_amount/', views.add_amount, name='add_amount'),
    path('logout/', views.logout_view, name='logout'),
    path("",views.home, name='home')
   

]
