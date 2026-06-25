from django.db import models
 
class Attribute(models.Model):
    """Тип характеристики: Колір, Розмір, Діагональ..."""
    name = models.CharField(max_length=100)           # 'Колір'
    slug = models.SlugField(max_length=100, unique=True)  # 'color'

    def __str__(self):
        return self.name


class AttributeValue(models.Model):
    """Конкретне значення: Червоний, XL, 55"..."""
    attribute = models.ForeignKey(
        Attribute,
        on_delete=models.CASCADE,
        related_name='values'
    )
    value = models.CharField(max_length=200)          # 'Червоний'

    class Meta:
        unique_together = ('attribute', 'value')      # не дублювати

    def __str__(self):
        return f'{self.attribute.name}: {self.value}'


class ProductAttribute(models.Model):
    """Зв'язок товару з конкретним значенням характеристики"""
    product = models.ForeignKey(
        'Product',
        on_delete=models.CASCADE,
        related_name='attributes'
    )
    attribute_value = models.ForeignKey(
        AttributeValue,
        on_delete=models.CASCADE,
        related_name='products'
    )

    class Meta:
        unique_together = ('product', 'attribute_value')

    def __str__(self):
        return f'{self.product} — {self.attribute_value}'