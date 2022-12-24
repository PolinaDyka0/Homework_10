from collections import UserDict


class AddressBook(UserDict):
    def __init__(self, data={}):
        self.data = data

    def __repr__(self):
        return '\n'.join(f'{record.name}: {record.phones}' for record in self.data.values())

    def add_record(self, record):
        self.data[record.name.value] = record


class Record:
    def __init__(self, name, phones=[]):
        self.name = name
        self.phones = phones

    def add_phone(self, phone):
        self.phones.append(phone)

    def delete_phone(self, phone):
        self.phones.remove(phone)

    def change_phone(self, old_phone, new_phone):
        self.phones = list(map(lambda x: x.replace(
            old_phone, new_phone), self.phones))


class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return self.value

    def __repr__(self):
        return self.value


class Name(Field):
    pass


class Phone(Field):
    pass


bool_var = True
address_book = AddressBook({'name': Record(Name('name'), [Phone('phone_number')]),
                            'Polina': Record(Name('Polina'), [Phone('0962154928')])})


def input_error(func):
    def inner_function(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except IndexError:
            if func.__name__ == 'add' or func.__name__ == 'change':
                return "Give me name and phone please"
            if func.__name__ == 'phone':
                return "Give me name for finding phone"
            else:
                return 'IndexError'
        except KeyError:
            if func.__name__ == 'phone':
                return 'No such phone'
            return "No such command"
        except ValueError:
            return 'There no such name'
    return inner_function


def split_command_line(inp):
    if inp == 'show all' or inp == 'good bye':
        return [inp]
    return inp.split(' ')


@input_error
def hello():
    return 'How can I help you?'


@input_error
def add(inp):
    record = address_book.data.get(inp[0])
    if record == None:
        record = Record(Name(inp[0]), [Phone(inp[1])])
        address_book.add_record(record)
    else:
        record.add_phone(Phone(inp[1]))
    return 'DONE!'


@input_error
def change(inp):
    record = address_book.data.get(inp[0])
    if record != None:
        record.phones = [Phone(inp[1])]
    else:
        raise ValueError
    return 'DONE!'


@ input_error
def phone(inp):
    return (address_book.data[inp[0]]).phones


@ input_error
def show_all():
    return address_book


@ input_error
def close():
    global bool_var
    bool_var = False
    return 'Good bye!'


@input_error
def handler(name, arguments):
    def add_func():
        return add(arguments)

    def change_func():
        return change(arguments)

    def phone_func():
        return phone(arguments)

    commands = {'hello': hello,
                'add': add_func,
                'change': change_func,
                'phone': phone_func,
                'show all': show_all,
                'close': close,
                'exit': close,
                'good bye': close,
                '.': close}

    return commands[name]


def main():
    while bool_var:
        inp = input('Type:\n')
        command, *arguments = split_command_line(inp)
        operation = handler(command.lower(), arguments)
        if isinstance(operation, str):
            print(operation)
        else:
            print(operation())


if __name__ == "__main__":
    main()
