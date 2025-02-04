from sqlite3 import connect
from pathlib import Path
from functools import wraps
import pandas as pd

# Using pathlib, create a `db_path` variable
# that points to the absolute path for the `employee_events.db` file
#### YOUR CODE HERE
db_path = Path(__file__).parent / "employee_events.db"
db_path = db_path.resolve()  # Get the absolute path


# OPTION 1: MIXIN
# Define a class called `QueryMixin`
class QueryMixin:
    
    # Define a method named `pandas_query`
    # that receives an sql query as a string
    # and returns the query's result
    # as a pandas dataframe
    #### YOUR CODE HERE
    def connect(self):
        return sqlite3.connect(db_path)
    
    def pandas_query(self, sql_query):
        try:
            connection = self.connect()
            df = pd.read_sql_query(sql_query, connection)
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            df = pd.DataFrame() # Return empty DataFrame in case of error
        finally:
            if connection:
                connection.close()
        return df


    # Define a method named `query`
    # that receives an sql_query as a string
    # and returns the query's result as
    # a list of tuples. (You will need
    # to use an sqlite3 cursor)
    #### YOUR CODE HERE
    def query(self, sql_query):
        try:
            connection = self.connect()
            cursor = connection.cursor()
            cursor.execute(sql_query)
            result = cursor.fetchall()
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            result = []
        finally:
            if connection:
                connection.close()
        return result
    

 
 # Leave this code unchanged
def query(func):
    """
    Decorator that runs a standard sql execution
    and returns a list of tuples
    """

    @wraps(func)
    def run_query(*args, **kwargs):
        query_string = func(*args, **kwargs)
        connection = connect(db_path)
        cursor = connection.cursor()
        result = cursor.execute(query_string).fetchall()
        connection.close()
        return result
    
    return run_query
