from django.contrib import admin
from django.views.generic import RedirectView
from django.urls import path, reverse_lazy
from accounts.views import login_view
from bigbox.views import KitDetailView, ProductsListView, Test, ProductDetailView, ProductCreateView, ProductUpdateView, ProductDeleteView, ProductLogListView, KitListView, create_kit, KitDeleteView, create_identical_kit, CategoryCreateView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', login_view, name='login'),
    path('logout', RedirectView.as_view(url=reverse_lazy('login')), name='redirect_to_login'),
    path('', RedirectView.as_view(url=reverse_lazy('login')), name='redirect_to_login'),
    path('products_list/', ProductsListView.as_view(), name='products_list'),
    path('test/', Test.as_view(), name='test'),
    path('product/<int:pk>/', ProductDetailView.as_view(), name='product_detail'),
    path('new_product/', ProductCreateView.as_view(), name='new_product'),
    path('product/<int:pk>/update/', ProductUpdateView.as_view(), name='product_update'),
    path('product/<int:pk>/delete/', ProductDeleteView.as_view(), name='product_delete'),
    path('product/<int:pk>/log', ProductLogListView.as_view(), name='product_log'),
    path('new_kit/', create_kit, name='new_kit'),
    path('kit_list/', KitListView.as_view(), name='kit_list'),
    path('kit/<int:pk>', KitDetailView.as_view(), name='kit_detail'),
    path('kit/<int:pk>/delete/', KitDeleteView.as_view(), name='kit_delete'),
    path('kit/<int:pk>/create_identical/', create_identical_kit, name='create_identical_kit'),
    path('new_category/', CategoryCreateView.as_view(), name='new_category'),
]
