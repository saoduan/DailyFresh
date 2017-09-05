from django.conf.urls import url
from df_user import views

urlpatterns = [
    url(r'^register/$', views.register),
    url(r'^register_handle$', views.register_handle),
    url(r'^login/$', views.login),
    url(r'^user_info_handle$', views.user_info_handle),
    url(r'^info/$', views.user_center_info),
    url(r'^register_exist/', views.register_exist),

    url(r'^order/$', views.user_order),
    url(r'^site/$', views.user_site),
    url(r'^verifycode/$', views.verifycode),
]