from django.db import models
from mptt.models import MPTTModel, TreeForeignKey

class manytomany(MPTTModel):
    title = models.CharField(max_length=32)
    parent = TreeForeignKey('self', on_delete=models.CASCADE,
                            null=True, blank=True, related_name='children')
    fieldname = models.CharField(max_length=80, default=None)

    def __str__(self):
        return self.title

    class MPTTMeta:
        order_insertion_by = ['title']

class Test(models.Model):

    interest_in_link = models.ManyToManyField(manytomany, blank=True, default=None,related_name="interest_in_link")
