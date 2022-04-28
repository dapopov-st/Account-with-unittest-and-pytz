import datetime
from collections import namedtuple
import numbers
#from timeHelper import TimeHelper
import pytz


def return_timezone(tz):
    while True:
        try:
            now_utc_aware = datetime.datetime.utcnow().replace(tzinfo=datetime.timezone.utc)
            now_utc_aware = now_utc_aware.astimezone(pytz.timezone(tz))
            #self._tz = pytz.timezone(tz)
            # return pytz.timezone(tz)
            break
        except pytz.UnknownTimeZoneError as err:
            print("Unknown timezone", err)
            print("Common timezones are: ")
            for zone in pytz.common_timezones:
                print(zone)
            tz = input("Enter a correct timezone: ")
            # exit(1)
        except:
            print("Another exception occurred")
            tz = input("Enter a correct timezone: ")
    return pytz.timezone(tz)


class Account:
    """TODO"""
    monthly_int_rate = .5  # percent representation

    def __init__(self, acct_num, first, last, tz='Etc/Greenwich', initial_balance=None, transaction_id=None):
        self._acct_num = acct_num
        # Assign the input values to the .first and .last properties directly instead of storing in non-public attributes
        # This way, all values provided to first and last, including initialization values, go through the setter method
        self.first = first
        self.last = last
        self.balance = initial_balance
        self.transaction_id = transaction_id if transaction_id else 0
        #self._tz = TimeHelper.return_timezone(tz)
        self.tz = return_timezone(tz)

    @property
    def tz(self):
        return self._tz

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

    # Make account num a read-only property
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
        if amt > 0:
            self._balance += amt
            return self.generate_conf_num('D')
        else:
            print("Deposit must be positive")

    def withdraw(self, amt):
        if self.balance - amt >= 0:
            self._balance = self._balance - amt
            return self.generate_conf_num('W')
        else:
            print("Transaction declined due to insufficient funds")
            return self.generate_conf_num('X')

    def deposit_interest(self):
        self._balance += (Account.monthly_int_rate/100)*self._balance
        print(self._balance)
        return  # TODO: return confirmation num

    def generate_conf_num(self, transaction: str) -> str:
        self.transaction_id += 1
        # cur_time = datetime.datetime.utcnow().replace(
        # tzinfo = datetime.timezone.utc).astimezone(pytz.timezone(self._tz))
        cur_time = datetime.datetime.utcnow().replace(
            tzinfo=datetime.timezone.utc).astimezone(self._tz)
        return transaction+'-'+str(self.acct_num)+'-'+datetime.datetime.strftime(cur_time, format='%Y%d%m%H%M%S')+'-'+str(self.transaction_id)

    # USE NAMEDTUPLE TO ACCESS PROPERTIES OF RESULT USING DOT NOTATION!!!!!

    def parse_conf_num(self, conf_num: str):
        conf_num_ = conf_num.split("-")
        transaction_code, transaction_id, account_number = conf_num_[
            0], conf_num_[-1], conf_num_[1]
        # Parse the date
        time = datetime.datetime.strptime(conf_num_[2], "%Y%d%m%H%M%S")
        time_utc = time.utcnow()
        print(time, time_utc)
        conf_num_dict = {
            "transaction_code": transaction_code,
            "account_number": account_number,
            "time": f"datetime.datetime.strftime(time,format='%Y-%d-%m %H:%M:%S ({self._tz})')",
            "time_utc": time_utc,
            "transaction_id": transaction_id
        }
        # time = datetime.datetime(dt)

        print(conf_num_)
        # TODO: parse time and time_utc
        Confirmation = namedtuple(
            'Confirmation', 'transaction_code account_number time time_utc transaction_id')
        # print(Confirmation)
        conf = Confirmation(**conf_num_dict)
        print(conf.transaction_code)
        print(conf.account_number)
        print(conf.time)
        print(conf.time_utc)
        print(conf.transaction_id)


if __name__ == '__main__':
    acct1 = Account(140568, 'John', 'Smith', 'America/New_York', 500)
    #acct1 = Account(140568, 'John', 'Smith', 'Amrica/ew_York', 500)
    conf_num = acct1.generate_conf_num('D')
    print(conf_num)
    acct1.parse_conf_num(conf_num)
    print(acct1.parse_conf_num(conf_num))
    print(acct1.balance)
