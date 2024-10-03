from objects.queue_item import QueueItem
from objects.taken_by_item import TakenByItem

class Book:
    def __init__(self, id : int, name : str, author : str,
                year : int, description : str, quantity : int):
        self.id = id
        self.name = name
        self.author = author
        self.year = year
        self.description = description
        self.quantity = quantity
        self.queue : list[QueueItem] = []
        self.taken_by : list[TakenByItem] = []

