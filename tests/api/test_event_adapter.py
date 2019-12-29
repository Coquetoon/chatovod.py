import pytest

from chatovod.api.event_adapter import (
    API_EVENT_TYPE_ATTRIBUTE,
    EventAdapter,
    EventsCollection,
)


@pytest.fixture
def api_data():
    return {API_EVENT_TYPE_ATTRIBUTE: "r", "id": 123, "r": "Room name", "c": 100}


@pytest.fixture
def api_transform():
    return {"r": "room", "c": "users_count"}


class FakeAPIEvent:
    event_type = "u"
    transforms = {"i": "id", "u": "user"}


@pytest.fixture
def fake_api_data():
    return {API_EVENT_TYPE_ATTRIBUTE: FakeAPIEvent.event_type, "i": 1, "u": "Admin"}


class FakeAPIEventNewType:
    event_type = "u"
    new_type = "user"
    transforms = {"i": "id", "u": "user"}


@pytest.fixture
def fake_api_new_type_data():
    return {API_EVENT_TYPE_ATTRIBUTE: FakeAPIEvent.event_type, "i": 1, "u": "Admin"}


class TestEventAdapter:
    def test_transform(self, api_data: dict, api_transform: dict):
        event_adapter = EventAdapter(None)

        api_data_keys = api_data.keys()

        transformed_data = event_adapter.transform(api_data, api_transform)

        assert api_data_keys == api_data.keys()
        assert transformed_data == {
            API_EVENT_TYPE_ATTRIBUTE: "r",
            "id": 123,
            "room": "Room name",
            "users_count": 100,
        }

    def test_adapt(self, fake_api_data: dict):
        events_collection = EventsCollection()
        events_collection.register(FakeAPIEvent)

        event_adapter = EventAdapter(events_collection)

        adapted_data = event_adapter.adapt(fake_api_data)

        assert adapted_data == {
            API_EVENT_TYPE_ATTRIBUTE: FakeAPIEvent.event_type,
            "id": 1,
            "user": "Admin",
        }

    def test_adapt_new_type(self, fake_api_new_type_data: dict):
        events_collection = EventsCollection()
        events_collection.register(FakeAPIEventNewType)

        event_adapter = EventAdapter(events_collection)

        adapted_data = event_adapter.adapt(fake_api_new_type_data)

        assert adapted_data == {
            API_EVENT_TYPE_ATTRIBUTE: FakeAPIEventNewType.new_type,
            "id": 1,
            "user": "Admin",
        }
