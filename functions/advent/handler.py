import json

from functions.advent.calendar import build_advent_calendar
from functions.advent.google_sheets import get_sheet_data, parse_to_shape


def should_show_preview(event):
    return (
        "queryStringParameters" in event
        and "preview" in event["queryStringParameters"]
        and event["queryStringParameters"]["preview"] == "yes"
    )


def handler(event, context):
    advent_data = get_sheet_data(parse_to_shape)
    print(advent_data)

    show_all_dates = True if should_show_preview(event) else False
    if show_all_dates:
        print("showing all dates, handler")

    accept_header = event["headers"]["accept"]
    if accept_header.startswith("text/html"):
        return {
            "statusCode": 200,
            "headers": {"Content-Type": "text/html"},
            "body": build_advent_calendar(advent_data, show_all=show_all_dates),
        }

    return {
        "statusCode": 200,
        "headers": {"Content-Type": "text/json"},
        "body": json.dumps(advent_data),
    }
