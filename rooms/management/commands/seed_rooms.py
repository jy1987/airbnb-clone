import random
from django.core.management.base import BaseCommand
from django.contrib.admin.utils import flatten
from django_seed import Seed
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
        all_users = user_models.User.objects.all()
        room_types = room_models.RoomType.objects.all()
        print(all_users, room_types)
        seeder.add_entity(
            room_models.Room,
            int(number),
            {
                "name": lambda x: seeder.faker.address(),
                "host": lambda x: random.choice(all_users),
                "room_type": lambda x: random.choice(room_types),
                "guests": lambda x: random.randint(1, 10),
                "price": lambda x: random.randint(1, 500),
                "beds": lambda x: random.randint(1, 10),
                "bedrooms": lambda x: random.randint(1, 10),
                "baths": lambda x: random.randint(1, 10),
            },
        )
        created_photos = (
            seeder.execute()
        )  # room_models.Room 에 default 값만큼 배정 => dict 형태를 가짐
        print(created_photos)  # {<class 'rooms.models.Room'>: [43, 44]}
        print((created_photos.values()))  # dict_values([[43,44]])
        created_clean = flatten(
            list(created_photos.values())
        )  # flatten return list which is single level
        amenities = room_models.Amenity.objects.all()
        facilities = room_models.Facility.objects.all()
        rules = room_models.HouseRule.objects.all()
        print(created_clean)
        for pk in created_clean:
            room = room_models.Room.objects.get(pk=pk)
            print(room)
            for i in range(1, random.randint(5, 10)):
                room_models.Photo.objects.create(
                    caption=seeder.faker.sentence(),
                    room=room,
                    file=f"room_photos/{random.randint(1,14)}.jpg",
                )

            for a in amenities:
                get_number = random.randint(0, 3)
                if get_number % 2 == 0:
                    room.amenities.add(a)
            for f in facilities:
                get_number = random.randint(0, 3)
                if get_number % 2 == 0:
                    room.facilities.add(f)
            for r in rules:
                get_number = random.randint(0, 3)
                if get_number % 2 == 0:
                    room.house_rules.add(r)  # manytomany 만드는 방법

        self.stdout.write(self.style.SUCCESS(f"{number} rooms made"))
