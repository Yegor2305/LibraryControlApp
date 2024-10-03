from dataclasses import dataclass
from datetime import date

@dataclass
class QueueItem:
    book_id : int
    user_id : int
    priority : int
    expiry_date : date

    def __str__(self):
        return f"{self.book_id} {self.user_id} {self.priority} {self.expiry_date}"
