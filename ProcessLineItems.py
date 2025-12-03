# Given a list of line where the cpt can either be a main cpt or an add-on. An add-on can only be paid if there is a line item for its main cpt. The
# dependecies contain a mapping of parent to child. Parent is the key and the child is the value. If the parent is not paid then the child cannot be paid.
# a main will always only be in the key column. Any cpt that is not in the dependencies at all is a main and will be paid.
# There will be no circular dependencies. If an add-ons parent is not paid, because it is not in the line items then the add-on will not be paid either.

from collections import defaultdict

line_items = [
    {"line_number": 1, "cpt": "A1"},
    {"line_number": 2, "cpt": "P1"},
    {"line_number": 3, "cpt": "P2"},
    {"line_number": 4, "cpt": "A4"},
    {"line_number": 5, "cpt": "A2"},
    {"line_number": 6, "cpt": "XYZ"},
    {"line_number": 7, "cpt": "A5"}
]

# Dependencies listed as parent → child
dependencies = [
        {"P1": "A2"},
        {"A2": "A4"},
        {"P2": "A1"},
        {"P3": "A5"}
    ]


li_cpts = {li["cpt"] for li in line_items}

dependency_map = {}
for dependency in dependencies:
    for k, v in dependency.items():
        dependency_map[v] = k

paid = set()

for cpt in li_cpts:
    if cpt not in dependency_map:
        paid.add(cpt)

changed = True
while changed:
    changed = False
    for li in line_items:
        cpt = li["cpt"]
        if cpt not in paid and cpt in dependency_map:
            if dependency_map[cpt] in paid:
                paid.add(cpt)
                changed = True


for li in line_items:
    if li["cpt"] in paid:
        print(f"line_number-{li["line_number"]} for cpt {li["cpt"]} has been paid")
    else:
        print(f"line_number-{li["line_number"]} for cpt {li["cpt"]} has been denied")
