import random
from django.core.management.base import BaseCommand
from django.contrib.admin.utils import flatten
from django_seed import Seed
from lists import models as list_models
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
            list_models.List,
            int(number),
            {
                "user": lambda x: random.choice(users),
            },
        )
        created_lists = (
            seeder.execute()
        )  # room_models.Room 에 default 값만큼 배정 => dict 형태를 가짐
        print(created_lists)  # {<class 'rooms.models.Room'>: [43, 44]}
        print((created_lists.values()))  # dict_values([[43,44]])
        created_clean = flatten(
            list(created_lists.values())
        )  # flatten return list which is single level
        for pk in created_clean:
            list_model = list_models.List.objects.get(pk=pk)
            to_add = rooms[random.randint(0, 5) : random.randint(6, 25)]
            print(to_add, *to_add)
            list_model.rooms.add(*to_add)
        self.stdout.write(self.style.SUCCESS(f"{number} lists made"))
