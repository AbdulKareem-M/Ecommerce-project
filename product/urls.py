from . import views
from django.urls import path

urlpatterns = [
  path('',views.ListProducts.as_view(),name='home'),
  path('add_product/',views.CreateProduct.as_view(),name='add_product'),
  path('update_product/<int:pk>/',views.UpdateProduct.as_view(),name='update_product'),
  path('delete_product/<int:pk>/',views.DeleteProduct.as_view(),name='delete_product'),
  path('product_detail/<int:pk>/',views.ProductDetail.as_view(),name='product_detail'),
  path('add_category/',views.AddCategory.as_view(),name='add_category'),
  path('update_category/<int:pk>',views.UpdateCategory.as_view(),name='update_category'),
  path('delete_category/<int:pk>',views.DeleteCategory.as_view(),name='delete_category'),
  path('category_detail/<int:pk>/',views.CategoryDetail.as_view(),name='category_detail'),
  path('all_categories',views.ListCategory.as_view(),name='all_categories'),
]