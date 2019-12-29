import asyncio
import logging
from collections import OrderedDict, defaultdict

from chatovod.api.event_adapter import EventAdapter
from chatovod.structures.room import Room

from .errors import ChatovodConnectionError, ConnectionReset

log = logging.getLogger(__name__)


class Chat:
    def __init__(self, client, user, http, loop):
        self.client = client
        self.user = user
        self.loop = loop
        self._http = http
        self._event_listener = EventListener(chat=self)
        self._event_handler = EventHandler(chat=self)

        self.reset()

    def reset(self):
        self._users = OrderedDict()
        self._rooms = OrderedDict()
        self._emojis = []
        self._emojis_groups = []
        self._emojis_base_path = None
        self._custom_emojis_base_path = None
        self._messages_to_delete = []

    @property
    def url(self):
        return self._http.url

    def _get_user(self, nickname):
        return self.users[nickname.lower()]

    def _add_user(self, user):
        nickname = user.nickname.lower()
        self._users[nickname] = user

    def _remove_user(self, user):
        return self._users.pop(user.nickname.lower())

    def _get_room(self, room_id):
        return self._rooms.get(room_id)

    def _add_room(self, room):
        self._rooms[room.id] = room

    def _remove_room(self, room):
        self._rooms.pop(room.id)

    def _add_message_to_delete(self, message):
        self._messages_to_delete.append(message)

    async def _delete_deferred_messages(self):
        messages_to_delete = self._messages_to_delete
        messages_by_room = defaultdict(list)

        for message in messages_to_delete:
            messages_by_room[message.room.id].append(message.id)

        messages_to_delete.clear()

        for room_id, messages in messages_by_room.items():
            log.debug("Deleting deferred messages from %s", room_id)
            await self._http.delete_messages(room_id, messages)

    async def _start(self):
        await self._http.fetch_session()
        info = await self._http.fetch_info()
        await self._event_handler.handle_start(info)

    def _create_room(self, data):
        room = Room(data=data)
        return room


class EventListener:
    def __init__(self, chat, *args, **kwargs):
        self.chat = chat

    async def listen(self):
        try:
            coro = self.chat._http.chat_bind()
            msg_stream = await asyncio.wait_for(coro, timeout=80, loop=self.chat.loop)
            await self.received_message(msg_stream)
        except (ConnectionReset, ChatovodConnectionError) as e:
            log.warning("A %s error occurred during event bind", e.__name__)
            raise

    async def received_message(self, msg_stream):
        if not isinstance(msg_stream, list):
            log.warning("Received %s with content %s", type(msg_stream), msg_stream)
            raise Exception

        for data in msg_stream:
            adapted_data = EventAdapter.adapt(data)

            event = adapted_data.get("t")
            parser = "parse_" + event.lower()

            try:
                parser_func = getattr(self.chat._event_handler, parser)
            except AttributeError:
                log.warning('Unknown event "%s"', event)
            else:
                parser_func(adapted_data)


class EventHandler:
    def __init__(self, chat):
        self.chat = chat

    async def handle_start(self, msg_stream):
        for data in msg_stream:
            adapted_data = EventAdapter.adapt(data)
            event = adapted_data.get("t")
            # parser = "_parse_" + event

            if event == "room_open":
                room = self.chat._create_room(adapted_data)
                self.chat._add_room(room)
            elif event == "message":
                # message = self.chat._create_message(message)
                # self.chat._cache_message(message)
                ...
            elif event == "has_older_events":
                # TODO: Implement this
                ...
            # else:
            #     try:
            #         parser_func = getattr(self, parser)
            #     except AttributeError:
            #         log.debug("Unhandled event on start %s", adapted_data)
            #     else:
            #         parser_func(raw)

        log.info("Handle start finished")

    def _parse_message(self, data):
        message = self.chat._create_message(data)

        return message

    def parse_set_option(self, raw):
        option = raw["option"]
        value = raw.get("value")

        log.debug("Setting option '%s' to '%s'", option, value)

        if option == "nick":
            self.user.nickname = value
        elif option == "signedIn":
            self.user.signed_in = value
        elif option == "wid":
            self._http.window_id = value
        else:
            log.info("Unhandled option %s:%s", option, raw)

    def handle_chat_emojis(self, raw):
        self._emojis_base_path = raw["default_path"]
        self._custom_emojis_base_path = raw.get("custom_path")

        for raw_group in raw["groups"]:
            group = self._create_emoji_group(raw_group)
            self._add_emoji_group(group)

        for raw_emoji in raw["emojis"]:
            emoji = self._create_emoji(raw_emoji)
            self._add_emoji(emoji)

    def handle_error(self, raw):
        ...

    def handle_room_open(self, event):
        pass
