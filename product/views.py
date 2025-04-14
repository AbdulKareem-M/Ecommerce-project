from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from .models import Product, Category, Review, Cart, CartItem
from .forms import RevieForm
from django.views.generic import CreateView, ListView, UpdateView, DeleteView, DetailView, View
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

# Utility decorator for login check
def is_user(fn):
    def wrapper(request, **kwargs):
        if not request.user.is_authenticated:
            return redirect("login")
        else:
            return fn(request, **kwargs)
    return wrapper


# ------------------- CATEGORY VIEWS -------------------

class CategoryCreateView(CreateView):
    model = Category
    fields = '__all__'
    template_name = 'category/add_category.html'
    success_url = reverse_lazy('home')


class CategoryListView(ListView):
    model = Category
    template_name = 'category/all_categories.html'
    context_object_name = 'categories'


class CategoryUpdateView(UpdateView):
    model = Category
    fields = '__all__'
    template_name = 'category/update_category.html'
    success_url = reverse_lazy('home')


class CategoryDeleteView(DeleteView):
    model = Category
    template_name = 'category/delete_category.html'
    success_url = reverse_lazy('home')


class CategoryDetailView(DetailView):
    model = Category
    template_name = 'category/category_detail.html'
    context_object_name = 'category'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['products'] = Product.objects.filter(category=self.object)
        return context

# ------------------- PRODUCT VIEWS -------------------

class ProductCreateView(CreateView):
    model = Product
    fields = ['name', 'description', 'price', 'stock', 'category', 'image']
    template_name = 'product/add_product.html'
    success_url = reverse_lazy('home')


class ProductUpdateView(UpdateView):
    model = Product
    fields = ['name', 'description', 'price', 'stock', 'category', 'image']
    template_name = 'product/update_product.html'
    success_url = reverse_lazy('home')


class ProductDeleteView(DeleteView):
    model = Product
    template_name = 'product/delete_product.html'
    success_url = reverse_lazy('home')


class ProductDetailView(DetailView):
    model = Product
    template_name = 'product/product_detail.html'
    context_object_name = 'product'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['reviews'] = Review.objects.filter(product=self.object)
        return context



def home(request):
    categories = Category.objects.all()
    top_deals = Product.objects.filter(stock__gt=0).order_by('-id')[:8]
    return render(request, 'home.html', {'categories': categories, 'top_deals': top_deals})


# ------------------- REVIEW VIEWS -------------------

class ReviewCreateView(CreateView):
    model = Review
    form_class = RevieForm
    template_name = 'review/add_review.html'

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.product = get_object_or_404(Product, pk=self.kwargs['pk'])
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('product_detail', kwargs={'pk': self.kwargs['pk']})



class ReviewUpdateView(UpdateView):
    model = Review
    fields = ['rating', 'comment']
    template_name = 'review/update_review.html'
    success_url = reverse_lazy('home')


class ReviewDeleteView(DeleteView):
    model = Review
    template_name = 'review/delete_review.html'
    success_url = reverse_lazy('home')


# ------------------- CART VIEWS -------------------

@method_decorator(login_required, name='dispatch')
class CartAddItemView(View):
    def post(self, request, **kwargs):
        product = get_object_or_404(Product, id=kwargs.get('pk'))
        cart, created = Cart.objects.get_or_create(user=request.user)
        cart_item, created = CartItem.objects.get_or_create(cart=cart, cart_item=product)

        if not created and cart_item.quantity < product.stock:
            cart_item.quantity += 1
        cart_item.save()

        return redirect('home')


@method_decorator(login_required, name='dispatch')
class CartListView(View):
    def get(self, request):
        cart, _ = Cart.objects.get_or_create(user=request.user)
        items = cart.cartitem_set.select_related('cart_item')
        c_items = [(item, item.cart_item.price * item.quantity) for item in items]
        return render(request, 'cart.html', {'c_items': c_items})



@method_decorator(login_required, name='dispatch')
class CartUpdateItemView(View):
    def post(self, request, **kwargs):
        cart_item = get_object_or_404(CartItem, id=kwargs.get('pk'))
        quantity = int(request.POST.get("quantity"))

        if quantity > cart_item.cart_item.stock:
            cart_item.quantity = cart_item.cart_item.stock
        else:
            cart_item.quantity = quantity

        cart_item.save()
        return redirect('listcart')


@method_decorator(login_required, name='dispatch')
class CartDeleteItemView(View):
    def get(self, request, **kwargs):
        cart_item = get_object_or_404(CartItem, id=kwargs.get('pk'), cart__user=request.user)
        cart_item.delete()
        return redirect('listcart')
    
    
def base_view(request):
    return render(request,'base.html')
