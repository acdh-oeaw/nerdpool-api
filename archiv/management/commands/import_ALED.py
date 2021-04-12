import json
from acdh_tei_pyutils.tei import TeiReader
from django.core.management.base import BaseCommand
from tqdm import tqdm

from archiv.models import NerSource, NerSample

source_json = {
    "title": "Chronik Aldersbach",
    "info": {
        "creators": [
            {
                "name": "Robert Klugseder",
            },
            {
                "name": "Maximilian Vogeltanz",
            },
            {
                "name": "Georg Vogeler",
            }
        ],
        "description": "Deutschsprachige Chronik (Mitte 17. Jahrundert) von Abt Gerhard Hörger (reg. 1651-1659) des Zisterzienserstift Aldersbach.",
        "license": "https://creativecommons.org/licenses/by-nc/4.0/",
        "url": "http://gams.uni-graz.at/context:aled"
    }
}


class Command(BaseCommand):

    help = "Fetches NERSamples from mrp.json"

    def handle(self, *args, **kwargs):
        for x in NerSource.objects.filter(title=source_json['title']):
            x.delete()
        source = NerSource.objects.create(
            title=source_json['title'],
            info=source_json['info']
        )
        doc = TeiReader('http://gams.uni-graz.at/o:aled.1/TEI_SOURCE')
        sample = doc.extract_ne_offsets(
            ne_xpath=".//*[(name()='name' and ./@ref) or name()='date' or name()='time']"
        )
        for x in tqdm(sample, total=len(sample)):
            data = {
                "text": x[0],
                "entities": x[1]['entities']
            }
            text = x[0]
            ner_exist = bool(data['entities'])
            NerSample.objects.create(
                ner_text=text,
                ner_sample=data,
                ner_ent_exist=ner_exist,
                ner_source=source
            )