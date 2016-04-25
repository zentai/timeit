from time import strftime
import time
import os
import datetime
from datetime import timedelta
import sys

def to_hour(sec):
    return get_time(sec)

def get_time(second):
    if second < 0:
        second = 0
    sec = timedelta(seconds=second)
    d = datetime.datetime(1,1,1) + sec
    return "%dh %dm" % (d.hour, d.minute)

def get_datetime(second):
    sec = timedelta(seconds=second)
    return (datetime.datetime.now() + sec).strftime("%Y%m%d %H:%M:%S")


class Timer(object):


    def __init__(self):
        self._key = self._initial()
        self._target_working_sec = 9 * 60 * 60 # 9 hour

    def _initial(self):
        key = "%s.txt" % strftime("%Y-%m-%d")
        if not os.path.exists(key):
            self._touch(key)
        return key

    def _touch(self, fname, times=None):
        with open(fname, 'a'):
            os.utime(fname, times)

    def timeit(self, desc):
        log = self._gen_log(desc)
        self._save(self._key, log)
        self.report()

    def _gen_log(self, desc):
        return "%s, %s" % (strftime("%Y%m%d %H:%M:%S"), desc)

    def _save(self, fname, desc):
        with open(fname, 'a') as f:
            f.write("%s\n" % desc)

    def _console(self, msg):
        print(msg)

    def report(self):
        raw = self._load(self._key)
        if len(raw) % 2 != 0:
            raw.append(self._gen_log("NOW"))
        working_sec = self._calc(raw)
        self._console("")
        self._console("========== Summary ===========")
        self._console("leave at : %s" % (get_datetime(self._target_working_sec - working_sec)))
        self._console("Countdown: %s" % (to_hour(self._target_working_sec - working_sec)))
        self._console("Working  : %s" % to_hour(working_sec))
        self._console("")
        self._print_raw(raw)


    def _load(self, fname):
        lines = []
        with open(fname) as f:
            lines = f.read().splitlines()
        return lines

    def _calc(self, raw):
        composite_list = [raw[x:x+2] for x in range(0, len(raw),2)]
        working_sec = 0
        for come_in, go_out in composite_list:
            sec = self._spend_time(come_in, go_out)
            working_sec += sec
        return working_sec

    def _spend_time(self, start_ts, end_ts):
        if not start_ts or not end_ts:
            return
        return self._timestamp(end_ts) - self._timestamp(start_ts)

    def _print_raw(self, raw):
        self._console("========== RAW data ===========")
        prev_item = None
        for idx, item in enumerate(raw, start=0):
            spend_min = self._to_min(self._spend_time(prev_item, item)) if idx % 2 == 0 and idx != 0 else "  "
            self._console("[%s] %s.) %s" % (spend_min, idx, item))
            prev_item = item

    def _to_min(self, second):
        if not second:
            return 0
        return int(second/60)

    def _timestamp(self, line):
        time_str = line.split(',')[0]
        return time.mktime(datetime.datetime.strptime(time_str, "%Y%m%d %H:%M:%S").timetuple())



if __name__ == '__main__':
    t = Timer()
    argv = sys.argv
    if len(argv) == 1:
        t.report()
    if len(argv) >= 2:
        t.timeit(" ".join(argv[1:]))
