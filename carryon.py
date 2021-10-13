import collections
import functools
import re

luggage_requirements = []
frequency = collections.defaultdict(list)
with open('carryon.csv', 'r') as datafile:
    for line in datafile:
        parts = line.strip().split(';')
        airline_name = parts[0]
        luggage_size = parts[1]

        obj = {
            'airline_name': airline_name
        }
        if 'linear' in luggage_size:
            obj['linear'] = float(re.search(r'^([\d.]+)', luggage_size, flags=0).group(1))
            obj['d1'] = 0
            obj['d2'] = 0
            obj['d3'] = 0
            obj['volume'] = 0
        else:
            d1, d2, d3 = [float(token.strip()) for token in luggage_size.strip().split('x')]
            obj['d1'] = d1
            obj['d2'] = d2
            obj['d3'] = d3

            frequency['{}:{}:{}'.format(d1, d2, d3)].append(airline_name)

            obj['linear'] = d1 + d2 + d3
            obj['volume'] = d1 * d2 * d3

        luggage_requirements.append(obj)

for i in range(len(luggage_requirements)):
    will_fit = 0

    for requirement in luggage_requirements:
        if luggage_requirements[i]['d1'] == 0 or requirement['d1'] == 0:
            if luggage_requirements[i]['linear'] <= requirement['linear']:
                will_fit += 1
        else:
            if luggage_requirements[i]['d1'] <= requirement['d1'] and luggage_requirements[i]['d2'] <= requirement[
                'd2'] and luggage_requirements[i]['d3'] <= requirement['d3']:
                will_fit += 1

    luggage_requirements[i]['will_fit'] = will_fit
    if luggage_requirements[i]['d1'] != 0:
        luggage_requirements[i]['frequency'] = len(frequency['{}:{}:{}'.format(luggage_requirements[i]['d1'],
                                                                               luggage_requirements[i]['d2'],
                                                                               luggage_requirements[i]['d3'])])
    else:
        luggage_requirements[i]['frequency'] = 0


def order_func_linear(item):
    return item['linear']


def order_func_volume(item):
    return item['volume']


def order_func_dimensions(item):
    return item['d1'], item['d2'], item['d3']


def order_func_frequency(item):
    return item['frequency']


def order_func_will_fit(item):
    return item['will_fit']


def compare_by_dimensions_or_linear(x, y):
    if x['d1'] == 0 or y['d1'] == 0:
        return x['linear'] - y['linear']

    if x['d1'] != y['d1']:
        return x['d1'] - y['d1']

    if x['d2'] != y['d2']:
        return x['d2'] - y['d2']

    return x['d3'] - y['d3']


def output(title, requirements):
    print()
    print('{:-^100}'.format(' {} '.format(title)))
    print()
    print('    Dimensions     | Lin. |  Vol.  | Frq. | Tot. | Airline ')
    print('-------------------|------|--------|------|------|------------------------------------')
    for requirement in requirements:
        if requirement['d1'] != 0:
            print('{:4} x {:4} x {:4} | {:4.1f} | {:6.1f} | {:4} | {:4} | {}'.format(
                requirement['d1'],
                requirement['d2'],
                requirement['d3'],
                requirement['linear'],
                requirement['volume'],
                len(frequency['{}:{}:{}'.format(requirement['d1'], requirement['d2'], requirement['d3'])]),
                requirement['will_fit'],
                requirement['airline_name']))
        else:
            print('                   | {:4.1f} |        |      | {:4} | {}'.format(
                requirement['linear'],
                requirement['will_fit'],
                requirement['airline_name']))
    # print('-------------------|------|------|------|------|------------------------------------')
    # print('    Dimensions     | Lnr. | Vol. | Frq. | Tot. | Airline ')
    # print('------------------------------------------------------------------------------------')
    print()


output('By dimensions and linear size',
       sorted(luggage_requirements, key=functools.cmp_to_key(compare_by_dimensions_or_linear), reverse=True))

output('By linear size',
       sorted(luggage_requirements, key=order_func_linear, reverse=True))

output('By volume',
       sorted(luggage_requirements, key=order_func_volume, reverse=True))

output('By frequency of use',
       sorted(luggage_requirements, key=order_func_frequency, reverse=True))

output('By number of airlines that fit',
       sorted(luggage_requirements, key=order_func_will_fit, reverse=True))

# 22 x 17.7 x 9.8 easyJet
# 22 x 14 x 9 - 31
# 21.6 x 15.7 x 9 - 10 Turkish
# 21.5 x 15.5 x 9 - 7
# 21.5 x 13.5 x 10 KLM
# 21.6 x 15.7 x 7.8 - 15
# 22 x 18 x 10 - British
# 22 x 15 x 8 - Emirates
# 21.5 x 15.9 x 9        1: ['Norwegian']

# 21.5 x 13.5 x 7.8


# 15.7 x 13.7 x 7        1: ['Loganair']
# 15.7 x 9.8 x 7.8       1: ['Ryanair']
# 15.7 x 11.8 x 7.8 - wizzair
