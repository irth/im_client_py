from im_client import proto


def test_validate_event():
    assert proto.validate_event({}) is False
    assert proto.validate_event({"name": "not_reserverd"}) is True
    assert proto.validate_event({"name": "MESSAGE"}) is False
    assert proto.validate_event({"name": "message"}) is True

    assert proto.validate_event({"name": "MESSAGE",
                                 "from": "whoever",
                                 "to": "wherever",
                                 "text": "whatever"}) is True

    assert proto.validate_event({"name": "MESSAGE",
                                 "to": "wherever",
                                 "text": "whatever"}) is False

    assert proto.validate_event({"name": "MESSAGE",
                                 "from": "whoever",
                                 "text": "whatever"}) is False

    assert proto.validate_event({"name": "MESSAGE",
                                 "from": "whoever",
                                 "to": "wherever"}) is False

