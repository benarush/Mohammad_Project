from django.core.management.base import BaseCommand
from blog.models import Post
from blog.thirdPartyApplications.automateBot import Bot


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument("--action", choices=("showonly", "realperform"))

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS("---------------------> AUTOMATE BOT START"))
        bot = Bot()
        if options['action'] == "realperform":
            bot.real_perform()
        else:
            print(bot.max_likes_per_user)
        self.stdout.write(self.style.SUCCESS("---------------------> AUTOMATE BOT FINISHED"))



