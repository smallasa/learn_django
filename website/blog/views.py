from django.shortcuts import render
from django.shortcuts import get_object_or_404

# 要展示所有博客，就需要先导入models
from . import models

#导入markdown
import markdown

#导入语法高亮度
import pygments

#Django内置分页功能
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# 导入Django导入搜索函数
from django.db.models import Q


# Create your views here.


# 展示当前页码的方法
def make_paginator(objects, page, num=5):
    paginator = Paginator(objects, num)

    try:
        object_list = paginator.page(page)
    except PageNotAnInteger:
        object_list = paginator.page(1)
    except EmptyPage:
        object_list = paginator.page(paginator.num_pages)

    return object_list, paginator

# 自定义分页方法
def pagination_data(paginator, page):
    # 如果无法分页，则无需展示分页导航条
    if paginator.num_pages == 1:
        return {}

    # 当前页的左边，初始值为空
    left = []

    # 当前页的右边，初始值为空
    right = []

    # 标示第1页页码后是否需要显示省略号
    left_has_more = False

    # 标示最后一页页码前是否需要显示省略号
    right_has_more = False

    # 表示是否需要显示第1页第页码号
    first = False

    # 表示是否需要显示最后一页的页码号
    last = False

    # 获得当前请求的页码号
    try:
        page_number = int(page)
    except ValueError:
        page_number = 1
    except:
        page_number = 1

    # 获得分页后的总页数
    total_pages = paginator.num_pages

    # 获得整个分页页码列表
    page_range = paginator.page_range

    if page_number == 1:
        right = page_range[page_number:page_number + 4]

        if right[-1] < total_pages - 1:
            right_has_more = True

        if right[-1] < total_pages:
            last = True
    elif page_number == total_pages:
        left = page_range[(page_number - 3) if (page_number - 3) > 0 else 0:page_number - 1]

        if left[0] > 2:
            left_has_more = True

        if left[0] > 1:
            first = True
    else:
        left = page_range[(page_number - 3) if (page_number - 3) > 0 else 0:page_number - 1]
        right = page_range[page_number:page_number + 2]

        if right[-1] < total_pages - 1:
            right_has_more = True
        if right[-1] < total_pages:
            last = True

        if left[0] > 2:
            left_has_more = True
        if left[0] > 1:
            first = True

    data = {
        'left': left,
        'right': right,
        'left_has_more': left_has_more,
        'right_has_more': right_has_more,
        'first': first,
        'last': last,
    }

    return data


def index(request):
    # 获取所有博客
    entries = models.Entry.objects.all()

    # 获取分页页码对象
    page = request.GET.get('page', 1)
    entry_list, paginator = make_paginator(entries, page)
    page_data = pagination_data(paginator, page)

    return render(request, 'blog/index.html', locals())


# 由于路由中有传参，所以定义视图时，需要把参数也写上
def detail(request, blog_id):
    # 获取浏览量的方法
    # entry = models.Entry.objects.get(id=blog_id)
    entry = get_object_or_404(models.Entry, id=blog_id)
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


# 定义分类视图
def category(request, category_id):
    c = models.Category.objects.get(id=category_id)

    entries = models.Entry.objects.filter(category=c)

    page = request.GET.get('page', 1)
    entry_list, paginator = make_paginator(entries, page)
    page_data = pagination_data(paginator, page)

    return render(request, 'blog/index.html', locals())


# 定义标签分类视图
def tag(request, tag_id):
    t = models.Tag.objects.get(id=tag_id)

    if t.name == "全部":
        entries = models.Entry.objects.all()
    else:
        entries = models.Entry.objects.filter(tags=t)

    page = request.GET.get('page', 1)
    entry_list, paginator = make_paginator(entries, page)
    page_data = pagination_data(paginator, page)

    return render(request, 'blog/index.html', locals())


# 定义搜索框视图
def search(request):
    keyword = request.GET.get('keyword', None)
    if not keyword:
        error_msg = "请输入关键字"
        return render(request, 'blog/index.html', locals())

    entries = models.Entry.objects.filter(
        Q(title__icontains=keyword)|
        Q(body__icontains=keyword)|
        Q(abstract__icontains=keyword)
    )

    page = request.GET.get('page', 1)
    entry_list, paginator = make_paginator(entries, page)
    page_data = pagination_data(paginator, page)

    return render(request, 'blog/index.html', locals())


# 定义归档视图
def archives(request, year, month):
    entries = models.Entry.objects.filter(created_time__year=year, created_time__month=month)

    page = request.GET.get('page', 1)
    entry_list, paginator = make_paginator(entries, page)
    page_data = pagination_data(paginator, page)

    return render(request, 'blog/index.html', locals())


# 定义403视图
def permission_denied(request):
    return render(request, 'blog/403.html', locals())


# 定义404视图
def page_not_found(request):
    return render(request, 'blog/404.html', locals())


# 定义403视图
def page_error(request):
    return render(request, 'blog/500.html', locals())