from typing import TypedDict

class Person(TypedDict):
    name: str
    age: int
    email: str

new_person : Person = {
    "name": "John Doe",
    "age": 30,
    "email": "john.doe@example.com"
}

print(new_person)