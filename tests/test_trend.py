import pytest
from unittest.mock import MagicMock, call
from src.controllers.sensorController import check_trend

def make_mocks(values):
    cursor = MagicMock()
    db = MagicMock()
    # Simuler ORDER BY id DESC — nyeste først
    db.cursor.return_value.fetchall.return_value = [(v,) for v in reversed(values)]
    trend_cursor = db.cursor.return_value
    return cursor, db, trend_cursor

def test_stigende_trend_i_prewarning_zone_giver_alert():
    cursor, db, trend_cursor = make_mocks([51, 55, 58, 62, 67])
    check_trend(cursor, db, "windmill-01", "temperature")
    print("db.cursor call count:", db.cursor.call_count)
    print("trend_cursor id:", id(trend_cursor))
    print("db.cursor() returnerer:", id(db.cursor.return_value))
    print("calls:", trend_cursor.execute.call_args_list)
    assert trend_cursor.execute.call_count == 2

def test_stigende_trend_i_normalområde_giver_ingen_alert():
    cursor, db, trend_cursor = make_mocks([20, 25, 30, 35, 40])
    check_trend(cursor, db, "windmill-01", "temperature")
    assert trend_cursor.execute.call_count == 1  # kun SELECT

def test_stigende_trend_over_warning_giver_ingen_trend_alert():
    cursor, db, trend_cursor = make_mocks([71, 73, 75, 78, 80])
    check_trend(cursor, db, "windmill-01", "temperature")
    assert trend_cursor.execute.call_count == 1  # kun SELECT

def test_ikke_konsekvent_stigning_giver_ingen_alert():
    cursor, db, trend_cursor = make_mocks([51, 60, 55, 63, 67])
    check_trend(cursor, db, "windmill-01", "temperature")
    assert trend_cursor.execute.call_count == 1  # kun SELECT

def test_fewer_than_5_readings_giver_ingen_alert():
    cursor, db, trend_cursor = make_mocks([51, 55, 58])
    check_trend(cursor, db, "windmill-01", "temperature")
    assert trend_cursor.execute.call_count == 1  # kun SELECT

def test_stigende_trend_rpm_i_prewarning_zone_giver_alert():
    cursor, db, trend_cursor = make_mocks([1210, 1300, 1400, 1500, 1550])
    check_trend(cursor, db, "windmill-01", "rpm")
    assert trend_cursor.execute.call_count == 2  # SELECT + INSERT

def test_ukendt_sensor_type_giver_ingen_alert():
    cursor, db, trend_cursor = make_mocks([51, 55, 58, 62, 67])
    check_trend(cursor, db, "windmill-01", "humidity")
    assert not trend_cursor.execute.called