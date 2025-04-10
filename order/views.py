from django.shortcuts import render, redirect
from django.views import View
from .models import Order, OrderItem, OrderSummary
from product.models import Cart, CartItem, Product
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
import razorpay
from django.conf import settings



@method_decorator(login_required, name='dispatch')
class OrderSingleProductView(View):
    """
    Handles ordering a single product directly.
    """

    def get(self, request, **kwargs):
        product_id = kwargs.get('pk')
        product = Product.objects.get(id=product_id)
        return render(request, 'orderpage.html', {'item': product})

    def post(self, request, **kwargs):
        product_id = kwargs.get('pk')
        product = Product.objects.get(id=product_id)
        quantity = int(request.POST.get('quantity'))
        total = quantity * product.price

        order, created = Order.objects.get_or_create(user=request.user, status="pending")

        OrderItem.objects.create(order=order, quantity=quantity, item=product)

        return redirect('order_success')


@method_decorator(login_required, name='dispatch')
class OrderFromCartView(View):
    """
    Handles placing an order with all items in the user's cart.
    """

    def get(self, request):
        return redirect('listcart')

    def post(self, request):
        cart = Cart.objects.get(user=request.user)
        cart_items = CartItem.objects.filter(cart=cart)

        if not cart_items.exists():
            return render(request, "cart.html", {"error": "Your cart is empty!"})

        order = Order.objects.create(user=request.user, status="pending")

        total_price = 0
        for item in cart_items:
            subtotal = item.quantity * item.cart_item.price
            total_price += subtotal
            OrderItem.objects.create(order=order, item=item.cart_item, quantity=item.quantity)

        # 2. Create Razorpay Order
        client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
        payment = client.order.create({
            "amount": int(total_price * 100),
            "currency": "INR",
            "payment_capture": "1"
        })

        # 3. Create OrderSummary
        summary = OrderSummary.objects.create(
            order_item_id=None,  # leave None if summary is per-order
            order_id=payment["id"],
            total=total_price
        )

        # 5. Clear cart
        cart_items.delete()

        # 6. Render payment page
        return render(request, "payment.html", {
            "order": order,
            "summary": summary,
            "razorpay_key": settings.RAZORPAY_KEY_ID,
            "amount": int(total_price * 100),
            "callback_url": "/order/payment/verify/"
        })


class OrderItemList(View):
    def get(self,request):

        data=OrderItem.objects.filter(order_id=request.user.id)

        return render(request,"myitems.html",{'data':data})


# import razorpay
# class PlaceOrderView(View):
    
#     def get(self,request):

#         #authentication btem  webservr and razorpay

#         client = razorpay.Client(auth=("rzp_test_fjxIXOLnt5CNWU", "ayqLYEUZEIlRnTxoD9JIEg6B"))

#         user=request.user
#         user=Order.objects.get(user=user)
#         order_items=OrderItem.objects.filter(order_id=user) #order id given in model
        
#         total=sum(i.quantity * i.item.price for i in order_items)

#         #converting paisa into ruppee

#         new_amount=int(total*100)


#         data=client.order.create(data={

#                     "amount":new_amount,
#                     "currency":"INR",
#                             })
#         print(data)
      
#         return redirect("home")

from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseBadRequest

@csrf_exempt
def verify(request):
    if request.method == "POST":
        data = request.POST
        client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))

        try:
            client.utility.verify_payment_signature({
                "razorpay_order_id": data.get('razorpay_order_id'),
                "razorpay_payment_id": data.get('razorpay_payment_id'),
                "razorpay_signature": data.get('razorpay_signature')
            })

            # Update OrderSummary
            summary = OrderSummary.objects.get(order_id=data.get('razorpay_order_id'))
            summary.payment_status = True
            summary.payment_id = data.get('razorpay_payment_id')
            summary.save()

            return render(request, "payment_success.html", {"summary": summary})

        except Exception as e:
            print("Payment verification failed:", e)
            return HttpResponseBadRequest("Payment verification failed")
