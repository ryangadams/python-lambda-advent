import json
import pathlib

from functions.advent.handler import handler
from functions.advent.request import should_show_preview


def test_makes_plain_request():
    with open(pathlib.Path(__file__).parent / "fixtures/request.json") as fixture:
        request_object = json.load(fixture)

    response = handler(request_object, {})

    assert "statusCode" in response


def test_preview_tests():
    event = {}
    assert should_show_preview(event) is False
    event = {"queryStringParameters": {}}
    assert should_show_preview(event) is False
    event = {"queryStringParameters": {"preview": "no"}}
    assert should_show_preview(event) is False
    event = {"queryStringParameters": {"preview": "yes"}}
    assert should_show_preview(event) is True
