import pytest

from chatovod.api.event_adapter import EventNotRegisteredError, EventsCollection


class BlankEvent:
    event_type = "blank"


class TestEventsCollection:
    def test_register_class(self):
        collection = EventsCollection()
        blank_event = collection.register(BlankEvent)

        assert BlankEvent is not None
        assert blank_event is not None
        assert len(collection.events_map) == 1
        assert collection.get_event_by_type("blank") == blank_event

    def test_get_event_by_type_raises_error_when_event_is_not_registered(self):
        collection = EventsCollection()

        with pytest.raises(EventNotRegisteredError):
            collection.get_event_by_type("invalid_event")
