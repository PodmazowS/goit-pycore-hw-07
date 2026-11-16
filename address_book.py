from collections import UserDict
from datetime import datetime, timedelta, date

class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

class Birthday(Field):
    def __init__(self, value):
        try:
            parsed_date = datetime.strptime(value, "%d.%m.%Y")
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")
        
        if parsed_date > datetime.today():
            raise ValueError("Date cannot be in the future")
        
    
        super().__init__(parsed_date.date())
    

class Name(Field):
    def __init__(self, value: str):
        if not value.strip():
            raise ValueError("Please enter your name")

        super().__init__(value)
        
class Phone(Field):
    def __init__(self, value: str):
        if not value.isdigit() or len(value) != 10:
            raise ValueError("Please enter correct phone number")
        
        super().__init__(value)

        
class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    def add_phone(self, phone: str):
        for p in self.phones:
            if p.value == phone:
                raise ValueError("This phone number is already added for this record")
        
        self.phones.append(Phone(phone))

    def find_phone(self, phone):
        for p in self.phones:
            if p.value == phone:
                return p
        return None

    def remove_phone(self, phone):
        phone_obj = self.find_phone(phone)
        
        if not phone_obj:
            raise ValueError("Phone is not found")
        
        self.phones.remove(phone_obj)
    
    def edit_phone(self, old_phone, new_phone):
        phone_obj = self.find_phone(old_phone)
        
        if not phone_obj:
            raise ValueError("Phone is not found")
        
        phone_obj.value = Phone(new_phone).value
    
    def add_birthday(self, birthday):
            self.birthday = Birthday(birthday)

    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}, birthday: {self.birthday}"


class AddressBook(UserDict):
    
    def add_record(self, record: Record):
        self.data[record.name.value] = record
    
    def find(self, name: str):
        return self.data.get(name)
    
    def delete(self, name: str):
        del self.data[name]
        
    def get_upcoming_birthdays(self):
        current_date = date.today()
        new_list = []
        

        for record, info in self.data.items():
            persons_birthday = info.birthday.value
            
            birthday_this_year = persons_birthday.replace(year=current_date.year)
            
            #Checking if birthday already passed

            if birthday_this_year < current_date:
                birthday_this_year = birthday_this_year.replace(year=current_date.year+1)
            
            #Here we are calcucating the difference between current date and birthday date this year
            difference = birthday_this_year - current_date
            days_until = difference.days


            #Here we are checking if birthday is in range of 7 days
            if days_until in range(0,7):
                if birthday_this_year.weekday() == 5 :
                    birthday_this_year = birthday_this_year + timedelta(days=2)
                elif birthday_this_year.weekday() == 6:
                    birthday_this_year = birthday_this_year + timedelta(days=1)


                dict_for_congrats = {"name": info.name.value,
                                    "congratulation_date": birthday_this_year.strftime("%Y.%m.%d")}

                new_list.append(dict_for_congrats) ## appending list with a dictionarries with the name and date to congrat
        
        return new_list

            
            
            