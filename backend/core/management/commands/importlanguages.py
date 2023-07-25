from django.conf.locale import LANG_INFO
from django.core.management.base import BaseCommand, CommandError

from users.models import Language


class Command(BaseCommand):
    help = 'Imports language codes and names from django.conf.locale.LANG_INFO'

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        if not Language.objects.exists():
            self.stdout.write('Languages not found, creating ones')
            cnt = 0
            for isocode in LANG_INFO:
                if len(isocode) == 2:  # we only care about the 2 letter iso codes
                    try:
                        lang = Language(
                            isocode=isocode,
                            name=LANG_INFO[isocode]['name'],
                            name_local=LANG_INFO[isocode]['name_local']
                        )
                        lang.save()
                        cnt += 1
                    except Exception as e:
                        raise CommandError(
                            'Error adding language %s: %s' % (lang, e)
                        )
            self.stdout.write('Added %d languages to users' % cnt)
        else:
            self.stdout.write('Languages were found, exiting')
