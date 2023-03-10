from pydantic import BaseModel, SecretStr


class User(BaseModel):
    id: int
    username: str
    password: SecretStr


class Transaction(BaseModel):
    id: str
    user: User
    value: int


t = Transaction(
    id='1234567890',
    user=User(
        id=42,
        username='JohnDoe',
        password='hashedpassword'
    ),
    value=9876543210,
)

# using a set:
print(t.model_dump(exclude={'user', 'value'}))

# using a dict:
print(t.model_dump(exclude={'user': {'username', 'password'}, 'value': True}))

print(t.model_dump(include={'id': True, 'user': {'id'}}))
