import datetime
from collections import namedtuple
import numbers
from time_helper import return_timezone


class Account:
    """A simple account class with timezones handled by pytz and return_timezone helper function. 
    Confirmation numbers are produced after every transaction and user information is validated."""
    monthly_int_rate: float
    monthly_int_rate = .5  # percent representation

    def __init__(self, acct_num, first, last, tz='Etc/Greenwich', initial_balance=None, transaction_id=None):
        self._acct_num = acct_num
        # Assign the input values to the .first and .last properties directly instead of storing in non-public attributes
        # This way, all values provided to first and last, including initialization values, go through the setter methods
        self.first = first
        self.last = last
        self.balance = initial_balance
        self.transaction_id = transaction_id if transaction_id else 0
        self._tz = return_timezone(tz)

    @property
    def first(self):
        return self._first

    @first.setter
    def first(self, val):
        self._first = Account.validate_and_set_name(
            '_first', val, 'First name')

    @property
    def last(self):
        return self._last

    @last.setter
    def last(self, val):
        self._last = Account.validate_and_set_name('_last', val, 'Last name')

    @staticmethod
    def validate_and_set_name(field, val, field_name):
        if val is not None and isinstance(val, str) and len(val.strip()) > 0:
            return val.strip()
        else:
            raise ValueError(f'{field_name} name must be a nonempty string')

    @property
    def full_name(self):
        return f"{self.first} {self.last}"

    # Make account_num a read-only property
    @property
    def acct_num(self):
        return self._acct_num

    @property
    def balance(self):
        return self._balance

    @balance.setter
    def balance(self, val):
        self._balance = Account.validate_and_set_balance(val)

    @staticmethod
    def validate_and_set_balance(val):
        if isinstance(val, numbers.Integral) and val >= 0:
            return val
        else:
            raise ValueError("Balance must be a nonnegative number")

    def deposit(self, amt):
        if isinstance(amt, numbers.Integral) and amt >= 0:
            self._balance += amt
            return self.generate_conf_num('D')
        else:  # This part could perhaps be improved with a custom exception class
            conf = self.generate_conf_num('X')
            print("Transaction declined since deposit must be a nonnegative real number")
            print("Confirmation number: ", conf)
            assert 'X-' in conf, "Confirmation code must start with X- for denied transactions"
            raise ValueError("Deposit must be positive")

    def withdraw(self, amt):
        if isinstance(amt, numbers.Integral) and self.balance - amt >= 0:
            self._balance = self._balance - amt
            return self.generate_conf_num('W')
        else:
            conf = self.generate_conf_num('X')
            print("Transaction declined due to insufficient funds")
            print("Confirmation number: ", conf)
            assert 'X-' in conf, "Confirmation code must start with X- for denied transactions"
            raise ValueError("Enter withdrawal as a negative number and \n",
                             "make sure that final balance is nonnegative")

    def deposit_interest(self):
        self._balance += (Account.monthly_int_rate/100)*self._balance
        return self.generate_conf_num('I')

    def generate_conf_num(self, transaction: str) -> str:
        self.transaction_id += 1
        cur_time = datetime.datetime.utcnow().replace(
            tzinfo=datetime.timezone.utc).astimezone(self._tz)
        return transaction+'-'+str(self.acct_num)+'-'+datetime.datetime.strftime(cur_time, format='%Y%d%m%H%M%S')+'-'+str(self.transaction_id)

    def parse_conf_num(self, conf_num: str):
        conf_num_ = conf_num.split("-")
        transaction_code, transaction_id, account_number = conf_num_[
            0], conf_num_[-1], conf_num_[1]
        # Parse the date
        time = datetime.datetime.strptime(conf_num_[2], "%Y%d%m%H%M%S")
        time_utc = time.utcnow()
        # Set up a dictionary and pass it to Confirmation namedtuple
        conf_num_dict = {
            "transaction_code": transaction_code,
            "account_number": account_number,
            "time": f"datetime.datetime.strftime(time,format='%Y-%d-%m %H:%M:%S ({self._tz})')",
            "time_utc": time_utc,
            "transaction_id": transaction_id
        }
        Confirmation = namedtuple(
            'Confirmation', 'transaction_code account_number time time_utc transaction_id')
        return Confirmation(**conf_num_dict)


# Some preliminary tests.  Formal tests are in test_account.py
if __name__ == '__main__':
    acct1 = Account(140568, 'John', 'Smith', 'America/New_York', 500)
    conf_num = acct1.generate_conf_num('D')
    print(conf_num)
    print(acct1.parse_conf_num(conf_num))
    print(acct1.balance)
    print(acct1.deposit(100))
    # The code below is for testing purposes only, DO NO USE BARE EXCEPTIONS IN PRODUCTION CODE!
    try:
        print(acct1.deposit(-100))
    except:
        pass
    try:
        print(acct1.withdraw(1000))
    except:
        pass
    acct2 = Account(140568, 'John', 'Smith', 'Amrica/ew_York', 500)
    print(acct2.deposit(2000))
    print(acct2.deposit_interest())
