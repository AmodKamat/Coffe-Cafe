from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
urlpatterns=[
    path("",views.home),
    path("register/",views.register),
    path("login/",views.user_login),
    path("logout/",views.user_logout),
    path("catfilter/<cid>",views.catfilter,name="catfilter"),
    path("productdetail/<pid>",views.productdetail),
    path("addtocart/<pid>",views.addtocart),
    path("viewcart/",views.viewcart),
    path("remove/<cid>",views.removefromcart),
    path("updateqty/<qv>/<cid>",views.upadateqty),
    path("placeorder",views.placeorder),
    path("makepayment",views.makepayment),
    path("sendmail",views.sendusermail),
    path('password_reset/', views.password_reset, name='password_reset'),
    path('password_reset/done/', views.password_reset_done, name='password_reset_done'),
    path('reset/<uidb64>/<token>/', views.password_reset_confirm, name='password_reset_confirm'),
    path('reset/done/', views.password_reset_complete, name='password_reset_complete'),
    
    
]


if settings.DEBUG:
    urlpatterns+=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)