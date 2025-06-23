
"""
# プロジェクト全体のurl設定を定義
特定のURLにアクセスした時にURLとViewのつながりを定義する

## 例
- path("EasyLiveMemo", include("EasyLiveMemo.urls"))

EasyLiveMemo 以下の URL がすべて EasyLiveMemo/urls.py の中で定義された URL に従って処理される

"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('EptMyAdminSite/', admin.site.urls),
    path('', include('TopPage.urls')),
    path('EasyMdBlog/', include('EasyMdBlog.urls')),
    path('EasyLiveMemo/', include('EasyLiveMemo.urls')),
    path('EasySurvey/', include('EasySurvey.urls'))
]
