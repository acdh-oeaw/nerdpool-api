from acdh_tei_pyutils.tei import TeiReader
from django.core.management.base import BaseCommand
from tqdm import tqdm

from archiv.models import NerSource, NerSample

source_json = {
    "title": "DIPKO",
    "info": {
        "creators": [
            {
                "name": "Anna Huemer",
            },
            {
                "name": "Lisa Brunner",
            },
            {
                "name": "Philipp Humer",
            }
        ],
        "description": "Itinerarium oder rayß beschreibung von Wien in Österreich nach Constantinopel. Der Textkorpus basiert zu einem großen Teil auf Übernahmen von Passagen vorhergehender Reiseberichte, von Berichten und Relationen des Internuntius, Johann Rudolf Schmid zum Schwarzenhorn, sowie auf Aufzeichnungen und Beobachtungen von Johann Georg Metzger selbst. Die Reinschrift eigener Aufzeichnungen erfolgte mit hoher Wahrscheinlichkeit nach Abschluss der Reise",
        "license": "https://creativecommons.org/licenses/by-nc-sa/4.0",
        "url": "http://gams.uni-graz.at/context:dipko"
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
        doc = TeiReader('https://gams.uni-graz.at/o:dipko.rb/TEI_SOURCE')
        sample = doc.extract_ne_offsets(ne_xpath='.//tei:rs[not(@type="event")]')
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