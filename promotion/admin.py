from django.contrib import admin
from .models import PromotionCode

class PromotionCodeAdmin(admin.ModelAdmin):
    list_display = ('promotion_code', 'discount_amount', 'is_used', 'created_at', 'used_at')
    list_filter = ('is_used', 'created_at', 'used_at')
    search_fields = ('promotion_code', 'used_at', 'discount_amount')
    readonly_fields = ('created_at', 'used_at')
    ordering = ('-created_at',)

admin.site.register(PromotionCode, PromotionCodeAdmin)
