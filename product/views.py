from django.shortcuts import render
from django.urls import reverse_lazy
from .models import Product, Category
from django.views.generic import CreateView, ListView, UpdateView

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


class CreateProduct(CreateView):
  model = Product
  fields = ['name','image','description','stock','price', 'category']
  template_name = 'add_product.html'
  success_url = reverse_lazy('home')
  

class ListProducts(ListView):
  model = Product
  template_name = 'home.html'
  context_object_name = 'products'