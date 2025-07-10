from fields import Name, Phone, Birthday
from decorators import input_error

class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    def __str__(self):
        phones_str = '; '.join(p.value for p in self.phones)
        birthday_str = f", birthday: {self.birthday.value.strftime('%d.%m.%Y')}" if self.birthday else ""
        return f"Contact name: {self.name.value}, phones: {phones_str}{birthday_str}"
    
    @input_error
    def add_phone(self, phone_number):
        phone = Phone(phone_number)

        if phone.value not in [p.value for p in self.phones]:
            self.phones.append(phone)
            return f'Phone number {phone_number} added for {self.name.value}'
        else:
            return f'Phone number {phone_number} already exist for {self.name.value}'

    @input_error
    def remove_phone(self, phone_number):
        phone_obj = Phone(phone_number)
        phone_for_deleting_value = phone_obj.value

        phone_list_len = len(self.phones)
        self.phones = [phone for phone in self.phones if phone.value != phone_for_deleting_value]
        if len(self.phones) == phone_list_len:
            return f"Phone number {phone_number} not found for {self.name.value}"
        else:
            return f"Phone number {phone_number} removed for {self.name.value}"
    
    @input_error
    def edit_phone(self, old_phone, new_phone):
        old_phone_obj = Phone(old_phone)
        new_phone_obj = Phone(new_phone)

        is_found = False
        for index, phone in enumerate(self.phones):
            if phone.value == old_phone_obj.value:
                self.phones[index] = new_phone_obj
                is_found = True
                return f"Phone number {old_phone_obj.value} updated to {new_phone_obj.value} for {self.name.value}"
        if not is_found:
            return f"Phone number {old_phone_obj.value} not found for {self.name.value}"
    
    @input_error
    def add_birthday(self, birthday_str):
        message = f'Birthday date {birthday_str} added for {self.name.value}'
        if self.birthday:
            message = f'Birthday date {birthday_str} updated for {self.name.value}'
        
        self.birthday = Birthday(birthday_str)
        return message

    @input_error
    def show_birthday(self):
        if self.birthday:
            return self.birthday.value.strftime('%d.%m.%Y')
        return "Birthday not set for this contact."    