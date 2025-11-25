def sum(a: int, b: int) -> int:
    return a + b

print(sum(1, 2))
# change typing checking mode to standard in edit (cmd/ctl + ',')
# pylance will raise error:
# print(sum('1', '2'))

# variable: type
name: str = '123'
age: int = 25
price: float = 19.9
is_acive: bool = True
# print(sum('1', '2'))

tags: list[str]= ['lession', 'python', 'backend']
nums: list[int | str] = [1,2,3, 'user']

user_data: dict[str, str] = {"name": "john", "email": 'aaa@gmail.com'}

middle_name: str | None = 'None' 
# or using Optional
from typing import Optional
middle_name: Optional[str] = None

# for interviews, recommend not to use type:
# - not all python versions support
# - a lot online IDE not support
# - cost more time
    
from typing import Annotated, get_type_hints

class Range:
    def __init__(self, lo: int, hi: int):
        self.lo = lo
        self.hi = hi

# Annotate an int with a range
Age = Annotated[int, Range(0, 120)]

def set_age(age: Age):
    return age

# Get type hints including metadata
hints = get_type_hints(set_age, include_extras=True)
print(hints)  
# → {'age': typing.Annotated[int, Range(0, 120)]}

# Access metadata
annot = hints['age']
origin = getattr(annot, "__origin__", None)         # int
metadata = getattr(annot, "__metadata__", None)     # (Range(0, 120),)
print(origin, metadata)