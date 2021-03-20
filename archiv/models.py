from django.db import models


class NerSource(models.Model):
    title = models.CharField(
        max_length=250,
        unique=True,
    )
    info = models.JSONField()

    def __str__(self):
        return f"{self.title}"


class NerSample(models.Model):
    ner_text = models.TextField(
        blank=True, null=True, verbose_name="text", help_text="text"
    )
    ner_sample = models.JSONField(
        blank=True, null=True, verbose_name="text", help_text="text"
    )
    ner_ent_exist = models.BooleanField(
        default=False, verbose_name="Contains Entities"
    )
    ner_source = models.ForeignKey(NerSource, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.ner_text[:20]}"
