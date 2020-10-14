from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from  django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import  LoginRequiredMixin, redirect_to_login
from django.views.generic import ListView, DetailView, View
from .models import Item, OrderItem, Order, BillingAddress, FavoriteItem
from django.utils import timezone
from .forms import CheckoutForm
import stripe
global path
stripe.api_key = "sk_test_51HVDQgElO0e4X0uhR1dDfmx54LRxKAtxAM2VCmXiOeISfMk0JIRiBUxi82vSzSb0HqMlMoEgPz0fpV0eADAROZLJ00Y7jv5W7i"


def item_list(request):
    if request.user.is_authenticated:

        order, _ = Order.objects.get_or_create(user=request.user)
        context = {
            'object_list': Item.objects.all(),
            'cart_qty': order.total_items_in_cart
        }
    else:
        context = {
            'object_list': Item.objects.all(),
            'cart_qty': 0
        }
    return render(request, 'home-page.html', context)


class HomeView(ListView):
    model = Item
    template_name = 'home-page.html'

    # user_pk = request.user.pk
    # print(f'User_id= {request.user.pk}')
    # order = Order.objects.get(pk=1)
    # qty = order.total_items_in_cart
    #
    # def get_context_data(self, **kwargs):
    #     context = super(HomeView, self).get_context_data(**kwargs)
    #     context.update({'cart_qty': self.qty})
    #     return context


def checkout(request):

    order = Order.objects.get(user=request.user)
    cart_items = OrderItem.objects.all().filter(ordered=False)
    form = CheckoutForm()
    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if form.is_valid():
            print(f'form is valid, form = {form}')
            print(f'cleaned_data = {form.cleaned_data}')
            street_address = form.cleaned_data.get('street_address')
            apartment_address = form.cleaned_data.get('apartment_address')
            country = form.cleaned_data.get('country')
            zip = form.cleaned_data.get('zip')
            same_billing_address = form.cleaned_data.get('same_billing_address')
            save_info = form.cleaned_data.get('save_info')
            payment_options = form.cleaned_data.get('payment_options')
            billing_address = BillingAddress(
                user=request.user,
                street_address=street_address,
                apartment_address=apartment_address,
                countries=country,
                zip=zip
            )
            billing_address.save()
            order.billing_address = billing_address
            order.save()
            return redirect('core:home')
        else:
            messages.warning(request, 'Failed Checkout')
            return redirect('core:checkout')

    context = {
        'object_list': Item.objects.all(),
        'cart_qty': order.total_items_in_cart,
        'order': order,
        'total_amount': order.total_amount,
        'form': form
    }

    return render(request, 'checkout-page.html', context)

class PaymentView(View):
    def get(self, *args, **kwargs):
        return render(self.request, 'payment.html', {})


class ProductDetailView(DetailView):
    model = Item
    template_name = 'product-page.html'

    def get_context_data(self, **kwargs):
        global path
        path = self.request.path_info
        print(path)
        order = Order.objects.get(user=self.request.user)
        context = super(ProductDetailView, self).get_context_data(**kwargs)
        context.update({'cart_qty': order.total_items_in_cart})
        return context




# def product(request):
#     context = {
#         'items': Item.objects.all()
#     }
#     return render(request, 'product-page.html', context)

class OrderSummaryView(View):

    def get(self, *args, **kwargs):
        global path
        path = self.request.path_info
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            # print(f'order = {order}')
            # print(order.items.all())
            context = {
                'object': order,
                'cart_qty': order.total_items_in_cart,
                'path': path
            }
            return render(self.request, 'order_summary.html', context)
        except ObjectDoesNotExist:
            messages.error(self.request, "You don't have an active order")
            return redirect("/")

def add_to_cart(request, pk):
    global path
    x = path[1:-1]
    print(x)
    item = get_object_or_404(Item, pk=pk)
    print(f'item = {item}')

    order_item, _ = OrderItem.objects.get_or_create(item=item, user=request.user, ordered=False)

    print(f'order_item = {order_item}')
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    print(f'order_qs = {order_qs}')
    order = Order.objects.get(user=request.user)
    if order_qs.exists():
        order = order_qs[0]
        print(f'order = {order}')
        if order.items.filter(item__slug=item.slug).exists():
            order_item.quantity += 1
            order_item.save()
            order.total_items_in_cart += 1
            order.save()
            if item.discount_price:
                order.total_amount += item.discount_price
            else:
                order.total_amount += item.price
            order.save()
            if x != 'order-summary':
                messages.info(request, 'Item quantity updated')
        else:
            order.items.add(order_item)
            order.total_items_in_cart += 1
            order.save()
            if item.discount_price:
                order.total_amount += item.discount_price
            else:
                order.total_amount += item.price
            order.save()
            messages.info(request, 'Item added to your cart')

            if x == 'order-summary':
                return redirect(f'core:{x}')
            else:
                return redirect('core:product', pk=pk)
    else:
        order = Order.objects.create(user=request.user, ordered_date=timezone.now())
        order.items.add(order_item)
        if x != 'order-summary':
            messages.info(request, 'Item added to your cart')
    if x == 'order-summary':
        return redirect(f'core:{x}')
    else:
        return redirect('core:product', pk=pk)


def remove_from_cart(request, pk):
    global path
    x = path[1:-1]
    item = get_object_or_404(Item, pk=pk)
    print(f'item = {item}')
    order_item = OrderItem.objects.get(item=item, user=request.user, ordered=False)
    print(f'order_item = {order_item}')
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    order = Order.objects.get(user=request.user)
    if order_qs.exists():
        order = order_qs[0]
        print(f'order = {order}')
        if order.items.filter(item__slug=item.slug).exists():
            print('!!!!!!!!!!!')
            order_item.quantity -= 1
            order_item.save()
            order.total_items_in_cart -= 1
            order.save()
            if item.discount_price:
                order.total_amount -= item.discount_price
            else:
                order.total_amount -= item.price
            order.save()
            # order.items.remove(order_item)
            # print('removed')
            if x != 'order-summary':
                messages.info(request, 'Item quantity updated')

        else:
            print('@@@@@@@@@')
            order.items.remove(order_item)
            order.total_items_in_cart -= 1
            order.save()
            if item.discount_price:
                order.total_amount -= item.discount_price
            else:
                order.total_amount -= item.discount_price
            order.save()
            if x != 'order-summary':
                messages.info(request, 'Item removed from your cart')

    if order_item.quantity == 0:
        order_item.delete()
        if x == 'order-summary':
            return redirect(f'core:{x}')
        else:
            return redirect('core:product', pk=pk)

    if x == 'order-summary':
        return redirect(f'core:{x}')
    else:
        return redirect('core:product', pk=pk)


def delete(request, pk):
    order = Order.objects.get(user=request.user)
    item = Item.objects.get(pk=pk)
    print(item)
    order_item = OrderItem.objects.get(item=item, user=request.user)
    print(order_item)
    order.total_items_in_cart = order.total_items_in_cart - order_item.quantity
    order.save()
    print(order.total_items_in_cart)
    print(f'total_amount = {order.total_amount}')
    if item.discount_price:
        order.total_amount = order.total_amount-(order_item.quantity*item.discount_price)
        order.save()
        print(order.total_amount)
    else:
        order.total_amount = order.total_amount-(order_item.quantity*item.price)
        order.save()
        print(order.total_amount)
    order_item.delete()

    return redirect('core:order-summary')


def charge_base(request):
    return render(request, 'charge_base.html', {})


def charge(request):
    order = Order.objects.get(user=request.user)
    order_item = OrderItem.objects.all()
    stripe.Customer.create(
        name=request.user.username,
    )
    stripe.Charge.create(
        amount=order.total_amount*100,
        currency="inr",
        source='tok_visa'
    )
    OrderItem.objects.update(ordered=True)
    Order.objects.update(total_items_in_cart=0, total_amount=0)
    # order.items.remove(order_item)
    # order_item.delete()
    for item in order.items.all():
        order.items.remove(item)
    return redirect('core:home')

def add_to_favorites(request, pk):
    item = get_object_or_404(Item, pk=pk)
    favorite_item = FavoriteItem.objects.create(item=item, user=request.user)
    return redirect('core:product', pk=pk)


class FavoritesView(ListView):
    model = FavoriteItem
    template_name = 'favorite-page.html'



