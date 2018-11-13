import requests

import json
import os

class Finviz:
    # URL = "http://localhost:8080/finance/finviz/statistics"
    URL = os.environ.get('FINVIZ_URI')

    def __init__(self):
        pass

    def get_stat(self, symbol):
        url = "{}/{}".format(self.URL, symbol)
        r = requests.get(url)
        if r.status_code == 200:
            astr = r.text
            astr = astr.replace("Oper. Margin", "Oper Margin")
            jobj = json.loads(astr)
            return jobj
        else:
            return None

if __name__ == "__main__":
    f = Finviz()
    print(f.get_stat('HSDT'))
