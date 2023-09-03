from django.urls import path
from .import views

urlpatterns = [
    path('', views.home,name='ahome'),
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
    path('deletecategory/<int:category_id>/',views.deletecategory,name='deletecategory')
    
   
]