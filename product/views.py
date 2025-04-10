from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from .models import Product, Category, Review, Cart, CartItem
from .forms import RevieForm
from django.views.generic import CreateView, ListView, UpdateView, DeleteView, DetailView, View
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

def is_user(fn):
    def wrapper(request, **kwargs):
        if not request.user.is_authenticated:
            return redirect("login")
        else:
            return fn(request, **kwargs)
    return wrapper


# base view
def base_view(request):
    categories = Category.objects.all()
    return render(request, 'base.html', {'categories': categories})


# category views
class CategoryCreateView(CreateView):
    model = Category
    fields = '__all__'
    template_name = 'category/add_category.html'
    success_url = reverse_lazy('add_category')


class CategoryUpdateView(UpdateView):
    model = Category
    fields = '__all__'
    template_name = 'category/update_category.html'
    success_url = reverse_lazy('home')


class CategoryListView(ListView):
    model = Category
    template_name = 'category/all_categories.html'
    context_object_name = 'categories'


class CategoryDeleteView(DeleteView):
    model = Category
    template_name = 'category/delete_category.html'
    success_url = reverse_lazy('home')


class CategoryDetailView(DetailView):
    model = Category
    template_name = 'category/category_detail.html'
    context_object_name = 'category'

# product views
class ProductCreateView(CreateView):
    model = Product
    fields = ['name', 'image', 'description', 'stock', 'price', 'category']
    template_name = 'product/add_product.html'
    success_url = reverse_lazy('home')


class ProductListView(ListView):
    model = Product
    template_name = 'home.html'
    context_object_name = 'products'
    paginate_by = 12

    def get_queryset(self):
        queryset = Product.objects.all()

        # Category filter
        category = self.request.GET.get('category')
        if category and category != 'All Products':
            queryset = queryset.filter(category__name=category)

        # Price range filter
        min_price = self.request.GET.get('min_price')
        max_price = self.request.GET.get('max_price')
        if min_price:
            queryset = queryset.filter(price__gte=min_price)
        if max_price:
            queryset = queryset.filter(price__lte=max_price)

        # Rating filter
        rating = self.request.GET.get('rating')
        if rating:
            queryset = queryset.filter(rating__gte=rating)

        # Availability filter
        in_stock = self.request.GET.get('in_stock')
        out_of_stock = self.request.GET.get('out_of_stock')
        if in_stock and not out_of_stock:
            queryset = queryset.filter(stock__gt=0)
        elif out_of_stock and not in_stock:
            queryset = queryset.filter(stock=0)

        # Sorting
        sort_by = self.request.GET.get('sort_by')
        if sort_by == 'price_low':
            queryset = queryset.order_by('price')
        elif sort_by == 'price_high':
            queryset = queryset.order_by('-price')
        elif sort_by == 'newest':
            queryset = queryset.order_by('-created_at')
        elif sort_by == 'popularity':
            queryset = queryset.order_by('-sales_count')

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Categories
        context['categories'] = [
            'All Products',
            'Electronics',
            'Fashion',
            'Home & Kitchen',
            'Beauty & Health',
            'Books'
        ]
        
        # Hardcoded brands since there's no Brand model
        context['brands'] = [
            'Apple',
            'Samsung',
            'Sony',
            'Nike',
            'Adidas'
        ]
        
        context['current_category'] = self.request.GET.get('category', 'All Products')
        context['current_sort'] = self.request.GET.get('sort_by', 'relevance')
        
        return context

class ProductUpdateView(UpdateView):
    model = Product
    fields = ['name', 'image', 'description', 'stock', 'price', 'category']
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


#review views
class ReviewCreateView(CreateView):
    def get(self, request, **kwargs):
        form = RevieForm()
        return render(request, 'review/add_review.html', {'form': form})

    def post(self, request, **kwargs):
        product = Product.objects.get(id=kwargs.get('pk'))
        form = RevieForm(request.POST)
        if form.is_valid():
            Review.objects.create(**form.cleaned_data, user=request.user, product=product)
            return redirect('home')
        return render(request, 'review/add_review.html', {'form': form})


class ReviewUpdateView(UpdateView):
    model = Review
    template_name = 'review/update_review.html'
    fields = ["rating", "review"]
    success_url = reverse_lazy('login')


class ReviewDeleteView(DeleteView):
    model = Review
    template_name = 'review/delete_review.html'
    success_url = reverse_lazy('login')


# cartviews
@method_decorator(login_required, name='dispatch')
class CartAddItemView(View):
    def post(self, request, **kwargs):
        product = Product.objects.get(id=kwargs.get('pk'))

        if product.stock > 0:
            cart, _ = Cart.objects.get_or_create(user=request.user)
            cart_item, created = CartItem.objects.get_or_create(cart=cart, cart_item=product)

            if not created and cart_item.quantity < product.stock:
                cart_item.quantity += 1
                cart_item.save()

        return redirect('home')


@method_decorator(is_user, name='dispatch')
class CartUpdateItemView(View):
    def post(self, request, **kwargs):
        cart_item = CartItem.objects.get(id=kwargs.get('pk'))
        new_quantity = int(request.POST.get("quantity"))

        if cart_item.quantity + new_quantity > cart_item.cart_item.stock:
            cart_item.quantity = cart_item.cart_item.stock
        else:
            cart_item.quantity += new_quantity

        cart_item.save()
        return redirect('register')


@method_decorator(is_user, name='dispatch')
class CartDeleteItemView(View):
    def get(self, request, **kwargs):
        cart = Cart.objects.get(cart=request.user)
        cart_item = CartItem.objects.get(id=kwargs.get("pk"), cart=cart)

        if cart_item:
            cart_item.delete()
        return redirect("listcart")


@method_decorator(login_required, name='dispatch')
class CartListView(View):
    def get(self, request):
        cart = Cart.objects.filter(user=request.user).first()

        if not cart:
            return render(request, 'cart.html', {'message': 'Your cart is empty.'})

        cart_items = CartItem.objects.filter(cart=cart)
        item_details = [(item, item.cart_item.price * item.quantity) for item in cart_items]

        return render(request, 'cart.html', {'c_items': item_details})
