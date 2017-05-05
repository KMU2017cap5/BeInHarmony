from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.main),
	url(r'/main', views.main), # 메인
	url(r'/intro', views.intro), # 소개
	url(r'/webcam', views.webcam), # 카메라
	url(r'/undecided', views.cloth), # 옷고르기
]