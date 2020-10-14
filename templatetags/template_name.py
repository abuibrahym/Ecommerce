from django import template
from jd_ecommerce.core.models import Order

register = template.Library()

# @register.filter
# def cart_item_count(user):
#     if user.is_authenticated:
#         pass

@register.filter
def cart_qty(user):
    if user.is_authenticated:
        user_pk = user.pk
        # print(f'User_id= {request.user.pk}')
        q=Order.objects.get(pk=user_pk)
        qty =q.total_items_in_cart
        return qty
    else:
        return 0
