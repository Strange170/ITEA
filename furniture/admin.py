from django.contrib import admin
from .models import Product

class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'owner', 'created_at')
    list_filter = ('owner',)
    search_fields = ('name', 'owner__username')
    
    def get_queryset(self, request):
        # Superusers يشوفوا كل المنتجات
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        # Sellers يشوفوا منتجاتهم بس
        return qs.filter(owner=request.user)
    
    def save_model(self, request, obj, form, change):
        if not change or not obj.owner:
            obj.owner = request.user  # لو مش متحدد owner، نخليها المستخدم الحالي
        super().save_model(request, obj, form, change)

admin.site.register(Product, ProductAdmin)
