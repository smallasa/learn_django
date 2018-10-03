from django.shortcuts import render

# 要展示所有博客，就需要先导入models
from . import models

#导入markdown
import markdown
#导入语法高亮度
import pygments

# Create your views here.


def index(request):
    # 获取所有博客
    entries = models.Entry.objects.all()

    return render(request, 'blog/index.html', locals())


# 由于路由中有传参，所以定义视图时，需要把参数也写上
def detail(request, blog_id):
    # 获取浏览量的方法
    entry = models.Entry.objects.get(id=blog_id)
    # 定义markdown
    md = markdown.Markdown(extensions=[
        'markdown.extensions.extra',
        'markdown.extensions.codehilite',
        'markdown.extensions.toc',
    ])
    # 将body内容转换为html
    entry.body = md.convert(entry.body)
    entry.toc = md.toc
    entry.increase_visitting()
    return render(request, 'blog/detail.html', locals())