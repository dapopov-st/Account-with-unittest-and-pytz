from account import Account
import unittest

# Run at the command line: python -m unittest test_account.py


class TestAccount(unittest.TestCase):
    def test_make_account_normal(self):
        acct_num = 'A123'
        first = 'John'
        last = 'Smith'
        tz = 'US/Eastern'
        balance = 100
        transaction_id = None
        a = Account(acct_num, first, last, tz, initial_balance=balance)
        self.assertEqual(acct_num, a.acct_num)
        self.assertEqual(first, a.first)
        self.assertEqual(last, a.last)
        self.assertEqual(first + ' ' + last, a.full_name)
        #self.assertEqual(tz, a.timezone)
        #self.assertEqual(balance, a.balance)
