import pytest
import assistant

def test_stadium_data_loaded():
    assert assistant.DATA is not None
    assert "stadium" in assistant.DATA
    assert "gates" in assistant.DATA
    assert "washrooms" in assistant.DATA
    assert "first_aid" in assistant.DATA
    assert "water_stations" in assistant.DATA

def test_detect_intent():
    intent, score = assistant.detect_intent("where is gate 3")
    assert intent == "gate"
    assert score > 0

    intent, score = assistant.detect_intent("medical emergency")
    assert intent == "emergency"

    intent, score = assistant.detect_intent("where is the washroom")
    assert intent == "washroom"

    intent, score = assistant.detect_intent("water refill station")
    assert intent == "water"

    intent, score = assistant.detect_intent("food and drinks")
    assert intent == "food"

    intent, score = assistant.detect_intent("wifi connection")
    assert intent == "wifi"

def test_answer_navigation_en():
    resp, intent = assistant.answer("where is gate 3", "North Upper", "English")
    assert intent == "gate"
    assert "Gate C" in resp

def test_answer_navigation_hinglish():
    resp, intent = assistant.answer("gate 3 kahan hai", "North Upper", "Hinglish")
    assert intent == "gate"
    assert "Gate C" in resp

def test_answer_navigation_hindi():
    resp, intent = assistant.answer("गेट 3 कहाँ है", "North Upper", "हिंदी")
    assert intent == "gate"
    assert "Gate C" in resp

def test_answer_water():
    resp, intent = assistant.answer("water refill", "North Upper", "English")
    assert intent == "water"
    assert "water" in resp.lower() or "refill" in resp.lower()

def test_answer_washroom():
    resp, intent = assistant.answer("where is washroom", "North Upper", "English")
    assert intent == "washroom"
    assert "washroom" in resp.lower() or "restroom" in resp.lower() or "level" in resp.lower()

def test_answer_emergency():
    resp, intent = assistant.answer("medical emergency", "North Upper", "English")
    assert intent == "emergency"
    assert "aid" in resp.lower() or "medical" in resp.lower() or "emergency" in resp.lower()

def test_quick_suggestions():
    sug_en = assistant.quick_suggestions("English")
    assert isinstance(sug_en, list)
    assert len(sug_en) > 0

    sug_hi = assistant.quick_suggestions("हिंदी")
    assert isinstance(sug_hi, list)
    assert len(sug_hi) > 0

    sug_hn = assistant.quick_suggestions("Hinglish")
    assert isinstance(sug_hn, list)
    assert len(sug_hn) > 0

def test_zone_items_filtering():
    items = assistant._zone_items(assistant.DATA["water_stations"], "North Upper")
    assert isinstance(items, list)
    assert len(items) > 0
