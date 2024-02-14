from django.db import models
from auditlog.registry import auditlog
from auditlog.models import AuditlogHistoryField
from django.http import HttpRequest
class Category(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    
class Product(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name='product_category')
    ativo = models.BooleanField()
    amount = models.IntegerField()
    premium = models.BooleanField()
    price = models.FloatField()
    ncm = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    history = AuditlogHistoryField()

    def __str__(self):
        return f'{self.name} R$ {str(self.price)}'

class Kit(models.Model):
    id = models.AutoField(primary_key=True)
    content = models.ManyToManyField(Product, related_name='kit_content')
    cost = models.FloatField()
    price = models.FloatField()
    profit = models.FloatField()
    label = models.CharField(max_length=50)
    history = AuditlogHistoryField()

    class Meta:
        ordering = ['label']

auditlog.register(Product)
auditlog.register(Kit)