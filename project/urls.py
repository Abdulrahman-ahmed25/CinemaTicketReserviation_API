"""project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from tickets import views
from rest_framework.authtoken.views import obtain_auth_token

#for using viewsets with number 7
from rest_framework.routers import DefaultRouter
router = DefaultRouter()
router.register('guests', views.GuestViewSet)
router.register('movies', views.MovieViewSet)
router.register('reservaions', views.ReservationViewSet)



urlpatterns = [
    path('admin/', admin.site.urls),
#part-1 by django without REST
#1 without REST framework an no model query
    path('django/jsonresponsemodel',views.no_rest_no_model),
#2 without REST framework with model query
    path('django/jsonresponsefrommodel',views.no_rest_yes_model),

#part-2 by REST
#3.1 GET POST from REST framework by function based views
    path('rest/fbv/', views.fbv_list), 
#3.2 GET PUT DELETE from REST framework by function based views
    path('rest/fbv/<int:pk>', views.fbv_pk),

#4.1 GET POST from REST framework by class based views
    path('rest/cbv/', views.CBV_list.as_view()),

#4.2 GET PUT DELETE from REST framework by class based views
    path('rest/cbv/<int:pk>', views.CBV_bk.as_view()),

#5.1 GET POST from REST framework by class based views using Mixins
    path('rest/mixinslist/', views.MixinsList.as_view()), 
#5.2 GET PUT DELETE from REST framework by class based views using Mixins
    path('rest/mixinslist/<int:pk>', views.MixinsBk.as_view()),

#6.1 GET POST from REST framework by class based views using Mixins
    path('rest/genericslist/', views.GenericsList.as_view()), 
#6.2 GET PUT DELETE from REST framework by class based views using Mixins
    path('rest/genericslist/<int:pk>', views.GenericsBk.as_view()),

#7 ViewSetClass
    path('rest/viewsets/',include(router.urls)),

#8 fbv new reservation
    path('rest/fbv/reservations',views.new_reservation),

#9 When using TokenAuthentication, you may want to provide a mechanism for clients to obtain a token given the username and password. REST framework provides a built-in view to provide this behavior. To use it, add the obtain_auth_token view to your URLconf:
    path('api-token-auth/', obtain_auth_token)
]


