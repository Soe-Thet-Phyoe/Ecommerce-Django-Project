"""
URL configuration for first_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.1/topics/http/urls/
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
from django.contrib import admin
from django.urls import path, include, re_path
from views  import page_views
from views import category_views, product_views #Another Way
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path("",  page_views.index, name="index"),
    path("shop/",  page_views.shop, name="shop"),
    
    # Category
    path("category/", category_views.category_list, name="cl"),
    path("category_create/", category_views.category_create, name="cc"),
    path("category_update/<int:user_id>", category_views.category_update, name="cu"),
    path("category_delete/<int:user_id>/", category_views.category_delete, name="cd"),

    # Product
    path("product_list/",  product_views.product_list, name="pl"),
    path("product_create/",  product_views.product_create, name="pc"),
    path("product_update/<int:user_id>",  product_views.product_update, name="pu"),
    path("product_delete/<int:user_id>",  product_views.product_delete, name="pd"),

    # Register?login
    path("register/",  page_views.user_register, name="ur"),
    path("otp/",  page_views.verify_otp, name="otp"),
    path("login/",  page_views.user_login, name="ul"),
    path("logout/",  page_views.user_logout, name="logout"),

    #cart
    path("cart/",  page_views.cart_list, name="cart"),
    path("add_to_cart/<int:pk>",  page_views.add_to_cart, name="add_to_cart"),
    path("remove_from_cart/<int:pk>",  page_views.remove_from_cart, name="remove_from_cart"),

    #Page_not_found
    re_path(r"^.*/$", page_views.page_not_found),
    

    path('',include('pwa.urls'))

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + static(settings.STATIC_URL, document_root = settings.STATIC_ROOT)
