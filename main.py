import os

import nimb

nimb_token = os.getenv("NIMB")
nimb.nimb.run(nimb_token)