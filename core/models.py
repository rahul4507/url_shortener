from django.db import models

class URL(models.Model):
    original_url = models.URLField(max_length=200)
    short_code = models.CharField(max_length=10, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.original_url} -> {self.short_code}"

    class Meta:
        app_label = 'core'
        db_table = 'url'
        indexes = [
            models.Index(fields=['short_code'], name='short_code_index'),
        ]