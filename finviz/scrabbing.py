import sys
import finviz
import xlwt

def to_excel(filename, sheetname, keys, values, verbose=False):
    if verbose:
        print('Export to excel file =', filename, ' sheetname =', sheetname)
    if len(filename) == 0 or len(sheetname) == 0 or len(keys) == 0 or len(values) == 0:
        raise ValueError('Export needs filename, sheetname, keys and values')
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
                    ws.write(line, i + 1, float(v[i][:-1].strip())/100, percentage_style)
                else:
                    ws.write(line, i + 1, float(v[i].strip()))
            except:
                ws.write(line, i + 1, v[i].strip())
        line += 1

    wb.save(filename)

def to_stdout(keys, values, space_char, verbose=False):
    print('Ticker', end=space_char)
    for i in range(0, len(keys)):
        print(keys[i], end=space_char)
    print()

    for k, v in values.items():
        print(k, end=space_char)
        for i in range(0, len(v)):
            print(v[i], end=space_char)
        print()

show_help = False
verbose_mode = False
silent_mode = False
space_char = '\t'
output_format = 'stdout'
argv = sys.argv

if (len(argv) < 2) or ('--help' in argv) or ('-h' in argv):
    show_help = True
else:
    for i in range(0, len(argv)):
        if argv[i] == '--char' and (i + 1) < len(argv):
            space_char = argv[i + 1][0:10]
        elif argv[i] == '--verbose' or argv[i] == '-v':
            verbose_mode = True
        elif argv[i] == '--silent':
            silent_mode = True
        elif argv[i] == '--excel' and (i + 2) < len(argv):
            output_format = 'excel'
            output_filename = argv[i + 1][0:100]
            output_page = argv[i + 2][0:50]

if show_help:
    print('''
FinViz scrabing...
scribing.py <TICKERS> <parameters>

Parameters:
    -h, --help      : show this page'
    -v, --verbose   : show more information about program works
    --excel         : export data in excel document.
       <filename>     If file or sheet name is not found, create new file and new sheet.
       <sheet name>   Example: --excel myexcel.xlsx "stock"
    --char <char>   : special separator char for standart output. Default = "\\t". Example: --char ";"
    --silent        : drop all message to stdout
''')
    exit(0)

keys = []
values = {}
tics = sys.argv[1].split()

if not silent_mode:
    for i in tics:
        print(i, end=' ')
    print()

for tic in tics:
    tic = tic[0:10]
    if not silent_mode:
        print('scrabing', tic, '...')
    value = []
    keys, value = finviz.scrab(tic, keys, verbose=verbose_mode)
    values[tic] = value

if verbose_mode:
    print('values = ', values)

if output_format == 'stdout':
    to_stdout(keys, values, space_char, verbose_mode)
elif output_format == 'excel':
    if not silent_mode:
        print('exporting to', output_filename)
    to_excel(output_filename, output_page, keys, values, verbose_mode)

if not silent_mode:
    print('scabbing completed')
