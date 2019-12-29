from .event_adapter import EventsCollection

APIEvents = EventsCollection()


@APIEvents.register
class SetOptionEvent:
    event_type = "so"
    new_type = "set_option"
    transforms = {"k": "option", "v": "value"}


@APIEvents.register
class CLSEvent:
    event_type = "cls"
    transforms = {
        "accountName": "email",
        "accountType": "account_type",
        "accountGroup": "user_group",
        "lastNick": "last_nickname",
    }


@APIEvents.register
class ChatEmojisEvent:
    event_type = "sl"
    new_type = "chat_emojis"
    transforms = {
        "smileys": "emojis",
        "cats": "groups",
        "dp": "default_path",
        "p": "custom_path",
    }


@APIEvents.register
class ErrorEvent:
    event_type = "error"
    transforms = {
        "et": "type",
        "est": "group",
        "error": "description",
        "r": "room_id",
        "ts": "timestamp",
    }


@APIEvents.register
class MessageEvent:
    event_type = "m"
    new_type = "message"
    transforms = {
        "ts": "timestamp",
        "f": "author",
        "m": "content",
        "r": "room_id",
        "actions": "actions",
    }


@APIEvents.register
class MessageDeleteEvent:
    event_type = "md"
    new_type = "message_delete"
    transforms = {"ts": "messages", "r": "room_id"}


@APIEvents.register
class MessageReadEvent:
    event_type = "pmr"
    new_type = "message_read"
    transforms = {"fromTime": "from_ts", "toTime": "until_ts"}


@APIEvents.register
class RoomUpdateEvent:
    event_type = "ru"
    new_type = "room_update"
    transforms = {"closeable": "can_be_closed", "showEnterLeave": "display_user_flow"}


@APIEvents.register
class RoomOpenEvent:
    event_type = "ro"
    new_type = "room_open"
    transforms = {
        "r": "room_id",
        "channelType": "type",
        "active": "set_focus",
        "title": "name",
        "closeable": "can_be_closed",
        "showEnterLeave": "display_user_flow",
    }


@APIEvents.register
class RoomCloseEvent:
    event_type = "rc"
    new_type = "room_close"
    transforms = {"r": "room_id", "iwid": "window_id"}


@APIEvents.register
class HasOlderEventsEvent:
    event_type = "hoe"
    new_type = "has_older_events"
    transforms = {"r": "room_id", "hasOlderEvents": "value"}


@APIEvents.register
class UserLeaveEvent:
    event_type = "ul"
    new_type = "user_leave"
    transforms = {"nick": "nickname"}


@APIEvents.register
class UserEnterEvent:
    event_type = "ue"
    new_type = "user_enter"
    transforms = {}


@APIEvents.register
class UserEnterRoomEvent:
    event_type = "uer"
    new_type = "user_enter_room"
    transforms = {}


@APIEvents.register
class UserLeaveRoomEvent:
    event_type = "ulr"
    new_type = "user_leave_room"
    transforms = {}
