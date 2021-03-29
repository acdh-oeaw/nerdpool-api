import json

from django.core.management.base import BaseCommand
from tqdm import tqdm

from archiv.models import NerSource, NerSample

source_json = {
    "title": "RTA",
    "info": {
        "creators": [
            {
                "name": "Roman Bleier",
                "github_name": "bleierr"
            },
            {
                "name": "N.N",
                "github_name": "nn"
            }
        ],
        "description": "some description about the project"
    }
}


class Command(BaseCommand):

    help = "Fetches NERSamples jsonl file"

    def handle(self, *args, **kwargs):
        for x in NerSource.objects.filter(title=source_json['title']):
            x.delete()
        source = NerSource.objects.create(
            title=source_json['title'],
            info=source_json['info']
        )
        filepath = 'RTA.jsonl'
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
