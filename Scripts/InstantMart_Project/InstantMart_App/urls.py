from django.urls import path
from .import views as v

urlpatterns = [
    path('',v.home,name='home'),
    path('signup',v.sign_up),
    path('signin',v.sign_in),
    path('signout',v.sign_out),
    path('search',v.search_product,name='search'),
    path('category',v.category),
    path('category/<str:category_name>/',v.category_page,name='category_page'),
    path('sidebar',v.sidebar),
    path('filter/<int:pid>',v.filter_cate),
    path('addtocart/<int:pid>',v.add_to_cart,name='add_to_cart'),

    path('cart',v.cart_item),
    path('payment_success/', v.payment_success, name='payment_success'),
    path('payment_cancel/', v.payment_cancel, name='payment_cancel'),
    path('success',v.success,name='success'),
    path('de_cart_item/<int:pid>',v.decrease_cart_item,name='de_cart_item'),
    path('in_cart_item/<int:pid>',v.increase_cart_item,name='in_cart_item'),
    path('delete/<int:Cid>', v.delete_cart_item, name='delete_cart_item'),
    path('account', v.account,name='account'),
    path('delete_address/<int:address_id>/', v.delete_address, name='delete_address'),
]