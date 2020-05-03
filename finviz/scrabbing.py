import sys
from finviz import FinViz
import xlwt
import argparse
from threading import Thread
import time


def to_excel(filename, sheetname, keys, values, verbose=False):
    assert not (filename is None or filename == ''), 'filename is empty'
    assert not (sheetname is None or sheetname == ''), 'sheetname is empty'

    if len(keys) == 0 or len(values) == 0:
        return

    if verbose:
        print('Export to excel file =', filename, ' sheetname =', sheetname)

    wb = xlwt.Workbook()
    ws = wb.add_sheet(sheetname)
    percentage_style = xlwt.XFStyle()
    percentage_style.num_format_str = '0.00%'

    ws.write(0, 0, 'Ticker')
    for i in range(0, len(keys)):
        ws.write(0, i + 1, keys[i])

    line = 1
    for k, v in values.items():
        ws.write(line, 0, k)
        for i in range(0, len(v)):
            try:
                if '%' in v[i]:
                    ws.write(line,
                             i + 1,
                             float(v[i][:-1].strip()) / 100,
                             percentage_style)
                else:
                    ws.write(line, i + 1, float(v[i].strip()))
            except BaseException:
                ws.write(line, i + 1, v[i].strip())
        line += 1

    wb.save(filename)


def to_stdout(keys, values, space_char):
    if len(keys) == 0 or len(values) == 0:
        return

    print('Ticker', end=space_char)
    for i in range(0, len(keys)):
        print(keys[i], end=space_char)
    print()

    for k, v in values.items():
        print(k, end=space_char)
        for i in range(0, len(v)):
            print(v[i], end=space_char)
        print()

def get_args():
    parser = argparse.ArgumentParser(description='FinViz scrabing...')
    parser.add_argument(
        'tickers',
        help='tickers of shares, separated by space',
        nargs='+')
    parser.add_argument(
        '-v',
        '--verbose',
        help='show more information about program works',
        action='store_true')
    parser.add_argument(
        '--silent',
        help='drop all message to stdout',
        action='store_true')
    parser.add_argument(
        '--excel',
        help='export data in excel document',
        nargs=2,
        metavar=(
            'filename',
            'sheetname'))
    return parser.parse_args()

def main():
    args = get_args()
    keys = []
    values = {}

    tickers = ' '.join(args.tickers).split()

    if not args.silent:
        print(*tickers)

    if not args.silent:
        start_time = time.time()

    finviz = FinViz()
    threads = []
    for tic in tickers:
        t = Thread(target=finviz.scrab, args=(tic, keys, values))
        t.start()
        threads.append(t)

    for t in threads:
        t.join()

    # sort values by keys
    values = dict(sorted(values.items()))

    if args.verbose:
        print('values = ', values)

    if args.excel is None:
        to_stdout(keys, values, '\t')
    else:
        if not args.silent:
            print('exporting to', args.excel[0])
        to_excel(args.excel[0], args.excel[1], keys, values, args.verbose)

    if not args.silent:
        print(
            'scabbing completed. It takes {} seconds'.format(
                round(
                    time.time() -
                    start_time,
                    2)))


if __name__ == "__main__":
    main()
