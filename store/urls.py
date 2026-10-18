from django.urls import path
from . import views

app_name = 'store'

urlpatterns = [
    path('', views.home, name='home'),
    path('bo-suu-tap/', views.catalog, name='catalog'),
    path('san-pham/<slug:slug>/', views.product_detail, name='product_detail'),
    path('api/dat-hang/', views.place_order, name='place_order'),
    path('api/chat/', views.api_chat, name='api_chat'),
    path('gioi-thieu/', views.about, name='about'),
]
