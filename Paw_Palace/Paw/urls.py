"""
URL configuration for Paw_Palace project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import path
from .import views

urlpatterns = [
    path('',views.index),
    path('shopregister',views.shopregister),
    path('userreg',views.userreg),
    path('about',views.about),
    path('shopabout',views.shopabout),
    path('userabout',views.userabout),
    path('log', views.log, name='log'),
    path('user', views.userhome, name='userhome'),
    path('shop',views.shophome),
    path('admin',views.adminhome),
    path('userlogout',views.userlogout),
    path('adminlogout',views.adminlogout),
    path('shoplogout',views.shoplogout),
    path('addnotification',views.addnotfication),
    path('userdetails',views.userdetails),
    path('petshopdetails',views.petshopdetails),
    path('unsuspense/<id>',views.unsuspense),
    path('suspense/<id>',views.suspense),
    path('gallery',views.gallery),
    path('shopgallery',views.shopgallery),
    path('admingallery',views.admingallery),
    path('markasseen/<id>',views.markasseen),
    path('markallseen/',views.markallseen),
    path('addphotos',views.addphotos),
    path('photoreq',views.photoreq),
    path('acceptphoto/<id>',views.acceptphoto),
    path('deletephoto/<id>',views.deletePhoto),
    path('addreviews',views.addreviews),
    path('editprofile',views.editprofile),
    path('editshopprofile',views.editshopprofile),
    path('updateuspf',views.updateuspf),
    path('updatesppf',views.updatesppf),
    path('shopping',views.shopping),
    path('shopdetail/<id>',views.shopdetail),
    path('book-service',views.book_service),
    path('addproducts',views.addproducts),
    path('shopproducts',views.shopproducts),
    path('all-products',views.all_products),
    path('all-services',views.all_services),
    path('editproduct/<id>',views.editproducts),
    path('updateproduct/<id>',views.updateproduct),
    path('deleteprod/<id>',views.deleteprod),
    path('addservices',views.addservices),
    path('addtocart/<id>',views.addtocart),
    path('cart',views.cart),
    path('cart/increment/<int:id>/', views.increment_quantity, name='increment_quantity'),
    path('cart/decrement/<int:id>/', views.decrement_quantity, name='decrement_quantity'),
    path('dltcartitm/<id>',views.dltcartitm),
    path('placeorder',views.placeorder),
    path('success',views.success),
    path('userorders',views.userorders),
    path('shoporders/<id>',views.shoporders,name='product_orders'),
    path('shopallorders',views.shopallorders,name='shop_all_orders'),
    path('update-order-status/<int:booking_id>/',views.update_order_status,name='update_order_status'),
    path('review',views.review),
    path('allorders',views.allorders),
    path('services',views.services),
    path('shopservices',views.shopservices),
    path('editserv/<id>',views.editserv),
    path('updateserv/<id>',views.updateserv),
    path('singleplaceorder/<id>',views.singleplaceorder),
    path('singlesuccess/<id>',views.singlesuccess),
    path('confirm-single-order',views.confirm_single_order),
    path('bookservice/<id>',views.bookservice),
    path('get-booked-slots/<id>',views.get_booked_slots),
    path('deleteserv/<id>',views.deleteserv),


]
