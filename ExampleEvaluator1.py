import sqlite3
import os
from simInfo.Evaluation import Decision_Evaluation
from simModel.Replay import ReplayModel

# Define the path to the database file
db_path = 'C:\\Users\\results\\2024-01-22_17-27-41.db'

def main():
    # Check if the database file exists
    if not os.path.exists(db_path):
        print(f"Database file does not exist: {db_path}")
        return

    # Perform database operations
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Example of querying the database
    try:
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        print("Tables in the database:")
        for table in tables:
            print(table[0])

        # Perform a query on the simINFO table
        cursor.execute("SELECT * FROM simINFO LIMIT 5;")
        rows = cursor.fetchall()
        print("Data from simINFO:")
        for row in rows:
            print(row)
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
    finally:
        # Close the database connection
        conn.close()

    # Run Replay and Evaluation
    database = './results/2024-01-7_16-17-41.db'
    model = ReplayModel(database)
    evaluator = Decision_Evaluation(database, model.timeStep)
    while not model.tpEnd:
        model.runStep()
        evaluator.Evaluate(model)

if __name__ == "__main__":
    main()
