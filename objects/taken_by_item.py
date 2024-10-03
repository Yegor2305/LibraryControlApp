from dataclasses import dataclass
from datetime import date

@dataclass
class TakenByItem:
    book_id : int
    user_id : int
    start_date : date
    expiry_date : date