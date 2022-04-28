import datetime
import pytz


class TimeHelper:
    @staticmethod
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
