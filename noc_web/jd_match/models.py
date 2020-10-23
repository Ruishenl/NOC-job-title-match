from django.db import models
from deprecated import deprecated


@deprecated
class CompareItemJT(models.Model):
    content = models.TextField()
    result_1 = models.TextField(default='')
    result_2 = models.TextField(default='')
    result_3 = models.TextField(default='')

    class Meta:
        unique_together = ["content", "result_1", "result_2", "result_3"]


@deprecated
class CompareItemJD(models.Model):
    content = models.TextField()
    result_1 = models.TextField(default='')
    result_2 = models.TextField(default='')
    result_3 = models.TextField(default='')

    class Meta:
        unique_together = ["content", "result_1", "result_2", "result_3"]


class CompareItem(models.Model):
    title = models.TextField(default='')
    description = models.TextField(default='')
    processed_text = models.TextField(default='')
    result_1 = models.TextField(default='')
    result_2 = models.TextField(default='')
    result_3 = models.TextField(default='')

    class Meta:
        unique_together = ["title", "description", "processed_text", "result_1", "result_2", "result_3"]
