from django.contrib import admin

from store.models.attribute import AttributeValue, ProductAttribute, Attribute
from store.models.tag import ProductTag, Tag
from .models import Category, Product
from django.utils.html import format_html

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = [ 'image_preview', 'name', 'slug', 'products_count']
    prepopulated_fields = {'slug': ('name',)}
    list_display_links = ['name']
    
    def image_preview(self, obj):
        if obj.image_url:
            return format_html(
                '<img src="{}" width="60" height="60" style="object-fit: cover; border-radius: 4px;">',
                obj.image_url
            )
        return '—'
    
    def products_count(self, obj):
        return obj.products.count()

    
    

    image_preview.short_description = 'Фото'

class ProductTagInline(admin.TabularInline):
    model = ProductTag
    extra = 1
    autocomplete_fields = ('tag',)

class ProductAttributeInline(admin.TabularInline):
    model = ProductAttribute
    extra = 1
    autocomplete_fields = ('attribute_value',)


@admin.register(Attribute)
class AttributeAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}


@admin.register(AttributeValue)
class AttributeValueAdmin(admin.ModelAdmin):
    list_display = ('attribute', 'value')
    list_filter = ('attribute',)
    search_fields = ('value', 'attribute__name')  # для autocomplete

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['image_preview', 'name', 'price', 'category', 'stock', 'is_available', 'total_price']

    list_editable = ['price', 'stock', 'is_available']
    search_fields = ['name', 'category__name']
    list_filter = ['category', 'is_available']
    ordering = ['-created_at']
    prepopulated_fields = {'slug': ('name',)}
    inlines = [ProductTagInline, ProductAttributeInline]
    
    
    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" width="60" height="60" style="object-fit: cover; border-radius: 4px;">',
                obj.image.url
            )
        return '—'
    
@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name',)  
    
    

