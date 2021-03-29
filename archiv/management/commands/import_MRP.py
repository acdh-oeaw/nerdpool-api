import json

from django.core.management.base import BaseCommand
from tqdm import tqdm

from archiv.models import NerSource, NerSample

source_json = {
    "title": "MRP",
    "info": {
        "creators": [
            {
                "name": "Ademir Hamzabegovic",
            }
        ],
        "description": "Ministerratsprotokolle"
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
        filepath = 'mrp.jsonl'
        with open(filepath) as fp:
            for x in tqdm(fp.readlines(), total=10319):
                data = json.loads(x)
                text = data['text']
                ner_exist = bool(data['spans'])
                if ner_exist:
                    entities = [[x['start'], x['end'], x['label']] for x in data['spans']]
                else:
                    entities = []
                ner_item = {
                    "text": text,
                    "entities": entities
                }
                NerSample.objects.create(
                    ner_text=text,
                    ner_sample=ner_item,
                    ner_ent_exist=ner_exist,
                    ner_source=source
                )
