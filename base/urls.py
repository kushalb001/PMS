from django.contrib import admin
from django.urls import path
from . import views
from django.urls.conf import include
from django.conf.urls.static import static 
from django.conf import settings 


urlpatterns = [
    path('',views.projectname,name='projectname'),
    path('login/',views.loginPage,name='login'),
    path('layout/',views.layout,name='layout'),
    path('home/',views.home,name='home'),
    path("billing/<str:ck>",views.billing,name='billing'),
    path('add-to-cart/<str:pk>/<str:ck>/', views.add_to_cart, name='add-to-cart'),
    path('cart/<str:ck>/',views.order_summary,name='cart'),
    path('remove-from-cart/<str:pk>/<str:ck>',views.remove_from_cart,name='remove-from-cart'),
    path("remove_single_item_from_cart/<str:pk>/<str:ck>",views.remove_single_item_from_cart, name="remove_single_item_from_cart"),
    path('checkout/<str:ck>/<int:ali>',views.checkout,name='checkout'),
    path('checkout2/<str:ck>',views.c_form,name='checkout2'),
    path('bill/<str:ck>',views.bill,name='bill'),
    path('register/',views.register,name='register'),
    path("billing/",views.billing1,name='billing1'),
    path("myorders/",views.myorders,name='myorders'),
    path("display_bill/<int:id>",views.display_bill,name='display_bill'),
    path('customer_orders/',views.customer_order,name='customer_orders'),
    path('orderdetail/<int:id>',views.orderdetails,name='orderdetail'),
    path('covid_data/',views.covid_data,name='covid_data'),
    path('logout/',views.logoutUser,name='logout')

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)