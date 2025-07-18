from django.db import models

# Create your models here.

class CodeDB(models.Model):
    is_new_data = models.BooleanField(verbose_name="isNewData", default=True)
    is_stop = models.BooleanField(verbose_name="isStop", default=False)
    time_delay = models.FloatField(verbose_name="timeDelay",blank=False,null=False,default=0.5)
    text = models.TextField(verbose_name="text", blank=True, null=True)

    def __str__(self):
        return f"obj: {self.time_delay} -> {self.text}"