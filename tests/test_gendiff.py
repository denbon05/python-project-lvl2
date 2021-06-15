import io
from os import path

from gendiff.app import generate_diff


def get_fixture_path(filename):
    return path.join(path.dirname(path.abspath(__file__)), "fixtures", filename)


def read_fixture(filepath):
    return io.open(filepath).read()


json1_path = get_fixture_path("file1.json")
json2_path = get_fixture_path("file2.json")
yml1_path = get_fixture_path("file1.yml")
yml2_path = get_fixture_path("file2.yml")

default_result_path = get_fixture_path("stylish.txt")
plain_result_path = get_fixture_path("plain.txt")
json_result_path = get_fixture_path("json.txt")


def test_generate_diff():
    default_result = read_fixture(default_result_path)
    plain_result = read_fixture(plain_result_path)
    json_result = read_fixture(json_result_path)

    assert generate_diff(json1_path, json2_path) == default_result
    assert generate_diff(yml1_path, yml2_path) == default_result
    assert generate_diff(yml1_path, json2_path, "plain") == plain_result
    assert generate_diff(json1_path, yml2_path, "json") == json_result