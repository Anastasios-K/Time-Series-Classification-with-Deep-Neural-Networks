from datetime import datetime


class TimeID:

    def __init__(self):
        self._timeid = self.__form_timeid()

    @property
    def timeid(self):
        return self._timeid

    @staticmethod
    def __form_timeid() -> str:
        current_date_and_time = datetime.now()
        curtxt = str(current_date_and_time)
        curtxt = curtxt.split(sep=".")[0]
        curtxt = curtxt.replace("-", "")
        curtxt = curtxt.replace(":", "")
        curtxt = curtxt.replace(" ", "_")
        return curtxt