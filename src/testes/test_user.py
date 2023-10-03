import unittest
import sqlite3
import os
from user import User

class UserTests(unittest.TestCase):
    def setUp(self):
        self.db_file = "test.db"
        self.user = User(self.db_file)
        self.conn = sqlite3.connect(self.db_file)
    
    def tearDown(self):
        self.conn.close()
        os.remove(self.db_file)
        
    def test_login(self):
        self.conn.execute("INSERT INTO users VALUES ('testuser', 'test@example.com', 'password')")
        self.conn.commit()

        self.assertEqual(self.user.login("testuser", "password"), True)
        self.assertEqual(self.user.login("testuser", "wrongpassword"), False)
        self.assertEqual(self.user.login("wronguser", "password"), False)
        self.assertEqual(self.user.login("", ""), "Preencha todos os campos!")
        
    def test_register_success(self):
        result = self.user.register('newuser', 'new@example.com', 'password', 'password')
        self.assertEqual(result, 'Usuário cadastrado com sucesso!')

        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username = ?", ('newuser',))
        user = cursor.fetchone()
        self.assertIsNotNone(user)

    def test_register_existing_username(self):
        self.conn.execute("INSERT INTO users VALUES ('existinguser', 'existing@example.com', 'password')")
        self.conn.commit()

        result = self.user.register('existinguser', 'new@example.com', 'password', 'password')
        self.assertEqual(result, 'o Username já está sendo usado!')

    def test_register_existing_email(self):
        self.conn.execute("INSERT INTO users VALUES ('existinguser', 'existing@example.com', 'password')")
        self.conn.commit()

        result = self.user.register('newuser', 'existing@example.com', 'password', 'password')
        self.assertEqual(result, 'Este email já está sendo usado, tente outro!')

    def test_register_password_mismatch(self):
        result = self.user.register('newuser', 'new@example.com', 'password', 'wrong_password')
        self.assertEqual(result, 'As senhas não coincidem!')

    def test_register_empty_fields(self):
        result = self.user.register('', '', '', '')
        self.assertEqual(result, 'Preencha todos os campos!')

    def test_change_password_success(self):
        self.conn.execute("INSERT INTO users VALUES ('testuser', 'test@example.com', 'password')")
        self.conn.commit()

        self.user.change_password('testuser', 'new_password')

        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username = ?", ('testuser',))
        user = cursor.fetchone()
        self.assertEqual(user[2], 'new_password')

    def test_check_user_existing(self):
        self.conn.execute("INSERT INTO users VALUES ('testuser', 'test@example.com', 'password')")
        self.conn.commit()

        result = self.user.check_user('testuser', 'test@example.com')
        self.assertTrue(result)

    def test_check_user_non_existing(self):
        result = self.user.check_user('nonexistinguser', 'nonexisting@example.com')
        self.assertFalse(result)

    def test_check_user_empty_fields(self):
        result = self.user.check_user('', '')
        self.assertEqual(result, 'Preencha todos os campos!')

if __name__ == '__main__':
    unittest.main()
        
        