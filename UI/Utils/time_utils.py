from PySide6.QtCore import QDateTime


class TimeUtils:

    @staticmethod
    def get_live_clock_text():
        current_time = QDateTime.currentDateTime()

        return current_time.toString(
            "'Live |' hh:mm:ss AP"
        )