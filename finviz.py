from urllib.request import urlopen, Request
from bs4 import BeautifulSoup
import time


class FinViz:
    def __init__(self, tic, url=None, user_agent=None):
        assert not (tic is None or tic == ''), 'tic is empty'
        self.tic = tic
        self.url = url or f'https://finviz.com/quote.ashx?t={tic}'
        self.user_agent = user_agent or 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:75.0) Gecko/20100101 Firefox/75.0'
        self.keys = []
        self.values = {}

    def _convert_value(self, value):
        value = value.replace(",", "")
        try:
            if value[-1:] == 'B':
                value = int(float(value[:-1]) * 1000000000)
            elif value[-1:] == 'M':
                value = int(float(value[:-1]) * 1000000)
            elif value[-1:] == '%':
                value = round(float(value[:-1]) / 100, 4)
            else:
                value = round(float(value), 2)
        except ValueError:
            pass
        return value

    def _get_table(self):
        response = urlopen(
            Request(
                self.url, headers={
                    'User-Agent': self.user_agent}))
        html = response.read().decode('utf8')
        soup = BeautifulSoup(html, 'html5lib')
        self.table = soup.find('table', attrs={'class': 'snapshot-table2'})

    def _get_keys(self):
        for td in self.table.find_all('td', attrs={'class': 'snapshot-td2-cp'}):
            _key = td.get_text()
            if _key == 'Volatility':
                self.keys.append('Volatility Week')
                self.keys.append('Volatility Month')
            else:
                self.keys.append(_key)

    def _get_values(self):
        self.values['datatime'] = time.time()
        idx = 0
        for td in self.table.find_all('td', attrs={'class': 'snapshot-td2'}):
            _value = td.get_text().strip()
            if self.keys[idx] == 'Volatility Week':
                v = _value.split()
                _value = v[0].strip()
                self.values[self.keys[idx]] = self._convert_value(_value)
                idx += 1
                _value = v[1].strip()
            self.values[self.keys[idx]] = self._convert_value(_value)
            idx += 1

        # convert very important values
        for k, v in self.values.items():
            if v == '-':
                if k == 'Target Price':
                    self.values[k] = self.values['Price']
                elif k == 'Beta':
                    self.values[k] = 1

    def _calc_values(self):
        # calculate Buying_price and Technical_idea     !!! VERY SIMPLE, JUST INFORMATION !!!
        self.values['Buying price'] = round(
            self.values['Target Price'] - self.values['ATR'] * 4, 2)
        if self.values['SMA20'] > 0 and self.values['SMA50'] > 0 and self.values[
                'SMA200'] > 0 and self.values['RSI (14)'] > 55 and self.values['Buying price'] >= self.values['Price']:
            self.values['Technical idea'] = 'buy'
        else:
            if self.values['Buying price'] < self.values['Price']:
                self.values['Technical idea'] = 'wait'
            else:
                self.values['Technical idea'] = 'sell'


    def get_values(self):
        self._get_table()
        self._get_keys()
        self._get_values()
        self._calc_values()
        return self.values
