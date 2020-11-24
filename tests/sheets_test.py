import json
import os


from functions.advent.google_sheets import get_sheet_data, parse_to_shape


def test_sheets_gets_sheets_data():
    def does_nothing_mapper(response_data):
        return response_data

    sheet_data = get_sheet_data(does_nothing_mapper)
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
                "First date",
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
