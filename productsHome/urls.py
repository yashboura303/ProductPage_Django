from django.urls import path

from . import views

app_name = 'productsHome'
urlpatterns = [
    path('', views.home, name='home'),
    path('<int:product_id>',views.productView, name="productView" ),
    path('dashboard',views.dashboard, name="dashboard")

]
