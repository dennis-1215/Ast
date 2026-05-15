from PySide6.QtCore import QTimer, QDateTime


class TimerManager:
    def __init__(self, parent=None):
        self.parent = parent
        self.timers = {}

    # 타이머 생성
    def create_timer(self, name, interval, callback, auto_start=True, single_shot=False):

        # 이미 존재하면 제거
        if name in self.timers:
            self.stop_timer(name)

        timer = QTimer(self.parent)
        timer.timeout.connect(callback)
        timer.setInterval(interval)
        timer.setSingleShot(single_shot)

        self.timers[name] = timer

        if auto_start:
            timer.start()

        return timer

    # 타이머 시작
    def start_timer(self, name):
        if name in self.timers:
            self.timers[name].start()

    # 타이머 정지
    def stop_timer(self, name):
        if name in self.timers:
            self.timers[name].stop()

    # 타이머 제거
    def remove_timer(self, name):

        if name in self.timers:
            timer = self.timers.pop(name)

            timer.stop()
            timer.deleteLater()

    # 특정 타이머 가져오기
    def get_timer(self, name):
        return self.timers.get(name)

    # 모든 타이머 종료
    def stop_all(self):
        for timer in self.timers.values():
            timer.stop()

    # 모든 타이머 제거
    def clear(self):

        for timer in self.timers.values():
            timer.stop()
            timer.deleteLater()

        self.timers.clear()