import asyncio
import datetime
import os
import atexit
import logging
import sys
import traceback
from dotenv import load_dotenv
from nio import AsyncClient, MatrixRoom, RoomMessageText

load_dotenv()
PROG_WITHOUT_EXT = os.path.splitext(os.path.basename(__file__))[0]


async def main() -> None:
    logger = logging.getLogger(PROG_WITHOUT_EXT)
    client = AsyncClient("https://matrix.org", os.environ.get("MATRIX_USER"))
    print(await client.login(os.environ.get("MATRIX_PASSWORD")))

    callbacks = Callbacks(client)

    client.add_event_callback(callbacks.message_callback, RoomMessageText)

    sync_response = await client.sync_forever(timeout=30000)  # milliseconds


async def message_callback(room: MatrixRoom, event: RoomMessageText) -> None:
    print(
        f"Message received in room {room.display_name}\n"
        f"{room.user_name(event.sender)} | {event.body}"
    )


class Callbacks(object):
    """Class to pass client to callback methods."""

    def __init__(self, client: AsyncClient):
        """Store AsyncClient."""
        self.client = client

    async def message_callback(self, room: MatrixRoom, event):
        """
        Handle all events of type RoomMessage.
        Includes events like RoomMessageText, RoomMessageImage, etc.
        """
        try:
            logger.debug(
                f"message_callback(): for room {room} received this "
                f"event: type: {type(event)}, event_id: {event.event_id}, "
                f"event: {event}"
            )
            logger.debug(f"event.server_timestamp = {event.server_timestamp}")
            timestamp = datetime.datetime.fromtimestamp(
                int(event.server_timestamp / 1000)
            )  # sec since 1970
            event_datetime = timestamp.strftime("%Y-%m-%d %H:%M:%S")
            # e.g. 2020-08-06 17:30:18
            logger.debug(f"event_datetime = {event_datetime}")

            print(
                f"Message received in room {room.display_name}\n"
                f"{room.user_name(event.sender)} | {event.body}"
            )

            if event.sender == "@itsmaleen:matrix.org":
                await self.client.room_send(
                    # Watch out! If you join an old room you'll see lots of old messages
                    room_id=room.room_id,
                    message_type="m.room.message",
                    content={
                        "msgtype": "m.text",
                        "body": "Hello world!"
                    }
                )

        except BaseException:
            logger.debug(traceback.format_exc())


if __name__ == "__main__":
    logging.basicConfig(  # initialize root logger, a must
        format="{asctime}: {levelname:>8}: {name:>16}: {message}", style="{"
    )
    logging.getLogger().setLevel(logging.INFO)

    logger = logging.getLogger(PROG_WITHOUT_EXT)
    asyncio.run(main())
    sys.exit(1)
