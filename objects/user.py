from dataclasses import dataclass

@dataclass
class User:
    id : int
    login: str
    password : str
    phone : str
    email : str
