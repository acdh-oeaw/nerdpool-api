from collections import Counter
from django.contrib.admin.utils import flatten
from django.db import models
from django.utils.functional import cached_property


class NerSource(models.Model):
    title = models.CharField(
        max_length=250,
        unique=True,
    )
    info = models.JSONField()

    def __str__(self):
        return f"{self.title}"

    @cached_property
    def related_samples(self):
        return NerSample.objects.filter(ner_source__title=self.title)

    @property
    def sample_count(self):
        return self.related_samples.count()

    @property
    def sample_stats(self):
        item = {
                'name': self.title,
                'id': self.title,
            }
        samples = self.related_samples.filter(ner_ent_exist=True)
        ents = [x['ner_sample__entities'] for x in samples.values('ner_sample__entities')]
        ents = Counter([x[2] for x in (flatten(ents))])
        item['data'] = [[k, v] for k, v in dict(ents).items()]
        return item


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
    ner_ent_type = models.CharField(
        blank=True, null=True, max_length=250,
        verbose_name="Entity Types", help_text="',' separated, e.g. PER,LOC"
    )

    def __str__(self):
        return f"{self.ner_text[:20]}"

    def save(self, *args, **kwargs):
        if self.ner_ent_exist:
            ents = [x for x in flatten(self.ner_sample['entities']) if isinstance(x, str)]
            self.ner_ent_type = ",".join(set(ents))
        super(NerSample, self).save(*args, **kwargs)
