from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import OrderInfo, OrderDetailInfo
from user_part.decorator import login as user_login
from user_part.models import Userinfo
from carts.models import CartInfo
from datetime import datetime
from decimal import Decimal
from django.db import transaction


@user_login
def order(request):
    user_id = request.session['user_id']
    user = Userinfo.objects.get(pk=user_id)
    cart_ids = []
    cart_ids1 = request.GET.get('cart_ids')
    for each in cart_ids1:
        cart_ids.append(int(each))
    carts = []
    for each in cart_ids:
        cart = CartInfo.objects.get(pk=each)
        carts.append(cart)
    context = {'carts':carts,
               'cart_ids1':cart_ids1,
               'user':user}
    return render(request, 'place_order.html', context)


@transaction.atomic()
@user_login
def order_handler(request):
    tran_id = transaction.savepoint()
    # 接收购物车编号
    cart_ids = request.GET.get('cart_ids')
    try:
        # 创建订单对象
        order = OrderInfo()
        user_id = request.session['user_id']
        user_address = Userinfo.objects.get(id=user_id).user_address
        order.order_user_id = user_id
        order.address = user_address
        order.total_price = Decimal(request.GET.get('total_price'))
        now = datetime.now()
        order.order_id = '%s%d'%(now.strftime('%Y%m%d%H%M%S'), user_id)
        order.order_date = now
        order.save()

        # 创建详单对象
        cart_ids1 = [int(each) for each in cart_ids]
        for each in cart_ids1:
            order_detail = OrderDetailInfo()
            order_detail.order = order
            # 查询购物车信息
            cart = CartInfo.objects.get(id=each)
            # 判断商品库存
            # 如果库存大于购买数量，则减少库存
            product = cart.product
            if product.product_stock >= cart.count:
                product.product_stock -= cart.count
                product.save()
                # 完善详单信息
                order_detail.products_id =product.id
                order_detail.price = product.product_price
                order_detail.count = cart.count
                order_detail.save()
                # 删除购物车数据
                cart.delete()
            # 如果库存小于购买数量
            else:
                transaction.savepoint_rollback(tran_id)
                return JsonResponse({'state':0})
        transaction.savepoint_commit(tran_id)
        state = 1
    except Exception as e:
        print('=================%s' %e)
        transaction.savepoint_rollback(tran_id)
        state = 2
    return JsonResponse({'state':state})


@user_login
def pay(request, id):
    order = OrderInfo.objects.get(pk=id)
    order.is_Pay = True
    order.save()
    return redirect('/user/order')


