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
