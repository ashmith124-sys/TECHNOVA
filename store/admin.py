from django.contrib import admin
from .models import category,product,banner,Order
# Register your models here.

@admin.register(category)
class categoryAdmin(admin.ModelAdmin):
    list_display=('name','activate')
    prepopulated_fields={'slug':('name',)}

@admin.register(product)
class productAdmin(admin.ModelAdmin):
    list_display=('name','category','price','stock','image_preview','active','created_at')
    list_filter=('category','active','created_at')
    search_fields=('name','description')
    prepopulated_fields={'slug':('name',)}
    ordering = ('-created_at',)
    def image_preview(self, obj):
        if obj.image:
            return f'<img src="{obj.image.url}" width="60" height="60" style="object-fit:cover;">'
        return "No Image"
    image_preview.allow_tags = True
    image_preview.short_description = "Image"

@admin.register(banner)
class bannerAdmin(admin.ModelAdmin):
    list_display=('title','active','create_at')
    list_filter=('active',)
    search_fields=('title','content')


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'name',
        'email',
        'phone',
        'total_amount',
        'status',
        'created_at'
    )

    list_filter = ('status', 'created_at')
    search_fields = ('name', 'email', 'phone', 'user__username')
    ordering = ('-created_at',)