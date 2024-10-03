from objects.book import Book
from objects.queue_item import QueueItem
from objects.taken_by_item import TakenByItem

class BooksCatalogue:
    def __init__(self):
        self.catalogue : list[Book] = []
        
    def append(self, book : list):
        self.catalogue.append(Book(book[0], book[1], book[2], book[3], book[4], book[5]))

    def set_queue(self, queue : list[tuple]):
        if len(queue) == 0 : return
        for queue_item in queue:
            qi = QueueItem(queue_item[0], queue_item[1], queue_item[2], queue_item[3])
            book = [book for book in self.catalogue if book.id == qi.book_id][0]
            book.queue.append(qi)
            #self.catalogue[qi.book_id - 1].queue.append(qi)

    def set_taken_by(self, taken_by : list[tuple]):
        if len(taken_by) == 0 : return
        for taken_by_item in taken_by:
            tbi = TakenByItem(taken_by_item[0], taken_by_item[1], taken_by_item[2], taken_by_item[3])
            book = [book for book in self.catalogue if book.id == tbi.book_id][0]
            book.taken_by.append(tbi)
            #self.catalogue[tbi.book_id - 1].taken_by.append(tbi)

    def print(self):
        for book in self.catalogue:
            print(f"{book.id} {book.name} {book.author} {book.year}" +
                  f"\nQueue: {''.join(book.queue.__str__())}" +
                  f"\nTaken by: {''.join(book.taken_by.__str__())}")

    