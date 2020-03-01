import argparse
from functools import partial
import os
from datetime import datetime, timedelta


class Task:
    def __init__(self, start_time, end_time, category):
        self._time = end_time - start_time
        self._category = category

    def get_time(self):
        return self._time

    def get_category(self):
        return self._category

    def __str__(self):
        return f'{self._category} - {self._time}'


class CategoryTime:
    def __init__(self, category, seconds=0):
        self._time = timedelta(seconds=seconds)
        self._category = category

    def __str__(self):
        hours = int(self._time.total_seconds() // (60*60))
        minutes = int((self._time.total_seconds() - hours*60*60) // 60)
        return f'{self._category} - {hours:02d}:{minutes:02d}'

    def __add__(self, task):
        return CategoryTime(
            category=self._category,
            seconds=(self._time + task.get_time()).total_seconds(),
        )


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('log_file', type=os.path.abspath)
    return parser.parse_args()


def get_tasks(log_file):
    time_format = r'%H:%M'
    now = datetime.now()
    today = partial(datetime, now.year, now.month, now.day)
    with open(log_file, 'r') as f:
        start_time, category, *_ = next(f).split()
        start_time = datetime.strptime(start_time, time_format)
        start_time = today(start_time.hour, start_time.minute)
        for line in f:
            end_time, new_category, *_ = line.split()
            end_time = datetime.strptime(end_time, time_format)
            end_time = today(end_time.hour, end_time.minute)
            yield Task(start_time, end_time, category)

            start_time = end_time
            category = new_category

    yield Task(start_time, now, category)


def get_times_per_category(tasks):
    categories = {}
    for task in tasks:
        category_time = categories.get(
            task.get_category(),
            CategoryTime(task.get_category()),
        )
        categories[task.get_category()] = category_time + task
    yield from categories.values()


def main():
    args = get_args()
    tasks = get_tasks(args.log_file)
    for category_time in get_times_per_category(tasks):
        print(category_time)


if __name__ == '__main__':
    main()
