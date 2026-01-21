from opendevtoolkit.plugins.time_tracker import format_duration


def test_format_duration():
    assert format_duration(5) == "5s"
    assert format_duration(65) == "1m 5s"
    assert format_duration(3600) == "1h 0m"
