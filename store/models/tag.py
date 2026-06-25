from django.conf import settings
from django.db import models

from store.models.mixins import SlugMixin

class Tag(SlugMixin):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class ProductTag(models.Model):  # кастомна проміжна модель
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
    tagged_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    tagged_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('product', 'tag')  # один тег — один раз на товар

    def __str__(self):
        return f'{self.product} → {self.tag}'