from collections import defaultdict
from datetime import datetime, timedelta, time
from decimal import Decimal, ROUND_UP

class DeliverySystem:
    def __init__(self):
        self.drivers = {}
        self.deliveries = defaultdict(list)

    def add_driver(self, driver_id: int, rate: float):
        self.drivers[driver_id] = rate

    def add_delivery(self, driver_id: int, start: datetime, end: datetime):
        self.deliveries[driver_id].append((start, end))

    def get_total(self):
        total = 0.0
        for driver_id, jobs in self.deliveries.items():
            rate = self.drivers.get(driver_id, 0)
            for job in jobs:
                start, end = job
                delta: timedelta = end - start
                if delta.total_seconds() > 10800:
                    delta = timedelta(hours=3)
                seconds_worked = delta.total_seconds()
                rate_per_second = rate / 3600.0
                total += seconds_worked * rate_per_second
        total = float(Decimal(total).quantize(Decimal('0.01'), rounding=ROUND_UP))
        print(f"Total payout: ${total}")
            



ds = DeliverySystem()
from datetime import datetime

# Add drivers
ds.add_driver("alice", 30.12)
ds.add_driver("bob", 20.99)
ds.add_driver("carol", 25.38)

# Add deliveries with second-level precision
ds.add_delivery("alice",
    datetime(2025, 11, 18, 9, 0, 15),
    datetime(2025, 11, 18, 10, 30, 45))  # 1h 30m 30s

ds.add_delivery("bob",
    datetime(2025, 11, 18, 10, 15, 0),
    datetime(2025, 11, 18, 12, 45, 30))  # 2h 30m 30s

ds.add_delivery("carol",
    datetime(2025, 11, 18, 13, 0, 0),
    datetime(2025, 11, 18, 13, 45, 0))   # 45m

ds.add_delivery("alice",
    datetime(2025, 11, 18, 14, 0, 0),
    datetime(2025, 11, 18, 14, 15, 30))  # 15m 30s

ds.add_delivery("bob",
    datetime(2025, 11, 18, 14, 0, 0),
    datetime(2025, 11, 18, 19, 15, 30))  # 5h 15m 30s

ds.get_total()
