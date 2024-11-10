from django.urls import path
from . import views
from .scripts.mainapppage import MainPageView,bookingpageview,export_data


urlpatterns = [
    path("",views.website_page, name='website_page'),
    path('index/', MainPageView.as_view(), name='index'),
    path('register/', views.register, name='register'),
    path('bookingpageview/', bookingpageview.as_view(), name='bookingpageview'),
    path('login_view/', views.login_view, name='login_view'),
    path('destroyevent/<int:module_id>',views.destroyevent,name="destroyevent"),
    path('add_amount/', views.add_amount, name='add_amount'),
    path('logout/', views.logout_view, name='logout'),
    path('download_report/',export_data.as_view(),name='download_report')
    # path("",views.home, name='home')
   

]
