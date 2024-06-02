from django.contrib import admin
from store.models import Product, Category, Cart, CartOrder, CartOrderItem, Review, Wishlist, Gallery, Tax
class ProductAdmin(admin.ModelAdmin):
    list_display = ['title', 'price', 'category', 'shipping_amount', 'stock_qty', 'in_stock', 'farmer', 'featured']
    list_editable = ['featured']
    list_filter = ['date']
    search_fields = ['title']
  
admin.site.register(Product, ProductAdmin)
admin.site.register(Category)
admin.site.register(Cart)
admin.site.register(CartOrder)
admin.site.register(CartOrderItem)
admin.site.register(Review)
admin.site.register(Wishlist)
admin.site.register(Gallery)
admin.site.register(Tax)

