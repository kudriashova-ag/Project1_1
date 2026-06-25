from django.db import models
from django.conf import settings
from .tag import Tag
from .mixins import SlugMixin, TimeMixin


class Product(SlugMixin, TimeMixin):
    category = models.ForeignKey(
        'Category', 
        related_name='products', 
        on_delete=models.SET_NULL, 
        null=True, 
        verbose_name='Категорія')
    name = models.CharField('Назва', max_length=100) 
    description = models.TextField('Опис',blank=True, null=True)
    price = models.DecimalField('Ціна',max_digits=10, decimal_places=2)
    sale_price = models.DecimalField('Ціна зі знижкою', max_digits=10, decimal_places=2, null=True, blank=True)
    tags = models.ManyToManyField(Tag, through='ProductTag', blank=True)
    stock = models.PositiveIntegerField('На складі',default=0)
    is_available = models.BooleanField('Доступний',default=True)
    total_price = models.DecimalField('Сума',max_digits=10, decimal_places=2, blank=True, null=True, editable=False)
    image = models.ImageField(
        upload_to='products/',  # папка всередині MEDIA_ROOT
        blank=True,               # поле необов'язкове у формах
        null=True                 # дозволяє NULL у БД
    )
    
    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товари'
        ordering = ['name']
        indexes = [
            models.Index(fields=['slug']),
            models.Index(fields=['category']),
            models.Index(fields=['is_available', 'stock']),  
        ]
        
        constraints = [
            models.CheckConstraint(
                name='product_price_positive',
                condition=models.Q(price__gt=0) & models.Q(price__lt=9999999),
                violation_error_message="Ціна повинна бути від 0 до 9999999",
            ),
            models.CheckConstraint(
                name='product_stock_positive',
                condition=models.Q(stock__gte=0),
                violation_error_message="Кількість товару повинна бути більше або дорівнювати 0",
            ),
        ]
        
    def save(self, *args, **kwargs):
        """перед збереженням .save()   Product.objects.create()"""
        self.total_price = self.price * self.stock
        
        # is_new = self.pk is None
        # if is_new:
        #     print("Новий товар")
        
            
        super().save(*args, **kwargs)
         
            
    # def delete():
    # .delete()
    # super().save(*args, **kwargs)
        
    
    
    #  ---- property ----
    @property
    def available(self):
        return self.is_available and self.stock > 0
    
    @property
    def current_price(self):
        return self.sale_price if self.sale_price else self.price
    
    @property
    def is_on_sale(self):
        return self.sale_price is not None
    
    @property
    def image_url(self):
        if self.image:
            return self.image.url
        return settings.STATIC_URL + 'images/no-photo.jpg'
    
    
    def __str__(self):
        return self.name
    