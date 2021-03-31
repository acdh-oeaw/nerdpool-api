import requests
from django.views.generic.base import TemplateView

from archiv.models import NerSource, NerSample


class HomePageView(TemplateView):

    template_name = "archiv/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['ner_source'] = NerSource.objects.all()
        context['ner_source_count'] = NerSource.objects.all().count()
        context['ner_samples_count'] = NerSample.objects.all().count()
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
