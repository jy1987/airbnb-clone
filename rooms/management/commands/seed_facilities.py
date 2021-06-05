from django.core.management.base import BaseCommand
from rooms.models import Facility


class Command(BaseCommand):
    help = "making seed for Facilities"

    """ def add_arguments(self, parser):
        parser.add_argument(
            "--times",
            help="thank you Money",
        ) """

    # BaseCommand class 안의 function 인 add_arguments 를 사용해 우리가 필요한 arguments를 추가할 수 있다.
    # NotImplementedError: subclasses of BaseCommand must provide a handle() method
    # => add handle(self, *args, **option)

    def handle(self, *args, **options):
        facilities = [
            "Private entrance",
            "Paid parking on premises",
            "Paid parking off premises",
            "Elevator",
            "Parking",
            "Gym",
            "Swim Pool",
        ]
        for f in facilities:
            Facility.objects.create(name=f)
        self.stdout.write(self.style.SUCCESS(f"{len(facilities)} Facilities created!!"))
