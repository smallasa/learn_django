# 导入url模块
from django.conf.urls import url
# 导入view试图模块
from . import views


#定义APP名字
app_name = 'blog'


urlpatterns = {
    url(r'^$', views.index, name='blog_index'),
    url(r'^(?P<blog_id>[0-9]+)', views.detail, name='blog_detail'),
}
