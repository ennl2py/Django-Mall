from django.shortcuts import render
from .models import ProductType, ProductInfo
from django.core.paginator import Paginator


def index(request):
    fruit_hot = ProductInfo.objects.filter(product_type_id=1).order_by('-product_click')[:4]
    fruit_latest = ProductInfo.objects.filter(product_type_id=1).order_by('-id')[:4]
    seafood_hot = ProductInfo.objects.filter(product_type_id=2).order_by('-product_click')[:4]
    seafood_latest = ProductInfo.objects.filter(product_type_id=2).order_by('-id')[:4]
    meat_hot = ProductInfo.objects.filter(product_type_id=3).order_by('-product_click')[:4]
    meat_latest = ProductInfo.objects.filter(product_type_id=3).order_by('-id')[:4]
    poultry_hot = ProductInfo.objects.filter(product_type_id=4).order_by('-product_click')[:4]
    poultry_latest = ProductInfo.objects.filter(product_type_id=4).order_by('-id')[:4]
    greens_hot = ProductInfo.objects.filter(product_type_id=5).order_by('-product_click')[:4]
    greens_latest = ProductInfo.objects.filter(product_type_id=5).order_by('-id')[:4]
    freeze_hot = ProductInfo.objects.filter(product_type_id=6).order_by('-product_click')[:4]
    freeze_latest = ProductInfo.objects.filter(product_type_id=6).order_by('-id')[:4]
    context = {'title':'天天生鲜-首页',
               'fruit_hot':fruit_hot, 'fruit_latest':fruit_latest,
               'seafood_hot':seafood_hot, 'seafood_latest':seafood_latest,
               'meat_hot':meat_hot, 'meat_latest':meat_latest,
               'poultry_hot':poultry_hot, 'poultry_latest':poultry_latest,
               'greens_hot':greens_hot, 'greens_latest':greens_latest,
               'freeze_hot':freeze_hot, 'freeze_latest':freeze_latest}
    return render(request, 'product/index.html', context)


def plist(request, type_id, page, sort):
    product_type = ProductType.objects.get(pk=int(type_id))
    latest_products = ProductInfo.objects.filter(product_type_id=int(type_id)).order_by('-id')[:2]
    if sort == '1':
        products = ProductInfo.objects.filter(product_type_id=int(type_id)).order_by('-id')
    if sort == '2':
        products = ProductInfo.objects.filter(product_type_id=int(type_id)).order_by('-product_price')
    if sort == '3':
        products = ProductInfo.objects.filter(product_type_id=int(type_id)).order_by('-product_click')
    paginator = Paginator(products, 10)
    page = paginator.page(int(page))
    context = {'title':product_type.type_name + '-商品列表',
               'product_type':product_type,
               'latest_products':latest_products,
               'sort':sort,
               'paginator':paginator,
               'page':page}
    return render(request, 'product/list.html', context)


def detail(request, id):
    product = ProductInfo.objects.get(pk=int(id))
    product.product_click += 1
    product.save()
    latest_products = ProductInfo.objects.filter(product_type_id=product.product_type_id).order_by('-id')[:2]
    context = {'title':'天天生鲜-商品详情',
               'product':product,
               'latest_products':latest_products}
    res = render(request, 'product/detail.html', context)

    # 记录最近浏览，在用户中心使用
    view_products = request.COOKIES.get('view_products', '')
    product_id = str(product.id)
    if view_products:
        products_list = view_products.split(',')
        # 先判断长度，如果等于5个，则删除最后一个
        if len(products_list) == 5:
            del products_list[4]
        # 如果该商品已经浏览过，则删除之前的记录，并添加到第一个的位置
        if products_list.count(product_id) == 1:
            products_list.remove(product_id)
        products_list.insert(0, product_id)
        view_products = ','.join(products_list)
    else:
        view_products = product_id
    res.set_cookie('view_products', view_products)
    return res
