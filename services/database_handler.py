import psycopg as pco
import base64
import datetime as dt
from typing import Literal
from objects.books_catalogue import BooksCatalogue
from objects.user import User

class DatabaseHandler:

    def __init__(self):
        self.connection_parametrs = {
            #Deleted
        }

    # ? All should work, in theory without bugs, now users logic must be added
    def get_books(self, user_id : int = 0, taken_or_queue : Literal["taken", "queue"] = "queue"):
        result = BooksCatalogue()
        table = "books"
        order_by = "id"

        if user_id != 0:
            if taken_or_queue == "taken":
                table = f"get_books_taken_by_user({user_id})"
            else:
                table = f"get_books_user_in_queue({user_id})"
            order_by = "book_id"

        books = self.select_data(table, "*", [], [], order_by_col=order_by)

        for book in books:
            result.append(list(book))
            if taken_or_queue != "taken":
                queue_for_book = self.select_data("queue", "*", ["book_id"], [book[0]], order_by_col="priority")
                result.set_queue(queue_for_book)
            if user_id == 0 or taken_or_queue == "taken":    
                taken_by_for_book = self.select_data("taken_by", "*", ["book_id"], [book[0]])
                result.set_taken_by(taken_by_for_book)

        return result
     
    def get_users(self):
        users_list = self.select_data("users", ["*"], [], [], order_by_col="id")
        return [User(user[0], self.decode(user[1]), user[2], user[3], user[4]) for user in users_list]

    def add_book(self, name : str, author : str, year : str, description : str, quantity : int):
        return self.insert_data("books", ["name", "author", "year", "short_desc", "quantity"],
                         (name, author, year, description, quantity), "books_id_seq")

    def take_book(self, user_id : int, book_id : int):
        return self.call_function("take_book", [str(book_id), str(user_id)])

    def return_book(self, user_id : int, book_id : int):
        self.call_function("return_book", [str(book_id), str(user_id)])

    def delete_from_queue(self, user_id : int, book_id : int):
        self.call_function("delete_from_queue", [str(book_id), str(user_id)])

    def sign_up(self, nickname : str, password : str, email : str, phone : str):
        return self.insert_data("users", ["login", "password", "phone_number", "email"],
                        (self.encode(nickname), self.encode(password), phone, email), "users_id_seq")
    
    def check_authorization(self, login : str, password : str):
        result = self.select_data("users", ["*"],
                                ["login", "password"], [self.encode(login), self.encode(password)])
        if len(result) == 0:
            return False
        result = list(result[0])
        result[1], result[2] = self.decode(result[1]), self.decode(result[2])
        return User(result[0], result[1], result[2], result[3], result[4])

    def get_in_line(self, user_id : int, book_id : int, priority : int, expiry_date : dt.date):
        return self.insert_data("queue", ["user_id", "book_id", "priority", "expiry_date"],
                         (user_id, book_id, priority, expiry_date))

    def insert_data(self, table_name : str, columns : list, values : tuple, constraint=""):
        constraint_value = 0
        try:
            with pco.connect(**self.connection_parametrs) as conn:
                if not self.is_connection_active(conn): return "Error"
                with conn.cursor() as cursor:
                    if constraint != "":
                        constraint_value = self.get_constraint(constraint, cursor)  
                        self.set_constraint(constraint, constraint_value - 1)      
                    command_text = f"INSERT INTO {table_name} ({', '.join(columns)}) VALUES ({('%s, '*len(columns)).removesuffix(', ')})"
                    cursor.execute(command_text, values)                             
                print("Success")       
            return "Success"
        except pco.DatabaseError as e:         
            if constraint != "": self.set_constraint(constraint, constraint_value - 1)
            print(f"Error: {e}")
            return "Error"
        
    def select_data(self, table_name : str, columns : list, where_cols : list,
                    where_vals : list, and_or : str = "AND", order_by_col : str = "", asc_desc : str = "ASC"):
        rows = {}
        with pco.connect(**self.connection_parametrs) as conn:
            if not self.is_connection_active(conn): return "Error"
            with conn.cursor() as cursor:
                command_text = f"SELECT {', '.join(columns)} FROM {table_name} WHERE"
                if len(where_cols) != 0:
                    for i in range(0, len(where_cols)):
                        command_text += f" {where_cols[i]} = '{where_vals[i]}' {and_or}"
                    command_text = command_text.removesuffix(f" {and_or}")
                else:
                    command_text = command_text.removesuffix("WHERE")

                if order_by_col != "":
                    command_text += f"ORDER BY {order_by_col} {asc_desc}"

                cursor.execute(command_text)  
                rows = cursor.fetchall()    

        return rows

    def call_function(self, func_name : str, params : list[str]):
        try:
            with pco.connect(**self.connection_parametrs) as conn:
                if not self.is_connection_active(conn): return "Error"
                with conn.cursor() as cursor:     
                    cursor.execute(f"SELECT {func_name}({', '.join(params)})")  
            return "Success" 
        except pco.DatabaseError as e:
            print(f"Error while calling function: {e}")
            return "Error"

    def get_constraint(self, constraint, cursor):
        cursor.execute(f"SELECT nextval('{constraint}')")
        return cursor.fetchall()[0][0]

    def set_constraint(self, constraint, value):
        with pco.connect(**self.connection_parametrs) as conn:
            if not self.is_connection_active(conn): return "Error"
            with conn.cursor() as cursor:
                cursor.execute(f"SELECT setval('{constraint}', {value});")
    
    def is_connection_active(self, connection):
        if connection.closed == True:
            return False
        return True

    def encode(self, input : str):
        return base64.b64encode(input.encode('utf-8')).decode('utf-8')
    
    def decode(self, input : str):
        return base64.b64decode(input).decode('utf-8')
    