from account import Account
import unittest
from time_helper import return_timezone


# To run at the command line: python -m unittest test_account.py


class TestAccount(unittest.TestCase):
    def setUp(self):
        print('Running setup...')
        self.acct_num = 'A123'
        self.first = 'John'
        self.last = 'Smith'
        self.tz = 'US/Eastern'
        self.balance = 100
        self.transaction_id = None
        self._tz = return_timezone(self.tz)

    def tearDown(self):
        print('Running tear down...')

    def test_make_account_normal(self):
        a = Account(self.acct_num, self.first, self.last,
                    self.tz, initial_balance=self.balance)
        self.assertEqual(self.acct_num, a.acct_num)
        self.assertEqual(self.first, a.first)
        self.assertEqual(self.last, a.last)
        self.assertEqual(self.first + ' ' + self.last, a.full_name)
        self.assertEqual(self._tz, a._tz)
        self.assertEqual(self.balance, a.balance)

    def test_make_account_invalid_first(self):
        firsts = ("", "  ", 123, None)
        for i, first in enumerate(firsts):
            with self.subTest(i):
                with self.assertRaises(ValueError):
                    a = Account(self.acct_num, first, self.last,
                                self.tz, initial_balance=self.balance)

    def test_make_account_invalid_last(self):
        lasts = ("", "  ", 123, None)
        for i, last in enumerate(lasts):
            with self.subTest(i):
                with self.assertRaises(ValueError):
                    a = Account(self.acct_num, self.first, last,
                                self.tz, initial_balance=self.balance)

    def test_make_account_invalid_balance(self):
        self.balance = -100
        balances = (-100, 'abc')
        for i, balance in enumerate(balances):
            with self.subTest(test_number=i):
                with self.assertRaises(ValueError):
                    Account(self.acct_num, self.first, self.last,
                            self.tz, initial_balance=balance)

    # TODO: test generate conf num
