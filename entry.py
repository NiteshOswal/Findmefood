import sys
sys.path.append("./models")

import profiles

id = 1436161156394835
profiles.init(1436161156394835)

profiles.delete(id)

profiles.init(1436161156394835)
