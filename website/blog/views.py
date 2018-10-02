from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request, 'blog/index.html', locals())

# 由于路由中有传参，所以定义视图时，需要把参数也写上
def detail(request, blog_id):
    return render(request, 'blog/detail.html', locals())