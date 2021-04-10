import json

from django.core.management.base import BaseCommand
from tqdm import tqdm

from archiv.models import NerSource, NerSample

source_json = {
    "title": "RTA",
    "info": {
        "creators": [
            {"name": "Roman Bleier", "github_name": "bleierr"},
            {"name": "Jacqueline More", "github_name": "jackymore"},
            {"name": "Magdalene Ebner"}
        ],
        "description": "From June to October 1576, Emperor Maximilian II and more than 200 representatives of the Reichsstände discussed and decided on the political fate of (Eastern) Central Europe in Regensburg. Envoys from (almost) all over Europe took this as an opportunity to go to Lower Bavaria as well. They made the Reichstag a place of European politics. This event has left a great deal of written documentation which are edited and published in the project The Imperial Diet of Regensburg, 1576 -- digital.",
        "license": "https://creativecommons.org/licenses/by-nc/4.0/",
        "url": "https://reichstagsakten-1576.uni-graz.at/en/"
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
            for x in tqdm(fp.readlines(), total=10442):
                data = json.loads(x)
                text = data['text']
                ner_exist = bool(data['entities'])
                NerSample.objects.create(
                    ner_text=text,
                    ner_sample=data,
                    ner_ent_exist=ner_exist,
                    ner_source=source
                )
