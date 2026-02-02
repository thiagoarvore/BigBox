from django.contrib import admin

from bigbox.models import Category, Kit, Product


class ProductAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "category",
        "amount",
        "price",
    )
    search_fields = (
        "name",
        "category",
    )


class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)


class KitAdmin(admin.ModelAdmin):
    list_display = ("label",)


admin.site.register(Kit, KitAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategoryAdmin)
