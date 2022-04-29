from account import Account
import unittest
from time_helper import return_timezone


class TestAccount(unittest.TestCase):
    """Test the methods in the Account class. To run the tests, navigate to the current
    directory at the command line, then type 
    python -m unittest test_account.py"""

    def setUp(self):
        print('Running setup...')
        self.acct_num = 'A123'
        self.first = 'John'
        self.last = 'Smith'
        self.tz = 'US/Eastern'
        self.balance = 100
        self.transaction_id = 0
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
                    Account(self.acct_num, first, self.last,
                            self.tz, initial_balance=self.balance)

    def test_make_account_invalid_last(self):
        lasts = ("", "  ", 123, None)
        for i, last in enumerate(lasts):
            with self.subTest(i):
                with self.assertRaises(ValueError):
                    Account(self.acct_num, self.first, last,
                            self.tz, initial_balance=self.balance)

    def test_make_account_invalid_balance(self):
        self.balance = -100
        balances = (-100, 'abc')
        for i, balance in enumerate(balances):
            with self.subTest(test_number=i):
                with self.assertRaises(ValueError):
                    Account(self.acct_num, self.first, self.last,
                            self.tz, initial_balance=balance)

    def test_generate_conf_num(self):
        a = Account(self.acct_num, self.first, self.last,
                    self.tz, initial_balance=self.balance)
        transaction = 'D'  # Should work for other letters as well
        self.transaction_id += 1
        conf_code = a.generate_conf_num(transaction)
        self.assertIn('D-', conf_code)

    def test_deposit_normal(self):
        deposit_amount = 200
        a = Account(self.acct_num, self.first, self.last,
                    self.tz, initial_balance=self.balance)
        final_balance = self.balance + deposit_amount
        conf_num = a.deposit(deposit_amount)
        self.assertAlmostEqual(a._balance, final_balance)
        self.assertIn('D-', conf_num)

    def test_withdraw_normal(self):
        withdrawal_amount = 100
        a = Account(self.acct_num, self.first, self.last,
                    self.tz, initial_balance=self.balance)
        final_balance = self.balance - withdrawal_amount
        conf_num = a.withdraw(withdrawal_amount)
        self.assertAlmostEqual(a._balance, final_balance)
        self.assertIn('W-', conf_num)

    def test_deposit_invalid(self):
        deposit_amounts = (-100, 'hundred')
        for i, deposit_amount in enumerate(deposit_amounts):
            with self.subTest(test_number=i):
                with self.assertRaises(ValueError):
                    a = Account(self.acct_num, self.first, self.last,
                                self.tz, initial_balance=self.balance)
                    a.deposit(deposit_amount)

    def test_withdrawal_invalid(self):
        withdrawal_amounts = (2000, 'thousand')
        for i, withdrawal_amount in enumerate(withdrawal_amounts):
            with self.subTest(test_number=i):
                with self.assertRaises(ValueError):
                    a = Account(self.acct_num, self.first, self.last,
                                self.tz, initial_balance=self.balance)
                    a.withdraw(withdrawal_amount)
