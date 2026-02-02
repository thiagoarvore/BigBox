from django.contrib import admin
from django.urls import path

from accounts.views import login_view, logout_view
from bigbox.views import (
    CategoryCreateView,
    KitDeleteView,
    KitDetailView,
    KitListView,
    ProductCreateView,
    ProductDeleteView,
    ProductDetailView,
    ProductLogListView,
    ProductsListView,
    ProductUpdateView,
    Test,
    create_identical_kit,
    create_kit,
    dashboard_view,
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("login/", login_view, name="login"),
    path("logout/", logout_view, name="logout"),
    path("", dashboard_view, name="dashboard"),
    path("dashboard/", dashboard_view, name="dashboard"),
    path("products_list/", ProductsListView.as_view(), name="products_list"),
    path("test/", Test.as_view(), name="test"),
    path("product/<int:pk>/", ProductDetailView.as_view(), name="product_detail"),
    path("new_product/", ProductCreateView.as_view(), name="new_product"),
    path(
        "product/<int:pk>/update/", ProductUpdateView.as_view(), name="product_update"
    ),
    path(
        "product/<int:pk>/delete/", ProductDeleteView.as_view(), name="product_delete"
    ),
    path("product/<int:pk>/log", ProductLogListView.as_view(), name="product_log"),
    path("new_kit/", create_kit, name="new_kit"),
    path("kit_list/", KitListView.as_view(), name="kit_list"),
    path("kit/<int:pk>", KitDetailView.as_view(), name="kit_detail"),
    path("kit/<int:pk>/delete/", KitDeleteView.as_view(), name="kit_delete"),
    path(
        "kit/<int:pk>/create_identical/",
        create_identical_kit,
        name="create_identical_kit",
    ),
    path("new_category/", CategoryCreateView.as_view(), name="new_category"),
]
