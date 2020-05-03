from urllib.request import urlopen, Request
from bs4 import BeautifulSoup


class FinViz:
    def __init__(self, url=None, user_agent=None):
        self.url = url or 'https://finviz.com/quote.ashx?t='
        self.user_agent = user_agent or 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:75.0) Gecko/20100101 Firefox/75.0'

    def scrab(self, tic, keys, values):
        assert not (tic is None or tic == ''), 'tic is empty'

        source_url = ''.join([self.url, tic])

        response = urlopen(
            Request(
                source_url, headers={
                    'User-Agent': self.user_agent}))
        html = response.read().decode('utf8')
        soup = BeautifulSoup(html, 'html5lib')
        table = soup.find('table', attrs={'class': 'snapshot-table2'})

        if len(keys) == 0:
            for td in table.find_all('td', attrs={'class': 'snapshot-td2-cp'}):
                keys.append(td.get_text())

        value = []
        for td in table.find_all('td', attrs={'class': 'snapshot-td2'}):
            value.append(td.get_text())

        for i in range(0, len(keys)):
            if keys[i] == 'Volatility':
                keys[i] = 'Volatility Week'
                keys.insert(i + 1, 'Volatility Month')
            if keys[i] == 'Volatility Week':
                v = value[i].split()
                value[i] = v[0]
                value.insert(i + 1, v[1])

        values[tic] = value
