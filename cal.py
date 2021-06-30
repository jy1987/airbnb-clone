import calendar


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
                days.append(day)
        print(days)
        return days

    def get_month(self):
        return self.months[self.month - 1]