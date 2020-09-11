from fake_useragent import UserAgent
ua = UserAgent()
a = ua.random
print(1, a)
a = a.split('(')[1]
print(2, a)
a = a.split(')')[0].split(';')
a = [x.strip() for x in a]
print(3, a)
