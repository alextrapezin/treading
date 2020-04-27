from urllib.request import urlopen, Request
from bs4 import BeautifulSoup

SOURCE_URL = 'https://finviz.com/quote.ashx?t='
USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:75.0) Gecko/20100101 Firefox/75.0'


def scrab(tic, keys, verbose=False):
    if len(tic) == 0:
        raise ValueError('Scrabing needs TIC')

    source_url = ''.join([SOURCE_URL, tic])

    if verbose:
        print('get webpage from', source_url)

    response = urlopen(Request(source_url, headers={'User-Agent': USER_AGENT}))

    html = response.read().decode('utf8')

#    if verbose:
#        print(html)

    soup = BeautifulSoup(html, 'html5lib')

    table = soup.find('table', attrs={'class': 'snapshot-table2'})
    if len(keys) == 0:
        for td in table.find_all('td', attrs={'class': 'snapshot-td2-cp'}):
            keys.append(td.get_text())

    values = []
    for td in table.find_all('td', attrs={'class': 'snapshot-td2'}):
        values.append(td.get_text())

    for i in range(0, len(keys)):
        if keys[i] == 'Volatility':
            keys[i] = 'Volatility Week'
            keys.insert(i + 1, 'Volatility Month')
        if keys[i] == 'Volatility Week':
            v = values[i].split()
            values[i] = v[0]
            values.insert(i + 1, v[1])
    return keys, values
