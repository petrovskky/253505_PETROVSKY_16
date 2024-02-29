import os
import circle
import square


shape = os.environ.get("SHAPE")
calculation = os.environ.get("CALCULATION")
size = float(os.environ.get("SIZE"))

functions = {
    ("circle", "area"): circle.area,
    ("circle", "perimeter"): circle.perimeter,
    ("square", "area"): square.area,
    ("square", "perimeter"): square.perimeter
}

function = functions.get((shape, calculation))

print(function(size))
