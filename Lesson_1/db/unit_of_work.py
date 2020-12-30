import sqlite3
import threading

connection = sqlite3.connect('db.sqlite')


class RecordNotFoundException(Exception):
    def __init__(self, message):
        super().__init__(f'Record not found: {message}')


class DbCommitException(Exception):
    def __init__(self, message):
        super().__init__(f'DB commit error: {message}')


class DbUpdateException(Exception):
    def __init__(self, message):
        super().__init__(f'DB update error: {message}')


class DbDeleteException(Exception):
    def __init__(self, message):
        super().__init__(f'DB delete error: {message}')


class PersonMapper:

    def __init__(self, connection):
        self.connection = connection
        self.cursor = connection.cursor()

    def find_by_id(self, id):
        statement = f'SELECT IDPERSON, FIRSTNAME, LASTNAME FROM PERSON WHERE IDPERSON="{id}"'
        self.cursor.execute(statement)
        result = self.cursor.fetchall()
        if result:
            return Person(*result[0])
        else:
            raise RecordNotFoundException(f'record with id={id} not found')

    def insert(self, person):
        statement = f'INSERT INTO PERSON (FIRSTNAME, LASTNAME) VALUES("{person.first_name}", "{person.last_name}")'
        self.cursor.execute(statement)
        try:
            self.connection.commit()
        except Exception as e:
            raise DbCommitException(e.args)

    def update(self, person):
        statement = f'UPDATE PERSON SET FIRSTNAME="{person.first_name}", LASTNAME="{person.last_name}" \
                      WHERE IDPERSON="{person.id_person}"'
        self.cursor.execute(statement)
        try:
            self.connection.commit()
        except Exception as e:
            raise DbCommitException(e.args)

    def delete(self, person):
        statement = f'DELETE FROM PERSON WHERE IDPERSON="{person.id_person}"'
        self.cursor.execute(statement)
        try:
            self.connection.commit()
        except Exception as e:
            raise DbCommitException(e.args)


class MapperRegistry:
    @staticmethod
    def get_mapper(obj):
        if isinstance(obj, Person):
            return PersonMapper(connection)
        if isinstance(obj, Category):
            return CategoryMapper(connection)


class UnitOfWork:

    current = threading.local()

    def __init__(self):
        self.new_objects = []
        self.dirty_objects = []
        self.remove_objects = []

    def register_new(self, obj):
        self.new_objects.append(obj)

    def register_dirty(self, obj):
        self.dirty_objects.append(obj)

    def register_remove(self, obj):
        self.remove_objects.append(obj)

    def insert_new(self):
        for obj in self.new_objects:
            MapperRegistry.get_mapper(obj).insert(obj)

    def update_dirty(self):
        for obj in self.dirty_objects:
            MapperRegistry.get_mapper(obj).update(obj)

    def delete_removed(self):
        for obj in self.remove_objects:
            MapperRegistry.get_mapper(obj).delete(obj)

    def commit(self):
        self.insert_new()
        self.update_dirty()
        self.delete_removed()

    @staticmethod
    def new_current():
        __class__.set_current(UnitOfWork)

    @classmethod
    def set_current(cls, unit_of_work):
        cls.current.unit_of_work = unit_of_work

    @classmethod
    def get_current(cls):
        return cls.current.unit_of_work


class DomainObject:
    def mark_new(self):
        UnitOfWork.get_current().register_new(self)

    def mark_dirty(self):
        UnitOfWork.get_current().register_dirty(self)

    def mark_removed(self):
        UnitOfWork.get_current().register_removed(self)


class Person(DomainObject):
    def __init__(self, id_person, first_name, last_name):
        self.id_person = id_person
        self.first_name = first_name
        self.last_name = last_name


class Category(DomainObject):
    def __init__(self, name):
        self.name = name


class CategoryMapper:
    def __init__(self, connection):
        self.connection = connection
        self.cursor = connection.cursor()

    def find_by_id(self, id):
        statement = f'SELECT ID, NAME FROM CATEGORY WHERE ID="{id}"'
        self.cursor.execute(statement)
        result = self.cursor.fetchall()
        if result:
            return Category(*result[0])
        else:
            raise RecordNotFoundException(f'record with id={id} not found')

    def insert(self, category):
        statement = f'INSERT INTO CATEGORY (NAME) VALUES("{category.name}")'
        self.cursor.execute(statement)
        try:
            self.connection.commit()
        except Exception as e:
            raise DbCommitException(e.args)

    def update(self, category):
        statement = f'UPDATE CATEGORY SET NAME="{category.name}" WHERE ID="{category.id}"'
        self.cursor.execute(statement)
        try:
            self.connection.commit()
        except Exception as e:
            raise DbCommitException(e.args)

    def delete(self, category):
        statement = f'DELETE FROM CATEGORY WHERE ID="{category.id}"'
        self.cursor.execute(statement)
        try:
            self.connection.commit()
        except Exception as e:
            raise DbCommitException(e.args)
