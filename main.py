import tkinter as tk
from tkinter import ttk, messagebox
import json
import requests


class Currency:
    def __init__(self, name, code, rate):
        self.name = name
        self.code = code
        self.rate = rate

    def convert(self, target_currency, amount):
        return amount * self.rate / target_currency.rate


class Converter(tk.Tk):

    def __init__(self, data):
        super().__init__()
        self.date = data["date"]
        self.rates = data["rates"]

        self.title("Przelicznik walut")
        self.geometry("480x360")

        self.menubar = tk.Menu(self)
        self.menubar.add_command(label="Objaśnienia skrótów", command=self.open_codes)
        self.menubar.add_command(label="Tabela kursów", command=self.open_table)
        self.config(menu=self.menubar)

        self.info_label = tk.Label(self, text=f"Kursy walut z dnia {self.date}", font=("Arial", 12))
        self.info_label.grid(row=0, column=0, columnspan=3, sticky='N')

        self.base_curr_entry = tk.Entry(self, width=20, font=("Arial", 20), justify="right")
        self.base_curr_entry.grid(row=1, column=0, columnspan=2, padx=10, pady=10)

        self.target_curr_entry = tk.Entry(self, width=20, font=("Arial", 20), justify="right",
                                          state="readonly")
        self.target_curr_entry.grid(row=3, column=0, columnspan=2, padx=10, pady=10)

        self.base_curr_list = ttk.Combobox(width=5, font=("Arial", 20), state="readonly")
        self.base_curr_list["values"] = [currency.code for currency in self.rates]
        self.base_curr_list.grid(row=1, column=2, padx=10, pady=10)

        self.target_curr_list = ttk.Combobox(width=5, font=("Arial", 20), state="readonly")
        self.target_curr_list["values"] = [currency.code for currency in self.rates]
        self.target_curr_list.grid(row=3, column=2, padx=10, pady=10)

        self.calculation_button = tk.Button(self, text="PRZELICZ!", font=("Arial", 14),
                                            command=self.convert_currency)
        self.calculation_button.grid(row=2, column=0, columnspan=3, padx=10, pady=10)

    def open_codes(self):
        top = tk.Toplevel()
        top.title("Objaśnienia skrótów")
        for currency in self.rates:
            curr_label = tk.Label(top, text=f'{currency.code} -> {currency.name}')
            if self.rates.index(currency) < len(self.rates) / 2:
                column = 0
                row = self.rates.index(currency)
            else:
                column = 1
                row = self.rates.index(currency) - round((len(self.rates) / 2))
            curr_label.grid(row=row, column=column, padx=5, pady=5, sticky='W')

    def open_table(self):
        top = tk.Toplevel()
        top.title("Tabela kursów walut")
        for currency in self.rates:
            if currency.code == "PLN":
                continue
            rate_label = tk.Label(top, text=f"{currency.name} ({currency.code}) -> {currency.rate}")
            if self.rates.index(currency) < len(self.rates) / 2:
                column = 0
                row = self.rates.index(currency)
            else:
                column = 1
                row = self.rates.index(currency) - round((len(self.rates) / 2))
            rate_label.grid(row=row, column=column, padx=5, pady=5, sticky='W')

    def convert_currency(self):
        self.target_curr_entry.config(state="normal")
        self.target_curr_entry.delete(0, tk.END)
        try:
            amount = float(self.base_curr_entry.get().replace(',', '.'))
        except ValueError:
            messagebox.showerror("Conversion error", "Wprowadź prawidłową wartość!")
            return
        if amount < 0:
            messagebox.showerror("Conversion error", "Wprowadzono ujemną wartość!")
            return
        base_curr_code = self.base_curr_list.get()
        target_curr_code = self.target_curr_list.get()
        codes = [currency.code for currency in self.rates]
        if base_curr_code == "" or target_curr_code == "":
            messagebox.showerror("Conversion error", "Nie wybrano walut!")
            return
        base_currency = self.rates[codes.index(base_curr_code)]
        target_currency = self.rates[codes.index(target_curr_code)]
        self.target_curr_entry.insert(0, str(round(base_currency.convert(target_currency, amount), 2)))
        self.target_curr_entry.config(state="readonly")


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
    app = Converter(download_currencies())
    app.mainloop()
