from . import views
from django.urls import path

urlpatterns = [
  path('',views.ListProducts.as_view(),name='home'),
  path('add_product/',views.CreateProduct.as_view(),name='add_product'),
  path('add_category/',views.AddCategory.as_view(),name='add_category'),
  path('update_category/<int:pk>',views.UpdateCategory.as_view(),name='update_category'),
  path('all_categories',views.ListCategory.as_view(),name='all_categories'),
]