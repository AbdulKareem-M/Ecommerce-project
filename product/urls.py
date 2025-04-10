from . import views
from django.urls import path

urlpatterns = [
    # Base
    path('base/', views.base_view, name='base'),

    # Category URLs
    path('category/add/', views.CategoryCreateView.as_view(), name='add_category'),
    path('category/<int:pk>/update/', views.CategoryUpdateView.as_view(), name='update_category'),
    path('categories/', views.CategoryListView.as_view(), name='all_categories'),
    path('category/<int:pk>/delete/', views.CategoryDeleteView.as_view(), name='delete_category'),
    path('category/<int:pk>/', views.CategoryDetailView.as_view(), name='category_detail'),

    # Product URLs
    path('product/add/', views.ProductCreateView.as_view(), name='add_product'),
    path('', views.ProductListView.as_view(), name='home'),
    path('product/<int:pk>/update/', views.ProductUpdateView.as_view(), name='update_product'),
    path('product/<int:pk>/delete/', views.ProductDeleteView.as_view(), name='delete_product'),
    path('product/<int:pk>/', views.ProductDetailView.as_view(), name='product_detail'),

    # Review URLs
    path('product/<int:pk>/review/add/', views.ReviewCreateView.as_view(), name='add_review'),
    path('review/<int:pk>/update/', views.ReviewUpdateView.as_view(), name='update_review'),
    path('review/<int:pk>/delete/', views.ReviewDeleteView.as_view(), name='delete_review'),

    # Cart URLs
    path('cart/', views.CartListView.as_view(), name='listcart'),
    path('cart/add/<int:pk>/', views.CartAddItemView.as_view(), name='add_to_cart'),
    path('cart/update/<int:pk>/', views.CartUpdateItemView.as_view(), name='update_cart_item'),
    path('cart/delete/<int:pk>/', views.CartDeleteItemView.as_view(), name='delete_cart_item'),
]
