'''
Date: 2021.04.29 22:31
Description: Omit
LastEditors: Rustle Karl
LastEditTime: 2021.04.29 22:31
'''

# column x row
GIRD_1x4 = '0_0|0_h0|0_h0+h1|0_h0+h1+h2'
GIRD_2x2 = '0_0|0_h0|w0_0|w0_h0'
GIRD_3x3 = '0_0|0_h0|0_h0+h1|w0_0|w0_h0|w0_h0+h1|w0+w3_0|w0+w3_h0|w0+w3_h0+h1'
GIRD_4x4 = '0_0|0_h0|0_h0+h1|0_h0+h1+h2|w0_0|w0_h0|w0_h0+h1|w0_h0+h1+h2|' \
           'w0+w4_0|w0+w4_h0|w0+w4_h0+h1|w0+w4_h0+h1+h2|w0+w4+w8_0|' \
           'w0+w4+w8_h0|w0+w4+w8_h0+h1|w0+w4+w8_h0+h1+h2'


def generate_gird_layout(column: int, row: int) -> str:
    layout = []

    for position in range(column * row):
        _column, _row = divmod(position, row)
        co = ['w%d' % (i * column) for i in range(_column)] or ['0']
        ro = ['h%d' % i for i in range(_row)] or ['0']
        layout.append(f"{'+'.join(co)}_{'+'.join(ro)}")

    return '|'.join(layout)


if __name__ == '__main__':
    print(generate_gird_layout(1, 4))
    print(generate_gird_layout(4, 40))
