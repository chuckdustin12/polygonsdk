"DOWNLOADS GDP DATA"

import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))



from sdks.nasdaq_sdk.sdk import Nasdaq


nasdaq = Nasdaq()

gdp = nasdaq.gdp()
print(gdp)