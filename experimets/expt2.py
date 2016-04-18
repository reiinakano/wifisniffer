def test(a):
    sub = a
    sub[0] +=1

if __name__ == '__main__':
    list = [0]
    test(list)
    print list
    test(list)
    print list