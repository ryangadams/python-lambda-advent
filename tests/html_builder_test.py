import json
import pathlib

from freezegun import freeze_time
from pyquery import PyQuery as pq
from functions.advent.calendar import build_panel_list, build_panel, build_window_list

with open(pathlib.Path(__file__).parent / "fixtures/sample_data.json") as file:
    sample_data = json.load(file)


@freeze_time("2012-01-14")
def test_prints_all_dates_in_january():
    output = build_panel_list(sample_data)
    html = pq(output)
    assert len(html("div.panel-container")) == 24


@freeze_time("2012-12-14")
def test_prints_up_to_today_in_december():
    output = build_panel_list(sample_data)
    html = pq(output)
    assert len(html("div.panel-container")) == 14


@freeze_time("2012-11-14")
def test_prints_nothing_the_rest_of_the_year():
    output = build_panel_list(sample_data)
    assert output == ""


def test_converts_day_number_to_text():
    html = pq(build_panel(**sample_data["values"][1]))
    assert html.attr("id") == "two"
    assert html("h2").text() == "Two – Welcome"
    html = pq(build_panel(**sample_data["values"][22]))
    assert html("h2").text() == "Twenty-three – Welcome"


def test_builds_all_boxes():
    html = pq(build_window_list())
    assert len(html("li")) == 24


def test_box_element_has_correct_id_and_text():
    html = pq(build_window_list())
    eleventh = html("li").eq(10)
    assert eleventh.text() == "11"
    assert eleventh.find("a").attr("href") == "#eleven"


@freeze_time("2012-12-15")
def test_box_list_has_the_right_number_open():
    html = pq(build_window_list())
    assert len(html("li.opened")) == 15


def test_building_panels():
    sheet_data = {
        "values": [
            {
                "day": "1",
                "title": "Welcome",
                "image": "https://www.stevensegallery.com/200/300",
                "video": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
                "comments": "First date",
            }
        ],
        "title": "2020's Advent Calendar",
        "image": "https://www.placecage.com/1280/800",
    }
    filtered_dates = sheet_data["values"]

    built_html = [build_panel(**date) for date in filtered_dates]
    output = "".join(built_html)
    print(output)
    assert len(built_html) == 1
