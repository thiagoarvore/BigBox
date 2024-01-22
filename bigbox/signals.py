from django.db.models.signals import pre_save, pre_delete, post_delete, post_save, m2m_changed
from django.dispatch import receiver
from bigbox.models import Kit, Product

@receiver(m2m_changed, sender=Kit.content.through)
def kit_post_save(sender, instance, action, **kwargs):
    if action == 'post_add':
        for product in instance.content.all():
            product.amount -= 1
            product.save()

            