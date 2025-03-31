def gen_reverse(value):
    print(1, value)
    if value[0] == '0':
        return value
    else:
        print(2, value)
        for i in range(len(value)-1, 0, -1):
            value = value[:i]+str(int(value[i]) ^ 1)+value[i+1:]
        return value


def gen_add(value):
    if value[0] == '0':
        return value
    else:
        add = 1
        for i in range(len(value)-1, 0, -1):
            tmp = int(value[i])+add
            add = tmp//2
            value = value[:i]+str(tmp % 2)+value[i+1:]
        return value
