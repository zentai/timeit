from time import strftime
import time
import os
import datetime
import sys

def to_min(sec):
    return int(sec/60)

def to_hour(sec):
    return int(sec/60/60)


class Timer(object):


    def __init__(self):
        self._key = self._initial()
        self._target_working_sec = 9 * 60 * 60 # 9 hour

    def _initial(self):
        key = "%s" % strftime("%Y-%m-%d")
        if not os.path.exists(key):
            self._touch(key)
        return key

    def _touch(self, fname, times=None):
        with open(fname, 'a'):
            os.utime(fname, times)

    def timeit(self, desc):
        log = self._gen_log(desc)
        self._save(self._key, log)
        self._console(log)

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
        count_down_min = to_min(self._target_working_sec - working_sec)
        count_down_hour = to_hour(self._target_working_sec - working_sec)
        self._console("Countdown minutes: %s hr (%s min)" % (count_down_hour, count_down_min))
        self._console("")
        self._console("Target working minutes: %s hr (%s min)" % (to_hour(self._target_working_sec), to_min(self._target_working_sec)))
        self._console("Current working minutes: %s hr (%s min)" % (to_hour(working_sec), to_min(working_sec)))


    def _load(self, fname):
        lines = []
        with open(fname) as f:
            lines = f.read().splitlines()
        return lines

    def _calc(self, raw):
        composite_list = [raw[x:x+2] for x in range(0, len(raw),2)]
        working_sec = 0
        self._print_raw(raw)
        for come_in, go_out in composite_list:
            sec = self._timestamp(go_out) - self._timestamp(come_in)
            working_sec += sec
        return working_sec

    def _print_raw(self, raw):
        self._console("========== RAW data ===========")
        for idx, item in enumerate(raw, start=0):
            self._console("[%s] %s.) %s" % ("*" if idx % 2 == 0 else " ", idx, item))

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
