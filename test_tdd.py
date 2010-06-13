#!/usr/bin/python
# -*- coding:Utf-8 -*-

"""
This file is part of Toudoudone.

Toudoudone is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

Toudoudone is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with Toudoudone.  If not, see <http://www.gnu.org/licenses/>.

Toudoudone  Copyright (C) 2010  Laurent Peuch <cortex@worlddomination.be>
"""

import unittest
from tdd import TodoDB, TodoAlreadyExist, TodoDoesntExist

class Test_TDD(unittest.TestCase):

    def reinitialise(self):
        """
        Reinitialise the db to make test with a clean one
        """
        tododb = TodoDB('sqlite:/:memory:')
        tododb.drop_db()
        tododb.create_db()
        return tododb

    def test_create_a_db(self):
        """
        create a clean database to test
        """
        tododb = self.reinitialise()

    def test_connect(self):
        TodoDB()

    def test_connect_to_another_database(self):
        TodoDB("sqlite:/file")

    def test_add_a_todo(self):
        """
        You should be able to add a new todo.
        This should inscrease the number of todos by one
        """
        tododb = self.reinitialise()

        was = tododb.todo_len()

        tododb.add_todo("This is a new todo")

        self.assertEqual(was + 1, tododb.todo_len())

    def test_cant_add_two_time_the_same_todo(self):
        """
        You shouldn't be able to add two time a todo with the same description
        """
        tododb = self.reinitialise()

        was = tododb.todo_len()

        tododb.add_todo("This is a new todo")

        self.assertEqual(was + 1, tododb.todo_len())

        self.assertRaises(TodoAlreadyExist, tododb.add_todo, "This is a new todo")

    def test_raise_if_todo_already_exist_multiple_time(self):
        tododb = self.reinitialise()

        was = tododb.todo_len()

        tododb.add_todo("This is a new todo")

        self.assertEqual(was + 1, tododb.todo_len())
        tododb._Todo(description="This is a new todo")
        self.assertEqual(was + 2, tododb.todo_len())

        self.assertRaises(AssertionError, tododb.add_todo, "This is a new todo")

    def test_get_todo_id(self):
        tododb = self.reinitialise()

        tododb.add_todo("This is a new todo")
        tododb.add_todo("This is a new todo 2")

        self.assertEqual(1, tododb.get_todo_by_desc("This is a new todo").id)
        self.assertEqual(2, tododb.get_todo_by_desc("This is a new todo 2").id)

    def test_get_todo_id_should_raise_an_exection_if_todo_doesnt_exist(self):
        tododb = self.reinitialise()

        self.assertRaises(TodoDoesntExist, tododb.get_todo_by_desc, "todo")

    def test_remove_todo(self):
        tododb = self.reinitialise()

        was = tododb.todo_len()
        tododb.add_todo("This is a new todo")

        self.assertEqual(was + 1, tododb.todo_len())

        todo = tododb.get_todo_by_desc("This is a new todo")
        tododb.remove_todo(todo.id)

        self.assertEqual(was, tododb.todo_len())

    def test_remove_should_raise_an_exception_if_todo_doesnt_exist(self):
        tododb = self.reinitialise()

        self.assertRaises(TodoDoesntExist, tododb.remove_todo, 3)

    def test_todo_len(self):
        tododb = self.reinitialise()
        self.assertEqual(0, tododb.todo_len())
        tododb.add_todo("New todo")
        self.assertEqual(1, tododb.todo_len())
        tododb.add_todo("New todo 2")
        self.assertEqual(2, tododb.todo_len())
        tododb.remove_todo(1)
        self.assertEqual(1, tododb.todo_len())
        tododb.remove_todo(2)
        self.assertEqual(0, tododb.todo_len())

    def test_seach_for_todo(self):
        tododb = self.reinitialise()

        todo_to_add = ("new todo", "another todo", "yet a todo", "tododo", "todotodo")
        todo_to_add_that_doesnt_match = ("blabla", "foo", "bar")

        true = [tododb.add_todo(i) for i in todo_to_add]

        false = [tododb.add_todo(i) for i in todo_to_add_that_doesnt_match]

        result = tododb.search_for_todo("todo")

        self.assertEqual(len(todo_to_add), len(result))

        for i in result:
            self.assertTrue(i.description in todo_to_add)
            self.assertTrue(i in true)
            self.assertFalse(i.description in todo_to_add_that_doesnt_match)
            self.assertFalse(i in false)

    def test_get_todo_by_desc(self):
        tododb = self.reinitialise()

        tododb.add_todo("todo")

        todo = tododb.get_todo_by_desc("todo")

        self.assertEqual(todo.id, 1)

        self.assertEqual(todo.description, "todo")

    def test_get_todo_should_return_the_created_todo(self):
        tododb = self.reinitialise()

        todo = tododb.add_todo("todo")

        self.assertEqual(todo.description, "todo")

    def test_get_todo_throw_except_if_doesnt_exist(self):
        tododb = self.reinitialise()

        self.assertRaises(TodoDoesntExist, tododb.get_todo_by_desc, "haha I don't exist")

    def test_rename_todo(self):
        tododb = self.reinitialise()

        t = tododb.add_todo("first name")

        tododb.rename_todo(t.id, "second name")

        self.assertEqual(t.description, "second name")

    def test_rename_todo_should_raise_exception_if_doesnt_exist(self):
        tododb = self.reinitialise()

        self.assertRaises(TodoDoesntExist, tododb.rename_todo, 15, "haha I don't exist")

    def test_toggle_todo(self):
        tododb = self.reinitialise()

        t = tododb.add_todo("prout")

        self.assertFalse(t.completed)
        tododb.toggle(t.id)
        self.assertTrue(t.completed)
        tododb.toggle(t.id)
        self.assertFalse(t.completed)

    def test_toggle_raise_doesnt_exist(self):
        tododb = self.reinitialise()
        self.assertRaises(TodoDoesntExist, tododb.toggle, 42)

    def test_list_todos(self):
        tododb = self.reinitialise()
        # empty
        self.assertEqual(0, len(tododb.list_todos()))
        t = tododb.add_todo("todo")
        # one todo
        self.assertEqual(1, len(tododb.list_todos()))
        self.assertTrue(t in tododb.list_todos())
        # two todo
        t2 = tododb.add_todo("todo 2")
        self.assertEqual(2, len(tododb.list_todos()))
        self.assertTrue(t in tododb.list_todos())
        self.assertTrue(t2 in tododb.list_todos())
        # only uncompleted
        tododb.toggle(t2.id)
        self.assertEqual(1, len(tododb.list_todos()))
        self.assertTrue(t in tododb.list_todos())
        self.assertTrue(t2 not in tododb.list_todos())
        # everything
        self.assertEqual(2, len(tododb.list_todos(all=True)))
        self.assertTrue(t in tododb.list_todos(all=True))
        self.assertTrue(t2 in tododb.list_todos(all=True))


if __name__ == "__main__":
   unittest.main()

