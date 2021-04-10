import json

from django.core.management.base import BaseCommand
from tqdm import tqdm

from archiv.models import NerSource, NerSample

source_json = {
    "title": "RITA",
    "info": {
        "creators": [
            {
                "name": "Michael Span",
            }
        ],
        "description": "Die annotierten Daten stammen aus sogenannten 'Verfachbüchern' aus mittleren Pustertal aus der zweiten Hälfte des 18. Jahrhunderts.",
        "license": "https://creativecommons.org/licenses/by/4.0/",
        "url": "https://hdl.handle.net/21.11115/0000-000D-FEAB-5"
    }
}


class Command(BaseCommand):

    help = "Fetches NERSamples short_samples.json"

    def handle(self, *args, **kwargs):
        for x in NerSource.objects.filter(title=source_json['title']):
            x.delete()
        source = NerSource.objects.create(
            title=source_json['title'],
            info=source_json['info']
        )
        filepath = 'rita.jsonl'
        with open(filepath) as fp:
            for x in tqdm(fp.readlines(), total=924):
                data = json.loads(x)
                text = data['text']
                ner_exist = bool(data['entities'])
                NerSample.objects.create(
                    ner_text=text,
                    ner_sample=data,
                    ner_ent_exist=ner_exist,
                    ner_source=source
                )
