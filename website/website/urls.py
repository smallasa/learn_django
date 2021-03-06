"""website URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
# 导入include模块
from django.conf.urls import include
# 导入静态图片路由
from django.conf import settings
from django.conf.urls.static import static
# 导入RSS模块
from blog.feed import LastestEntriesFeed
# 导入错误页码
from blog import views as blog_views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    # 创建二级路由(转向APP自己路由地址)
    url(r'^blog/', include('blog.urls')),
    # 定义RSS路由
    url(r'latest/feed/$', LastestEntriesFeed()),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler403 = blog_views.permission_denied
handler404 = blog_views.page_not_found
handler500 = blog_views.page_error