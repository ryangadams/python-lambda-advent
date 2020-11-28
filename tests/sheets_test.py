import json
import os
from datetime import datetime, timedelta

import pytest

import functions.advent.google_sheets as gs
from functions.advent.calendar import parse_to_shape
from functions.advent.csv_sheets import get_sheet_data_csv


def test_sheets_gets_sheets_data():
    def does_nothing_mapper(response_data):
        return response_data

    sheet_data = gs.get_sheet_data(does_nothing_mapper)
    expected_data = {
        "range": "Sheet1!A1:E1000",
        "majorDimension": "ROWS",
        "values": [
            [
                "Meta",
                "Title",
                "2020's Advent Calendar",
                "Image",
                "https://www.placecage.com/1280/720",
            ],
            ["Date", "Title", "Pic Url (not used)", "Vid Url", "Comment"],
            [
                "1",
                "Welcome",
                "",
                "https://www.youtube.com/embed/dQw4w9WgXcQ",
                "Advent Day 1",
            ],
            [
                "2",
                "Hello",
                "",
                "https://www.youtube.com/embed/dQw4w9WgXcQ",
                "Advent Day 2",
            ],
            [
                "3",
                "Goodbye",
                "",
                "https://www.youtube.com/embed/dQw4w9WgXcQ",
                "Advent day 3",
            ],
        ],
    }

    assert sheet_data == expected_data


def test_data_mapper():
    input_data = {
        "range": "Sheet1!A1:E1000",
        "majorDimension": "ROWS",
        "values": [
            [
                "Meta",
                "Title",
                "2020's Advent Calendar",
                "Image",
                "https://www.placecage.com/1280/800",
            ],
            ["Date", "Title", "Pic Url", "Vid Url", "Comment"],
            [
                "1",
                "Welcome",
                "https://www.stevensegallery.com/200/300",
                "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
                "First date",
            ],
        ],
    }
    expected_output = {
        "values": [
            {
                "day": "1",
                "title": "Welcome",
                "image": "https://www.stevensegallery.com/200/300",
                "video": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
                "comments": "First date",
            },
        ],
        "image": "https://www.placecage.com/1280/800",
        "title": "2020's Advent Calendar",
    }
    assert parse_to_shape(input_data) == expected_output


# A couple of helpers
def now():
    return datetime.now()


def hours_ago(num):
    # has a hack to fix correct for test run duration
    return datetime.now() - timedelta(hours=num, seconds=-5)


# fmt: off
@pytest.mark.parametrize(
    "data,timestamp,expected_result",
    [
        (True, datetime.now(), False),  # has recent content
        (None, now(), True),  # has no content but thinks it does (shouldn't happen)
        (None, hours_ago(2), True),  # no content, and it is expired (shouldn't happen)
        (True, hours_ago(2), True),  # has content, but it's expired
        (True, hours_ago(1), False),  # has content, not yet expired
    ],
)
def test_supports_simple_caching(data, timestamp, expected_result):
    gs.simple_caching_sheet_data = data
    gs.simple_caching_time = timestamp

    assert gs.cache_expired_or_empty() is expected_result
# fmt: on


def test_gets_csv_data():
    def does_nothing_mapper(response_data):
        return response_data

    sheet_data = get_sheet_data_csv(does_nothing_mapper)
    expected_data = {
        "range": "Sheet1!A1:E1000",
        "majorDimension": "ROWS",
        "values": [
            [
                "Meta",
                "Title",
                "2020's Advent Calendar",
                "Image",
                "https://www.placecage.com/1280/720",
            ],
            ["Date", "Title", "Pic Url (not used)", "Vid Url", "Comment"],
            [
                "1",
                "Welcome",
                "",
                "https://www.youtube.com/embed/dQw4w9WgXcQ",
                "Advent Day 1",
            ],
            [
                "2",
                "Hello",
                "",
                "https://www.youtube.com/embed/dQw4w9WgXcQ",
                "Advent Day 2",
            ],
        ],
    }

    assert sheet_data == expected_data
