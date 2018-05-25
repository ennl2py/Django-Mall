from django.shortcuts import render, redirect
from django.http.response import JsonResponse
from .models import CartInfo
from user_part.decorator import login as user_login


@user_login
def cart(request):
    user_id = request.session['user_id']
    carts = CartInfo.objects.filter(user_id=user_id)
    context = {'carts':carts}
    return render(request, 'cart.html', context)


@user_login
def add(request, id, num):
    # user_id的用户购买了id的商品num个
    user_id = request.session['user_id']
    # 查看购物车中用户是否已经购买此商品，如果有则数量新增，没有的话则新建
    cart = CartInfo.objects.filter(user_id=user_id, product_id=int(id)).first()
    if cart:
        cart.count += int(num)
    else:
        cart = CartInfo()
        cart.user_id = user_id
        cart.product_id = int(id)
        cart.count = int(num)
    cart.save()
    # 返回json请求
    count = CartInfo.objects.filter(user_id=user_id).count()
    return JsonResponse({'count':count})


@user_login
def count_judge(request):
    # 返回json请求
    count = CartInfo.objects.filter(user_id=request.session['user_id']).count()
    return JsonResponse({'count': count})


@user_login
def edit(request, id, num):
    try:
        cart = CartInfo.objects.get(pk=int(id))
        cart.count = num
        cart.save()
        data = {'ok':1}
    except Exception as e:
        data = {'ok':0}
    return JsonResponse(data)


@user_login
def delete(request, id):
    try:
        cart = CartInfo.objects.get(pk=int(id))
        cart.delete()
        data = {'ok':1}
    except Exception as e:
        data = {'ok':0}
    return JsonResponse(data)
