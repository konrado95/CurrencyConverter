import json
import requests
import Converter


class Currency:
    def __init__(self, name, code, rate):
        self.name = name
        self.code = code
        self.rate = rate

    def convert(self, target_currency, amount):
        return amount * self.rate / target_currency.rate


def download_currencies(url="http://api.nbp.pl/api/exchangerates/tables/A?format=json"):
    page = requests.get(url)
    content = json.loads(page.text)[0]
    currencies = []
    date = content["effectiveDate"]
    for curr in content["rates"]:
        name = curr["currency"]
        code = curr["code"]
        rate = float(curr["mid"])
        currencies.append(Currency(name, code, rate))
    currencies.insert(0, Currency("Polski złoty", "PLN", 1))
    return {"date": date, "rates": currencies}


if __name__ == "__main__":
    app = Converter.Converter(download_currencies())
    app.mainloop()
