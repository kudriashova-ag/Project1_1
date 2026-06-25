from django.db import models

from django.conf import settings

from .mixins import SlugMixin

class Category(SlugMixin):
    name = models.CharField('Назва', max_length=100)
    image = models.ImageField('Зображення',
        upload_to='categories/',  # папка всередині MEDIA_ROOT
        blank=True,               # поле необов'язкове у формах
        null=True                 # дозволяє NULL у БД
    )
    
    class Meta:
        verbose_name = "Категорія"
        verbose_name_plural = "Категорії"
        #db_table = "categories"
        ordering = ["name"]    # впливає на всі QuerySet
        
    @property
    def image_url(self):
        if self.image:
            return self.image.url
        return settings.STATIC_URL + 'images/no-photo.jpg'
        
        

    def __str__(self):
        return self.name