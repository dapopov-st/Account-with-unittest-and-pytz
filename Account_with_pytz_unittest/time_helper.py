import datetime
import pytz


def return_timezone(tz=None):
    """A helper function for handling timezones in the Account class.  If the user enters
    an invalid time zone, the user is given a list of possible correct answers and 
    prompted to reenter the time zone."""
    while True:
        try:
            now_utc_aware = datetime.datetime.utcnow().replace(tzinfo=datetime.timezone.utc)
            now_utc_aware = now_utc_aware.astimezone(pytz.timezone(tz))
            break

        except pytz.UnknownTimeZoneError as err:
            print("Unknown timezone", err)
            print("Common timezones are: ")
            for zone in pytz.common_timezones:
                print(zone)
            tz = input("Enter a correct timezone: ")

        except AttributeError as err:
            print("Invalid attribute", err)

    return pytz.timezone(tz)
