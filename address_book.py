from collections import UserDict
from datetime import datetime, timedelta
from records import Record

class AddressBook(UserDict):
    def add_record(self, record: Record):
        self.data[record.name.value] = record
    
    def find(self, name):
        record = self.data.get(name)
        return record
    
    def delete(self, name):
        if name in self.data:
            del self.data[name]
            return f"Contact {name} deleted"
        else:
            raise KeyError

    def get_upcoming_birthdays(self):
        upcoming_birthdays = []
        today = datetime.today().date()

        for record in self.data.values():
            if record.birthday and record.birthday.value:
                bday_date = record.birthday.value
                bday_this_year = bday_date.replace(year=today.year)

                if bday_this_year < today:
                    bday_this_year = bday_date.replace(year=today.year + 1)

                bday_difference = (bday_this_year - today).days

                if 0 <= bday_difference <= 7:
                    bday_day_of_week = bday_this_year.weekday()

                    if bday_day_of_week == 5:
                        bday_this_year += timedelta(days=2)
                    elif bday_day_of_week == 6:
                        bday_this_year += timedelta(days=1)
                    
                if (bday_this_year - today).days <= 7:
                    upcoming_birthdays.append({
                        "name": record.name.value,
                        "congratulation_date": bday_this_year.strftime('%d.%m.%Y')
                    })    

        return upcoming_birthdays