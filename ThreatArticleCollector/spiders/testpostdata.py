#_*_coding:utf-8_*_
def test(name,*args,**kwargs):
    print(name)
    print(args)
    print(type(kwargs))


if __name__ == '__main__':
    test('Tom',1,2,3,4,5,6,key1=1,value1=1,key2=2,value2=2,key3=3,value3=3)

# def findad(username,**args):
#     '''''find address by dictionary'''
#     print 'Hello: ', username
#     for name,address in args.items():
#         print 'Contact %s at %s'%(name,address)
# findad('wcdj',gerry='gerry@byteofpython.info',wcdj='wcdj@126.com',yj='yj@gmail.com')