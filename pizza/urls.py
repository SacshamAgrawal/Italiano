from django.urls import path, include
from django.views.generic import TemplateView
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register('order',viewset=views.OrderViewSet)

urlpatterns = [
    path('',views.homepage,name='homepage'),
    path('menu/',views.menu,name='menu'),
    path('blog/',TemplateView.as_view(template_name='pizza/blog.html'),name='blog'),
    path('blog-single/',TemplateView.as_view(template_name='pizza/blog-single.html'),name='blog-single'),
    path('tracker/',views.tracker,name='tracker'),
    path('add_to_cart/',views.add_to_cart,name='add_to_cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('orderdone/', views.orderDone, name='orderdone'),
    path('api/',include(router.urls)),
    path("customer-service/", views.room, name="contact",),
]

