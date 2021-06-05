import random
from django.core.management.base import BaseCommand
from django_seed import Seed
from reviews import models as review_models
from rooms import models as room_models
from users import models as user_models


class Command(BaseCommand):
    help = "making seed for Rooms"

    def add_arguments(self, parser):
        parser.add_argument("--number", default=2, help="thank you Money")

    # --arguments 형식임
    # BaseCommand class 안의 function 인 add_arguments 를 사용해 우리가 필요한 arguments를 추가할 수 있다.
    # NotImplementedError: subclasses of BaseCommand must provide a handle() method
    # => add handle(self, *args, **option)

    def handle(self, *args, **options):
        number = options.get("number")
        seeder = Seed.seeder()
        users = user_models.User.objects.all()
        rooms = room_models.Room.objects.all()
        print(users, rooms)
        seeder.add_entity(
            review_models.Review,
            int(number),
            {
                "accuracy": lambda x: random.randint(1, 5),
                "communication": lambda x: random.randint(1, 5),
                "cleanliness": lambda x: random.randint(1, 5),
                "location": lambda x: random.randint(1, 5),
                "check_in": lambda x: random.randint(1, 5),
                "value": lambda x: random.randint(1, 5),
                "room": lambda x: random.choice(rooms),
                "user": lambda x: random.choice(users),
            },
        )

        seeder.execute()

        self.stdout.write(self.style.SUCCESS(f"{number} reviews made"))
