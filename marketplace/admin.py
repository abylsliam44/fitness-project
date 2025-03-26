from django.contrib import admin
from .models import Category, Product, ProductImage


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1 
    readonly_fields = ('preview',)

    def preview(self, obj):
        if obj.image:
            return f'<img src="{obj.image.url}" width="100" style="object-fit: cover;" />'
        return ""
    preview.allow_tags = True
    preview.short_description = "Preview"


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'type', 'price', 'owner', 'is_active', 'created_at')
    list_filter = ('type', 'category', 'is_active')
    search_fields = ('title', 'description', 'owner__username')
    prepopulated_fields = {'slug': ('title',)}
    inlines = [ProductImageInline]


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    prepopulated_fields = {'slug': ('name',)}


@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ('product', 'image', 'uploaded_at')
