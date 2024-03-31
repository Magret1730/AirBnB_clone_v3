#!/usr/bin/python3
"""
Contains the TestDBStorageDocs and TestDBStorage classes
"""

from datetime import datetime
import inspect
import models
from models.engine import db_storage
from models.amenity import Amenity
from models.base_model import BaseModel
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
import json
import os
import pep8
import unittest
DBStorage = db_storage.DBStorage
classes = {"Amenity": Amenity, "City": City, "Place": Place,
           "Review": Review, "State": State, "User": User}


class TestDBStorageDocs(unittest.TestCase):
    """Tests to check the documentation and style of DBStorage class"""
    @classmethod
    def setUpClass(cls):
        """Set up for the doc tests"""
        cls.dbs_f = inspect.getmembers(DBStorage, inspect.isfunction)

    def test_pep8_conformance_db_storage(self):
        """Test that models/engine/db_storage.py conforms to PEP8."""
        pep8s = pep8.StyleGuide(quiet=True)
        result = pep8s.check_files(['models/engine/db_storage.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_pep8_conformance_test_db_storage(self):
        """Test tests/test_models/test_db_storage.py conforms to PEP8."""
        pep8s = pep8.StyleGuide(quiet=True)
        result = pep8s.check_files(['tests/test_models/test_engine/\
test_db_storage.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_db_storage_module_docstring(self):
        """Test for the db_storage.py module docstring"""
        self.assertIsNot(db_storage.__doc__, None,
                         "db_storage.py needs a docstring")
        self.assertTrue(len(db_storage.__doc__) >= 1,
                        "db_storage.py needs a docstring")

    def test_db_storage_class_docstring(self):
        """Test for the DBStorage class docstring"""
        self.assertIsNot(DBStorage.__doc__, None,
                         "DBStorage class needs a docstring")
        self.assertTrue(len(DBStorage.__doc__) >= 1,
                        "DBStorage class needs a docstring")

    def test_dbs_func_docstrings(self):
        """Test for the presence of docstrings in DBStorage methods"""
        for func in self.dbs_f:
            self.assertIsNot(func[1].__doc__, None,
                             "{:s} method needs a docstring".format(func[0]))
            self.assertTrue(len(func[1].__doc__) >= 1,
                            "{:s} method needs a docstring".format(func[0]))


class TestDBStorageGetCount(unittest.TestCase):
    """Tests for get and count methods of the DBStorage class."""
    def test_get_method(self):
        """Get method test"""
        # Create initial state objects for testing
        new_state1 = State(name="California")
        new_state2 = State(name="New York")
        models.storage.new(new_state1)
        models.storage.new(new_state2)
        models.storage.save()

        # Retrieve the first state object if available
        state = None
        states = list(models.storage.all("State").values())
        if states:
            first_state = states[0]
            first_state_id = first_state.id  # [0]
            state = models.storage.get(State, first_state_id)
            self.assertIsNotNone(state)
        if state:
            self.assertEqual(state.id, first_state_id)
        # Test for non-existent id
        self.assertIsNone(models.storage.get(State, "8888888"))

    def test_count_method(self):
        """Count method test """
        previous_count = models.storage.count()
        new_state = State(name="Test_State")
        models.storage.new(new_state)
        models.storage.save()
        self.assertEqual(models.storage.count(), previous_count + 1)
        # Test count with class name
        self.assertLessEqual(models.storage.count(State), previous_count + 1)
        # Cleanup
        models.storage.delete(new_state)
        models.storage.save()


class TestFileStorage(unittest.TestCase):
    """Test the FileStorage class"""
    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_all_returns_dict(self):
        """Test that all returns a dictionaty"""
        self.assertIs(type(models.storage.all()), dict)

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_all_no_class(self):
        """Test that all returns all rows when no class is passed"""
        # Create some objects in the database
        state1 = State(name="State 1")
        state2 = State(name="State 2")
        models.storage.new(state1)
        models.storage.new(state2)
        models.storage.save()

        # Test all method without passing a class
        all_objects = models.storage.all()

        # Assert that all objects are returned
        self.assertIn(state1, all_objects.values())
        self.assertIn(state2, all_objects.values())

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_new(self):
        """test that new adds an object to the database"""
        # Create a new object and add it to the database
        state = State(name="New State")
        models.storage.new(state)
        models.storage.save()

        # Retrieve the object from the database
        retrieved_state = models.storage.get(State, state.id)

        # Assert that the retrieved object is not None
        self.assertIsNotNone(retrieved_state)
        # Assert that the retrieved object matches the added object
        self.assertEqual(state, retrieved_state)

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_save(self):
        """Test that save properly saves objects to file.json"""
        # Create a new object and add it to the database
        state = State(name="State")
        models.storage.new(state)
        models.storage.save()

        # Modify the object's attributes
        state.name = "Modified State"
        models.storage.save()

        # Retrieve the object from the database
        retrieved_state = models.storage.get(State, state.id)

        # Assert that the retrieved object matches the modified object
        self.assertEqual(state.name, retrieved_state.name)
