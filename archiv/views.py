import requests
from django.contrib.admin.utils import flatten
from collections import Counter
from django.db.models import Count
from django.views.generic.base import TemplateView

from archiv.models import NerSource, NerSample


class HomePageView(TemplateView):

    template_name = "archiv/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        ner_source = list(NerSource.objects.values_list('title', 'info').annotate(num_samples=Count('nersample')))
        dict_list = [
            {
                'name': x[0],
                'y': x[2],
                'drilldown': x[0]
            } for x in ner_source
        ]
        ner_titles = [x[0] for x in list(NerSource.objects.values_list('title'))]
        drilldown = []
        for x in ner_titles:
            item = {
                'name': x,
                'id': x,
            }
            samples = NerSample.objects.filter(ner_ent_exist=True).filter(ner_source__title=x)
            ents = [x['ner_sample__entities'] for x in samples.values('ner_sample__entities')]
            ents = Counter([x[2] for x in (flatten(ents))])
            item['data'] = [[k, v] for k, v in dict(ents).items()]
            drilldown.append(item)
        context['ner_source'] = NerSource.objects.all()
        context['drilldown'] = drilldown
        context['dict_list'] = dict_list
        return context


class ImprintView(TemplateView):
    template_name = 'archiv/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        r = requests.get("https://shared.acdh.oeaw.ac.at/acdh-common-assets/api/imprint.php?serviceID=19058")

        if r.status_code == 200:
            context['imprint_body'] = f"{r.text}"
        else:
            context['imprint_body'] = """
            On of our services is currently not available. Please try it later or write an email to
            acdh@oeaw.ac.at
            """
        return context
