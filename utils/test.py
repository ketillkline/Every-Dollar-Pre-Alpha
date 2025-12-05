value = 'I am him. And he is me'

if '.' in value:  # check for bug
    try:
        value = float(value)
    except ValueError:
        print('nope')
else:
    try:
        value = int(value)
    except ValueError:
        print('nope')

print(type(value))