from django.urls import path
from . import views

urlpatterns = [
    path('',views.store,name='store'),
    path('category/<slug:category_slug>/',views.store,name='products_by_category'),
    path('category/<slug:category_slug>/<slug:product_slug>/',views.product_detail,name='product_detail'),
    path('search/',views.search,name='search'),
    path('invoice/<int:order_item_id>/',views.invoice, name='invoice'),
     path('generateinvoice/<int:orderitem_id>/', views.generateInvoice.as_view(), name='generateinvoice'),
    
]
