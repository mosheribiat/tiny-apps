from datetime import datetime, date
from dataclasses import dataclass, field
from typing import Dict, Optional, List

class OrderParser:
    @staticmethod
    def parse_many(input_str: str, delimiter: str = "||") -> List[Order]:
        return [Order.from_string(order.strip()) for order in input_str.split(delimiter) if order.strip()]


@dataclass(order=True)
class Order:
    sort_index: int = field(init=False, repr=False, compare=True)

    order_id: int = field(compare=False)
    customer: str
    delivery_date: date
    items: Dict[str, int] = field(default_factory=dict)
    notes: Optional[str] = None

    _required_keys = {"order_id", "customer", "items", "delivery_date"}
    _optional_keys = {"notes"}
    _all_keys = _required_keys | _optional_keys

    @classmethod
    def validate(cls, parts):
        found_keys = {part.split("=", 1)[0] for part in parts}
        missing = cls._required_keys - found_keys
        if missing:
            raise ValueError(f"Missing required keys: {missing}")
        unexpected = found_keys - cls._all_keys
        if unexpected:
            raise ValueError(f"Unexpected keys: {unexpected}")

            
    @classmethod
    def from_string(cls, input_str: str):
        parts = input_str.split(";")
        cls.validate(parts)
        data = {}
        for part in parts:
            key, value = part.split("=", 1)

            if key == "items":
                items = {}
                for item in value.split(","):
                    try:
                        name, count = item.split(":")
                        items[name] = int(count)
                    except ValueError:
                        raise ValueError(f"Invalid item format: '{item}'")
                data["items"] = items

            elif key == "order_id":
                if key in data:
                    raise ValueError(f"Duplicate key: {key}")
                try:
                    data[key] = int(value)
                except ValueError:
                    raise ValueError(f"Invalid order_id:{value}")
                
            elif key == "delivery_date":
                try:
                    data[key] = datetime.strptime(value, "%Y-%m-%d").date()
                except ValueError:
                    raise ValueError(f"Invalid date format: {value}")

            else:
                data[key] = value

        return cls(**data)


    def to_string(self):
        lines = [
            f"Order #{self.order_id}",
            f"Customer: {self.customer}",
            f"Delivery Date: {self.delivery_date.strftime('%Y-%m-%d')}",
            f"Items: {', '.join(f'{k}: {v}' for k, v in self.items.items())}"
        ]
        for field_name in self.__dataclass_fields__:
            if field_name in {"order_id", "customer", "delivery_date", "items", "sort_index"}:
                continue  # already printed
            value = getattr(self, field_name)
            if value is not None:
                lines.append(f"{field_name.replace('_', ' ').title()}: {value}")
        return "\n".join(lines)

    def total_quantity(self):
        return sum(self.items.values())

    def __str__(self):
        return self.to_string()

    def __post_init__(self):
        self.sort_index = self.total_quantity()


    
# run the code
input = "order_id=1234;customer=Jane Doe;items=beef:2,chicken:1;delivery_date=2025-11-10;notes=Leave at front door"
input2 = "order_id=1;customer=Jane;items=beef:2,chicken:2;delivery_date=2025-11-10||order_id=2;customer=Moshe;items=chicken:4;delivery_date=2025-11-12"
print(Order.from_string(input))
orders = OrderParser.parse_many(input2, "||")
sorted_orders = sorted(orders)
for order in sorted_orders:
    print("------------------------------")
    print(order)
    print("------------------------------\n")