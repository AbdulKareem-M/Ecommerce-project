from django.shortcuts import render
from django.urls import reverse_lazy
from .models import Product, Category
from django.views.generic import CreateView, ListView, UpdateView, DeleteView, DetailView

class AddCategory(CreateView):
  model  = Category
  fields = '__all__'
  template_name = 'add_category.html'
  success_url = reverse_lazy('add_category')
  

class UpdateCategory(UpdateView):
  model = Category
  fields = '__all__'
  template_name = 'update_category.html'
  success_url = reverse_lazy('home')
  

class ListCategory(ListView):
  model = Category
  template_name = 'all_categories.html'
  context_object_name = 'categories'
  

class DeleteCategory(DeleteView):
  model = Category
  template_name = 'delete_category.html'
  success_url = reverse_lazy('home')
  

class CategoryDetail(DetailView):
  model = Category
  template_name = 'category_detail.html'
  context_object_name = 'category'


class CreateProduct(CreateView):
  model = Product
  fields = ['name','image','description','stock','price', 'category']
  template_name = 'add_product.html'
  success_url = reverse_lazy('home')
  

class ListProducts(ListView):
  model = Product
  template_name = 'home.html'
  context_object_name = 'products'
  

class UpdateProduct(UpdateView):
  model = Product
  fields = fields = ['name','image','description','stock','price', 'category']
  template_name = 'update_product.html'
  success_url = reverse_lazy('home')
  

class DeleteProduct(DeleteView):
  model = Product
  template_name = 'delete_product.html'
  success_url = 'home'
  

class ProductDetail(DetailView):
  model = Product
  template_name = 'product_detail.html'
  context_object_name = 'product'
  

