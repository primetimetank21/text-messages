"""
This script
"""
import os
import sys
import datetime
import time
from dataclasses import dataclass


@dataclass
class MessageSender:
    """
    Bot that sends an iMessage
    """

    phone_number: str = ""
    message: str = ""
    delay: str | float = ""

    def _check_delay(self) -> bool:
        try:
            time_arr = self.delay.split(":")
        except Exception:  # pylint: disable=broad-except
            print("Delay improperly formatted (should be 'hours:mins:secs(opt)')")
            return False

        if not 2 <= len(time_arr) <= 3:
            print("Delay improperly formatted (should be 'hours:mins:secs(opt)')")
            return False

        for i, time_slice in enumerate(time_arr):
            if not isinstance(int(time_slice), int):
                print(
                    "Delay improperly formatted (hours, mins, and secs should all be numbers)"
                )
                return False
            if int(time_slice) < 0:
                print(
                    "Delay improperly formatted (hours, mins, and secs should all be positive numbers)"  # pylint: disable=line-too-long
                )
                return False
            time_arr[i] = int(time_slice)
        self.delay = self._convert(time_arr)
        return True

    def _convert(self, time_arr: list[int]) -> float:
        """
        Converts time array given into seconds
        """
        self.delay: float
        time_str = time.strptime(
            f"{time_arr[0]}:{time_arr[1]}:{time_arr[2] if len(time_arr) == 3 else 0},end".split(
                ","
            )[
                0
            ],
            "%H:%M:%S",
        )
        return datetime.timedelta(
            hours=time_str.tm_hour, minutes=time_str.tm_min, seconds=time_str.tm_sec
        ).total_seconds()

    def _check_phone_number(self) -> bool:
        if len(self.phone_number) != 10:
            print("Phone number improperly formatted (should be 10 digits long)")
            return False

        for num in self.phone_number:
            try:
                if not isinstance(int(num), int):
                    raise Exception
            except Exception:  # pylint: disable=broad-except
                print("Phone number improperly formatted (illegal character found)")
                return False
        return True

    def _check_message(self) -> bool:
        if len(self.message) == 0:
            print("Message has no content")
            return False
        return True

    def _verify_checks(self) -> bool:
        return (
            self._check_phone_number() and self._check_message() and self._check_delay()
        )

    def _check_input(self) -> bool:
        if len(sys.argv) != 4:
            return False

        try:
            num, msg, delay = sys.argv[1:]  # pylint: disable=unbalanced-tuple-unpacking
        except Exception as exception:  # pylint: disable=broad-except
            print(exception)
            sys.exit(-1)

        self.phone_number, self.message, self.delay = num, msg, delay

        if not self._verify_checks():
            return False

        return True

    def _send_message(self) -> None:
        try:
            time.sleep(self.delay)
            os.system(f'osascript send.scpt {self.phone_number} "{self.message}"')
        except Exception as exception:  # pylint: disable=broad-except
            print(f"Something went wrong: {exception}")
            cur_time = datetime.datetime.now().strftime("%m-%d-%y_at_%H%M")
            with open(f"./logs/{cur_time}.log", "w", encoding="utf-8") as logger:
                logger.write(str(exception) + "\n")

    def run(self) -> None:
        """
        Starts the message sender
        """
        if not self._check_input():
            print(
                'Proper usage: \'python3 main.py "1235556789" "Message to send" "hours(req):mins(req):secs(opt)"\''  # pylint: disable=line-too-long
            )
            sys.exit(-1)
        print(f"Success! Good to send ({self})")
        self._send_message()


if __name__ == "__main__":
    sender = MessageSender()
    sender.run()
