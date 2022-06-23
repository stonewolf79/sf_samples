USERS = ['admin', 'guest', 'director', 'root', 'superstar']

#yesno = input("""Введите Y, если хотите авторизоваться, или N, 
#             если хотите продолжить работу как анонимный пользователь: """)

auth = True#yesno == "Y"
username = ''

if auth:
    #username = input("Введите ваш username:")
    pass

def is_auth(f):
    def w(*a,**k):
        if not auth:
            print('доступ запрещён')
        else:
            return f(*a,**k)
    return w

def has_access(f):
    def w(*a,**k):
        if not username in USERS:
            print(f'нет пользрователя {username}')
        else:
            return f(*a,**k)
    return w

@is_auth
@has_access
def from_db():
    print("some data from database")

def test(user):
    global username
    username = user
    print(f'user = {user}')
    from_db()

test('admin')
test('qwe')