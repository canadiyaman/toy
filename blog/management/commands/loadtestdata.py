import uuid

from django.core.management import BaseCommand


from user.models import Writer
from blog.models import Article


class Command(BaseCommand):
    help = "Generates initial events and categories"

    def add_arguments(self, parser):
        parser.add_argument(
            "-c",
            nargs="?",
            type=int,
            help="Count of Event wanted to create (default: 100)",
        )
        parser.add_argument(
            "-cn",
            nargs="?",
            type=str,
            help="You can give category names with using to separate with comma (eg. Work,Spor)",
        )

    def handle(self, *args, **options):
        for i in range(10):
            user, _ = Writer.objects.get_or_create(
                username=f"test_user_{i}", is_editor=False
            )

            for i_i in range(15):
                Article.objects.create(
                    title=f"Test Data Title {i_i} {uuid.uuid4()}",
                    content=f"Test Content {i_i}",
                    written_by=user,
                )
