from rest_framework import serializers
from archiv.models import NerSource, NerSample


class NerSourceSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = NerSource
        fields = "__all__"
        depth = 1


class NerSampleSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = NerSample
        fields = "__all__"
        depth = 0
