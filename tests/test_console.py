#!/usr/bin/python3
"""Unit test for console command interpreter
"""
import unittest
from unittest.mock import patch
import os
import json
from io import StringIO

import console
import tests
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review
from models.engine.file_storage import FileStorage


class TestConsole(unittest.TestCase):

    """ Definition of Unit test for command interpreter
    Functions:
        test_0_documentation(self)
        test_1_all(self)
        test_2_show(self)
        test_3_create(self)
        test_4_destroy(self)
        test_5_update(self)
        test_6_update(self)
    """
    err_msg1 = "** class name missing **\n"
    err_msg2 = "** class doesn't exist **\n"
    err_msg3 = "** instance id missing **\n"
    err_msg4 = "** no instance found **\n"

    @classmethod
    def setUpClass(cls):
        """Set up test
        """
        cls.cons = console.HBNBCommand()
        try:
            os.rename("file.json", "backup")
        except IOError:
            pass
        with open("file.json", "w+", encoding="utf-8") as f:
            cls.json_f = f.read()

    @classmethod
    def tearDownClass(cls):
        """Removes temporary file (file.json) created
        """
        os.remove("file.json")
        try:
            os.rename("backup", "file.json")
        except IOError:
            pass

    def test_0_documentation(self):
        """Test docstrings exist in console.py
        """
        self.assertTrue(len(console.__doc__) >= 1)

    def test_3_create(self):
        """Tests output for cmd "create"
        """
        with patch('sys.stdout', new=StringIO()) as f:
            self.cons.onecmd("create")
            self.assertEqual(self.err_msg1, f.getvalue())
        with patch('sys.stdout', new=StringIO()) as f:
            self.cons.onecmd("create SomeClass")
            self.assertEqual(self.err_msg2, f.getvalue())
        with patch('sys.stdout', new=StringIO()) as f:
            # creates instances for upcoming test
            self.cons.onecmd("create User")
            self.cons.onecmd("create User")
        with patch('sys.stdout', new=StringIO()) as f:
            self.cons.onecmd(self.cons.precmd("User.all()"))
            self.assertEqual('["[User]', f.getvalue()[:8])

    def test_1_all(self):
        """Tests output for cmd "all"
        """
        with patch('sys.stdout', new=StringIO()) as f:
            self.cons.onecmd("all NonExistantModel")
            self.assertEqual(self.err_msg2, f.getvalue())
        with patch('sys.stdout', new=StringIO()) as f:
            self.cons.onecmd("all Place")
            self.assertEqual("[]\n", f.getvalue())

    def test_4_destroy(self):
        """Tests output for cmd "destroy"
        """
        with patch('sys.stdout', new=StringIO()) as f:
            self.cons.onecmd("destroy")
            self.assertEqual(self.err_msg1, f.getvalue())
        with patch('sys.stdout', new=StringIO()) as f:
            self.cons.onecmd("destroy TheWorld")
            self.assertEqual(self.err_msg2, f.getvalue())
        with patch('sys.stdout', new=StringIO()) as f:
            self.cons.onecmd("destroy User")
            self.assertEqual(self.err_msg3, f.getvalue())
        with patch('sys.stdout', new=StringIO()) as f:
            self.cons.onecmd("destroy BaseModel 12345")
            self.assertEqual(self.err_msg4, f.getvalue())
        with patch('sys.stdout', new=StringIO()) as f:
            self.cons.onecmd(self.cons.precmd("City.destroy('123')"))
            self.assertEqual(self.err_msg4, f.getvalue())

    def test_5_update(self):
        """Tests output for cmd "update"
        """
        with patch('sys.stdout', new=StringIO()) as f:
            self.cons.onecmd("update")
            self.assertEqual(self.err_msg1, f.getvalue())
        with patch('sys.stdout', new=StringIO()) as f:
            self.cons.onecmd("update You")
            self.assertEqual(self.err_msg2, f.getvalue())
        with patch('sys.stdout', new=StringIO()) as f:
            self.cons.onecmd("update User")
            self.assertEqual(self.err_msg3, f.getvalue())
        with patch('sys.stdout', new=StringIO()) as f:
            self.cons.onecmd("update User 12345")
            self.assertEqual(self.err_msg4, f.getvalue())

    def test_6_update(self):
        """Tests output for cmd ".update()"
        """
        with patch('sys.stdout', new=StringIO()) as f:
            self.cons.onecmd(self.cons.precmd(".update('1213431')"))
            self.assertEqual(self.err_msg1, f.getvalue())
        with patch('sys.stdout', new=StringIO()) as f:
            self.cons.onecmd(self.cons.precmd("You.update()"))
            self.assertEqual(self.err_msg2, f.getvalue())
        with patch('sys.stdout', new=StringIO()) as f:
            self.cons.onecmd(self.cons.precmd("User.update()"))
            self.assertEqual(self.err_msg3, f.getvalue())
        with patch('sys.stdout', new=StringIO()) as f:
            self.cons.onecmd(self.cons.precmd("User.update('12345')"))
            self.assertEqual(self.err_msg4, f.getvalue())

    def test_2_show(self):
        """Tests output for cmd "show"
        """
        with patch('sys.stdout', new=StringIO()) as f:
            self.cons.onecmd("show")
            self.assertEqual(self.err_msg1, f.getvalue())
        with patch('sys.stdout', new=StringIO()) as f:
            self.cons.onecmd(self.cons.precmd("Any.show()"))
            self.assertEqual(self.err_msg2, f.getvalue())
        with patch('sys.stdout', new=StringIO()) as f:
            self.cons.onecmd("show Review")
            self.assertEqual(self.err_msg3, f.getvalue())
        with patch('sys.stdout', new=StringIO()) as f:
            self.cons.onecmd(self.cons.precmd("User.show('123')"))
            self.assertEqual(self.err_msg4, f.getvalue())


if __name__ == "__main__":
    unittest.main()
