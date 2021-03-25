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
