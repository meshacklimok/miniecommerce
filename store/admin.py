from django.contrib import admin
from .models import Product, Category, ProductImage, Review

# ----------------------------
# Product Admin
# ----------------------------
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'category', 'is_in_stock', 'views_count', 'created_at')
    readonly_fields = ('views_count', 'created_at', 'updated_at')
    list_filter = ('category', 'is_in_stock')
    search_fields = ('name', 'description')
    prepopulated_fields = {'slug': ('name',)}
    ordering = ('-created_at',)

# ----------------------------
# Category Admin
# ----------------------------
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name',)

# ----------------------------
# Product Image Admin
# ----------------------------
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ('product', 'uploaded_at')
    readonly_fields = ('uploaded_at',)
    search_fields = ('product__name',)

# ----------------------------
# Review Admin
# ----------------------------
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('product', 'customer', 'rating', 'created_at')
    readonly_fields = ('created_at',)
    search_fields = ('product__name', 'customer__username')

# Register all models
admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(ProductImage, ProductImageAdmin)
admin.site.register(Review, ReviewAdmin)
