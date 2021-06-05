import random
from datetime import datetime, timedelta
from django.core.management.base import BaseCommand
from django.contrib.admin.utils import flatten
from django_seed import Seed
from reservations import models as reservation_models
from rooms import models as room_models
from users import models as user_models


class Command(BaseCommand):
    help = "making seed for Reservations"

    def add_arguments(self, parser):
        parser.add_argument("--number", default=2, help="thank you Money")

    def handle(self, *args, **options):
        number = options.get("number")
        seeder = Seed.seeder()
        users = user_models.User.objects.all()
        rooms = room_models.Room.objects.all()
        print(users, rooms)
        seeder.add_entity(
            reservation_models.Reservation,
            int(number),
            {
                "guest": lambda x: random.choice(users),
                "room": lambda x: random.choice(rooms),
                "status": lambda x: random.choice(["pending", "confirmed", "canceled"]),
                "check_in": lambda x: datetime.now(),
                "check_out": lambda x: datetime.now()
                + timedelta(days=random.randint(3, 10)),
            },
        )

        seeder.execute()

        self.stdout.write(self.style.SUCCESS(f"{number} reservations made"))
