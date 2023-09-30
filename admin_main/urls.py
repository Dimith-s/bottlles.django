from django.urls import path
from .import views

urlpatterns = [
    path('', views.home,name='ahome'),
    path('adminlogout/',views.admin_logout,name='admin_logout'),
    path('userlist',views.userlist,name='userlist'),
    path('sizelist/',views.sizelist,name='sizelist'),
    path('addsize/', views.addsize, name='addsize'),
    path('productlist',views.productlist,name='productlist'),
    path('categorylist',views.categorylist,name = 'categorylist'),
    path('addproduct/',views.addproduct,name= 'addproduct'),
    path('editproduct/<int:product_id>/',views.addproduct,name= 'editproduct'),
    path('deleteproduct/<int:product_id>/',views.deleteproduct,name= 'deleteproduct'),
    path('user-block/<int:user_id>', views.user_block, name='user_block'),
    path('category-block/<int:category_id>', views.category_block, name='category_block'),
    path('product-block/<int:product_id>',views.product_block,name='product_block'),
    path('addcategory/',views.addcategory,name='addcategory'),
    path('editcategory/<int:category_id>/',views.addcategory,name='editcategory'),
    path('deletecategory/<int:category_id>/',views.deletecategory,name='deletecategory'),
    path('orderlist/',views.orderlist,name='orderlist'),
    path('order_details/<int:id>/',views.order_details,name='order_details'),
    path('edit_order/<int:id>/',views.edit_order,name="edit_order"),
    path('coupon_management/',views.coupon_management,name='coupon_management'),
    path('addcoupon/', views.addcoupon, name='addcoupon'),
    path('salesreport/', views.sales_report, name='sales_report'),
     path('yearly-sales/', views.yearly_sales, name='yearly_sales'),
    path('monthly-sales/', views.monthly_sales, name='monthly_sales'),
    path('accept_return/<int:id>/', views.accept_return_request, name='accept_return_request'),

    
   
]