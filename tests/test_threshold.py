import pytest
from unittest.mock import MagicMock
from src.controllers.sensorController import check_threshold

def test_kritisk_temperatur_giver_high_alert():
    cursor = MagicMock()
    db = MagicMock()
    
    check_threshold(cursor, db, "windmill-01", "temperature", 95)
    
    assert cursor.execute.called
    args = cursor.execute.call_args[0][1]
    assert args[4] == "HIGH"

def test_advarsel_temperatur_giver_medium_alert():
    cursor = MagicMock()
    db = MagicMock()
    
    check_threshold(cursor, db, "windmill-01", "temperature", 75)
    
    assert cursor.execute.called
    args = cursor.execute.call_args[0][1]
    assert args[4] == "MEDIUM"

def test_normal_temperatur_giver_ingen_alert():
    cursor = MagicMock()
    db = MagicMock()
    
    check_threshold(cursor, db, "windmill-01", "temperature", 50)
    
    assert not cursor.execute.called