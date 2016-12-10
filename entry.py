import sys
sys.path.append("./models")

import profiles

id = 1436161156394835
profiles.init(1436161156394835)

profiles.updateLoc(id, 123123, 123123)
profiles.get(id)
profiles.updateParam(id, "first_name", "Something else")