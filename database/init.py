# __init__.py

from your_module_name.db import Database

def main():
    db = Database()
    db.create_tables()
    db.close()

if __name__ == "__main__":
    main()
