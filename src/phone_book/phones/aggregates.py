import string
import typing
from pydantic.main import BaseModel
from pydantic import validator


class PhoneNumber:
    def __init__(self, value: typing.Any):
        self._value = self.prepare(value)

    def __repr__(self):
        return self._value

    def __str__(self):
        return str(self._value)

    def format(self):
        return '+' + str(self._value)

    @property
    def value(self) -> int:
        return self._value

    @classmethod
    def prepare(cls, value: typing.Any) -> int:
        value = str(value)
        value = ''.join(c for c in value if c not in string.ascii_letters)
        return int(value)


class Phone(BaseModel):
    id: typing.Optional[int]
    fullname: str
    address: str
    phone: int

    @validator('phone')
    def validate_phone(cls, value):
        return PhoneNumber(value).value

    class Config:
        arbitrary_types_allowed = True
