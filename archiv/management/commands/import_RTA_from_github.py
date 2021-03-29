import os
import acdh_tei_pyutils
from acdh_tei_pyutils.tei import TeiReader
from github import Github

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

    help = "Fetches NERSamples from bleierr/NERDPool"

    def handle(self, *args, **kwargs):
        for x in NerSource.objects.filter(title=source_json['title']):
            x.delete()
        source = NerSource.objects.create(
            title=source_json['title'],
            info=source_json['info']
        )
        clean_markup = os.path.join(acdh_tei_pyutils.__path__[0], 'files', 'clean_markup.xsl')
        g = Github()
        repo = g.get_repo('bleierr/NERDPool')
        contents = repo.get_contents("RTA_1576")
        for x in tqdm(contents, total=len(contents)):
            dl_url = x._rawData.get('download_url')
            doc = TeiReader(xml=dl_url, xsl=clean_markup)
            ne_list = doc.extract_ne_offsets(
                parent_nodes='.//tei:body//tei:p',
                ne_xpath=".//*[contains(name(), 'Name') or name()='date' or name()='time']"
            )
            for y in ne_list:
                ner_item = {
                    "text": y[0],
                    "entities": y[1]['entities']
                }
                ner_exit = bool(y[1]['entities'])
                NerSample.objects.create(
                    ner_text=y[0],
                    ner_sample=ner_item,
                    ner_ent_exist=ner_exit,
                    ner_source=source
                )
