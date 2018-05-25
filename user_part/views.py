from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponseRedirect
from django.core.mail import send_mail
from django.core.paginator import Paginator
from .models import Userinfo
from products.models import ProductInfo
from order.models import OrderInfo
from hashlib import sha1
from .decorator import login as user_login



def register(request):
    context = {'title':'用户注册'}
    return render(request, 'user/register.html', context)


def register_judge(request):
    get_datas = request.GET
    if 'user_name' in get_datas:
        count = Userinfo.objects.filter(user_name=get_datas['user_name']).count()
    if 'user_email' in get_datas:
        count = Userinfo.objects.filter(user_email=get_datas['user_email']).count()
    return JsonResponse({'count':count})


def register_handler(request):

    # 拿到POST数据
    post_datas = request.POST
    user_name = post_datas['user_name']
    user_pwd = post_datas['pwd']
    user_cpwd = post_datas['cpwd']
    user_email = post_datas['email']

    # 再次判断密码是否一致，若不一致则返回注册页面，否则进入注册流程
    if user_pwd != user_cpwd:
        return redirect('/user/register/')

    # 密码加密
    s1 = sha1()
    s1.update(user_pwd.encode('utf-8'))
    user_pwd = s1.hexdigest()

    # 进入注册流程
    user = Userinfo()
    user.user_name = user_name
    user.user_pwd = user_pwd
    user.user_email = user_email
    user.save()

    # 返回登录页面
    return redirect('/user/login/')


def login(request):
    username = request.COOKIES.get('username', '')
    context = {'title':'用户登录', 'username':username, 'error_pwd':0}
    return render(request, 'user/login.html', context)


def login_judge(request):
    get_datas = request.GET['user_name']
    count = Userinfo.objects.filter(user_name=get_datas).count()
    return JsonResponse({'count': count})


def login_handler(request):
    # 拿到POST数据
    post_datas = request.POST
    user_name = post_datas['username']
    user_pwd = post_datas['pwd']
    remember = post_datas.get('remember', 0)

    # 密码加密
    s1 = sha1()
    s1.update(user_pwd.encode('utf-8'))
    user_pwd1 = s1.hexdigest()

    # 找到用户，判断密码是否一致，若不一致
    user = Userinfo.objects.get(user_name=user_name)
    if user.user_pwd == user_pwd1:
        url = request.COOKIES.get('url', '/')
        res = HttpResponseRedirect(url)

        if remember:
            res.set_cookie('username', user_name)
        else:
            res.set_cookie('username', '', max_age=-1)

        request.session['user_id'] = user.id
        request.session['user_name'] = user.user_name

        return res
    else:
        context = {'title':'用户登录', 'username':user_name, 'userpwd':user_pwd, 'error_pwd':1}
        return render(request, 'user/login.html', context)


def forget(request):
    context = {'title': '重置密码'}
    if request.method == 'POST':
        user = Userinfo.objects.filter(user_name=request.POST['username']).first()
        token = user.generate_reset_token()
        href = "http://127.0.0.1:8000/user/reset/?token=" + token
        message = user.user_name + ' 您申请了重置登录密码<br>请在1小时内点击<a href="' + href +'">此链接</a>' + \
                  '以完成重置'
        send_mail('密码重置', '', '94112776@qq.com', [user.user_email], fail_silently=False, html_message=message)
        return redirect('/user/login/')
    return render(request, 'user/forget.html', context)


def reset(request):
    if request.method == 'POST':
        if not request.session.get('r_token'):
            return redirect('/user/forget/')

        new_pwd = request.POST['pwd']

        s1 = sha1()
        s1.update(new_pwd.encode('utf-8'))
        new_pwd = s1.hexdigest()

        if Userinfo.reset_password(request.session['r_token'], new_pwd):
            del request.session['r_token']
            return redirect('/user/login/')
        else:
            return redirect('/user/forget/')
    else:
        token = request.GET.get('token')
        if token:
            request.session['r_token'] = token
        context = {'title': '重置密码'}
        return render(request, 'user/reset.html', context)


def logout(request):
    request.session.flush()
    return redirect('/')


@user_login
def info(request):
    user_email = Userinfo.objects.get(id=request.session['user_id']).user_email
    view_products = request.COOKIES.get('view_products', '')
    view_list = []
    if view_products:
        view_products = view_products.split(',')
        for each in view_products:
            view_list.append(ProductInfo.objects.get(pk=int(each)))
    context = {'title':'个人信息',
               'user_name':request.session['user_name'],
               'user_email':user_email,
               'view_list':view_list}
    return render(request, 'user/user_center_info.html', context)


@user_login
def order(request):
    user_id = request.session['user_id']
    orders = OrderInfo.objects.filter(order_user_id=user_id).order_by('-order_date')
    paginator = Paginator(orders, 2)
    page = paginator.page(1)
    context = {'title':'全部订单',
               'orders':orders,
               'paginator': paginator,
               'page': page}
    return render(request, 'user/user_center_order.html', context)


@user_login
def order_page(request, page):
    user_id = request.session['user_id']
    orders = OrderInfo.objects.filter(order_user_id=user_id).order_by('-order_date')
    paginator = Paginator(orders, 2)
    page = paginator.page(int(page))
    context = {'title':'全部订单',
               'orders':orders,
               'paginator': paginator,
               'page': page}
    return render(request, 'user/user_center_order.html', context)


@user_login
def site(request):
    user = Userinfo.objects.get(id=request.session['user_id'])
    if request.method == "POST":
        post_datas = request.POST
        user.user_rman = post_datas['r_man']
        user.user_address = post_datas['address']
        user.user_mnumber = post_datas['mnumber']
        user.user_pnumber = post_datas['pnumber']
        user.save()
    context = {'title':'收货地址', 'user':user}
    return render(request, 'user/user_center_site.html', context)