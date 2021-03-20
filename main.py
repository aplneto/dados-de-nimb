import os

import nimb
from keep_alive import keep_alive

nimb_token = os.getenv("NIMB")

keep_alive()
nimb.nimb.run(nimb_token)