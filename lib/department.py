# from __init__ import CURSOR, CONN


# class Department:

#     def __init__(self, name, location, id=None):
#         self.id = id
#         self.name = name
#         self.location = location

#     def __repr__(self):
#         return f"<Department {self.id}: {self.name}, {self.location}>"
from __init__ import CURSOR, CONN


class Department:

    def __init__(self, name, location, id=None):
        self.id = id
        self.name = name
        self.location = location

    def __repr__(self):
        return f"<Department {self.id}: {self.name}, {self.location}>"

    @classmethod
    def create_table(cls):
        """Creates the 'departments' table if it does not exist."""
        query = """
        CREATE TABLE IF NOT EXISTS departments (
            id SERIAL PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            location VARCHAR(255) NOT NULL
        )
        """
        CURSOR.execute(query)
        CONN.commit()

    @classmethod
    def drop_table(cls):
        """Drops the 'departments' table if it exists."""
        query = """
        DROP TABLE IF EXISTS departments
        """
        CURSOR.execute(query)
        CONN.commit()

    def save(self):
        """Saves the Department instance to the database and assigns it an ID."""
        if self.id is None:
            query = """
            INSERT INTO departments (name, location)
            VALUES (?, ?)
            RETURNING id
            """
            CURSOR.execute(query, (self.name, self.location))
            self.id = CURSOR.fetchone()[0]
        else:
            query = """
            UPDATE departments
            SET name = ?, location = ?
            WHERE id = ?
            """
            CURSOR.execute(query, (self.name, self.location, self.id))
        CONN.commit()

    @classmethod
    def create(cls, name, location):
        """Creates a new row in the db using parameter data and returns a Department instance."""
        department = cls(name, location)
        department.save()
        return department

    def update(self):
        """Updates an instance's corresponding db row to match its new attribute values."""
        self.save()

    def delete(self):
        """Deletes the instance's corresponding db row."""
        if self.id is not None:
            query = """
            DELETE FROM departments
            WHERE id = ?
            """
            CURSOR.execute(query, (self.id,))
            CONN.commit()
