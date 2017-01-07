import requests
import pytz
from datetime import time, datetime


def load_attempts(pages=10):
    url = 'https://devman.org/api/challenges/solution_attempts'
    for page in range(1, pages + 1):
        response = requests.get(url, params={'page': page}).json()
        yield from response['records']


def is_midnighter(record, end_hour=3):
    timestamp = record['timestamp']
    if timestamp:
        timezone = record['timezone']
        attempt_time = datetime.fromtimestamp(timestamp, pytz.timezone(timezone)).time()
        return time(0, 0) < attempt_time < time(end_hour, 0)


def get_midnighters():
    return {record['username'] for record in load_attempts() if is_midnighter(record)}


if __name__ == '__main__':
    midnighters = get_midnighters()
    print("Отправляли задачи на проверку после полуночи:")
    print('\n'.join(midnighters))
