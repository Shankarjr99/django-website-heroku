from django.urls import path
import include
from . import views

urlpatterns = [
    path("blog/",views.index,name="blog"),
    path("contact",views.Contact,name="contact"),
    path("",views.Home,name="home"),
    path("search",views.search,name="search"),
    path('signup',views.signup,name="signup"),
    path('login',views.loginmodal,name='login'),
    path('logout',views.logoutmodal,name='logout'),
    path('new_comment',views.new_comment,name='new_comment'),
    # path('oauth/', include('social_django.urls', namespace='social')),
    path("<str:slug>",views.Details,name='details')
]