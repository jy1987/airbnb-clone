from django.utils import timezone
import calendar


class Day:
    def __init__(self, number, number2, past, month, year):
        self.number = number
        self.number2 = number2
        self.month = month
        self.year = year
        self.past = past

    def __str__(self):
        return str(self.number)


class Calendar(calendar.Calendar):
    def __init__(self, year, month):
        super().__init__(firstweekday=6)

        self.year = year
        self.month = month
        self.day_names = ("Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat")
        self.months = (
            "January",
            "February",
            "March",
            "April",
            "May",
            "June",
            "July",
            "August",
            "September",
            "October",
            "November",
            "December",
        )

    def get_days(self):

        weeks = self.monthdays2calendar(self.year, self.month)
        # monthdays2calendar(self.year, self.month) => [[(),(),()....],[(),(),()....],[(),(),()....]] 이런식
        days = []

        for week in weeks:
            for day in week:
                print(day[0], day[1])
                now = timezone.now()
                today = now.day
                now_month = now.month
                past = False
                if now_month >= self.month and day[0] <= today:
                    past = True
                new_day = Day(day[0], day[1], past, month=self.month, year=self.year)
                #  Day(day[0], day[1], past, month=self.month, year=self.year) 각각의 인자를 가지고 있는 상태.
                days.append(new_day)
        print(days)
        return days

    def get_month(self):
        return self.months[self.month - 1]
