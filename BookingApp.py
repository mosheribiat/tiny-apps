# Process the list of booking lines for a hotel with 5 rooms.
# A client must be booked in a single room for the entire booked period.
# Return the room the booking will get and if all rooms cannot be filled return the NO_ROOM_AVAIL error.
# For invalid lines return the applicable error reponse.

from collections import defaultdict
from dataclasses import dataclass
from datetime import datetime, date, timedelta
from typing import Tuple

@dataclass
class Booking:
    start: date
    end: date

class BookingApp:
    MAX_ROOMS = 5
    error_response = {
        "INVALID_INPUT":"input is not a valid date",
        "INVALID_RANGE":"date range is invalid",
        "NO_ROOM_AVAIL":"no rooms available for this date range"
    }

    report = []
    calendar = defaultdict(set)
    def parse_input(self, line: str) -> Tuple[Booking, str]:
        dates = line.split(" ")
        if len(dates) != 2:
            return (None, self.error_response["INVALID_INPUT"])
        try:
            start = datetime.strptime(dates[0], "%Y-%m-%d").date()
            end = datetime.strptime(dates[1], "%Y-%m-%d").date()
            return (Booking(start, end), "")
        except ValueError:
            return (None, self.error_response["INVALID_INPUT"])

    def get_available_room(self, booking: Booking):
        days_in_booking = (booking.end - booking.start).days 
        date_range = [booking.start + timedelta(days=i) for i in range(days_in_booking+1)]
        for i in range(1, self.MAX_ROOMS+1):
            available = all(i not in self.calendar[dt] for dt in date_range)
            if available:
                return i
        return 0

    def book_rooms(self, input: str):
        input_lines = input.splitlines()
        for line in input_lines:
            booking, error_msg = self.parse_input(line)
            if error_msg:
                report_str = f"{line} - {error_msg}"
                self.report.append(report_str)
                continue
            if booking.start >= booking.end:
                report_str = f"{line} - {self.error_response["INVALID_RANGE"]}"
                self.report.append(report_str)
                continue
            room = self.get_available_room(booking)
            if not room:
                report_str = f"{line} - {self.error_response["NO_ROOM_AVAIL"]}"
                self.report.append(report_str)
            else:
                days_in_booking = (booking.end - booking.start).days 
                date_range = [booking.start + timedelta(days=i) for i in range(days_in_booking+1)]
                for dt in date_range:
                    self.calendar[dt].add(room)
                report_str = f"{line} - {room}"
                self.report.append(report_str)

    def print_report(self):
        for line in self.report:
            print(line)

booking_lines = """\
2025-11-19 2025-11-23
2025-11-19 2025-11-23
2025-11-19 2025-11-23
2025-11-19 2025-11-23
2025-11-19 2025-11-23
2025-11-19 2025-11-23
2025-11-24 2025-11-25
2025-11-28 2025-12-03
2025-11-22 2025-11-23
2025-11-26 2025-11-27
2025-11-25 2025-11-26
2025-12-02 2025-11-04
2025-12-01 2025-11-03
2025-12-19 2025-11-23
2025-11-24 2025-11-25
2025-11-28 2025-12-03
2025-11-25 2025-11-24
2025-11-44 2025-11-25
2025-11-25
2025-12-01 2025-12-01
"""

ba = BookingApp()
ba.book_rooms(booking_lines)
ba.print_report()


