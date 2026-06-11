from django.db import models

class SlugMixin(models.Model):
    slug = models.SlugField('URL',unique=True)  # url-сумісний рядок 
    
    class Meta:
        abstract = True
        
        

class TimeMixin(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        abstract = True