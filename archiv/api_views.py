import django_filters

from rest_framework import filters
from rest_framework import viewsets

from archiv.models import NerSample, NerSource
from archiv.api_serializers import NerSampleSerializer, NerSourceSerializer


class NerSampleFilter(django_filters.FilterSet):

    class Meta:
        model = NerSample
        fields = {
            'ner_source__title': ['exact'],
            'ner_ent_type': ['contains'],
        }


class NerSampleViewSet(viewsets.ModelViewSet):
    queryset = NerSample.objects.all()
    serializer_class = NerSampleSerializer
    filter_backends = [
        django_filters.rest_framework.DjangoFilterBackend,
        filters.SearchFilter
    ]
    filter_class = NerSampleFilter
    search_fields = [
        'ner_text',
    ]


class NerSourceViewSet(viewsets.ModelViewSet):
    queryset = NerSource.objects.all()
    serializer_class = NerSourceSerializer
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend]
