USER_AUTH = 0
USERNAME = ''

def account_check():
    global USER_AUTH
    if USER_AUTH == -1:
        print("Not a valid response. Please answer 'yes' or 'no'.")
    USER_AUTH = -1
    existing = input("Do you have an account? Y/N ").upper()
    make_account() if existing in 'NO' else login() if existing in 'YES' else account_check()
    return USERNAME
    

def login():
    global USER_AUTH
    global USERNAME
    auth = 0
    while auth == 0:
        username = input("Enter your username: ")
        password = input("Password: ")
        key = username + "%" + password
        with open('accounts.txt', 'r') as f:
            for line in f.readlines():
                if line.strip() == key:
                    print("Successfully logged in.")
                    USER_AUTH = 1
                    USERNAME = username
                    return 
        print("Could not find your account. Please try again.")


def make_user():
    existing = -1
    username = input("Enter a username (Not containing the % symbol): ")
    while '%' in username:
        username = input("Not a valid username. Please try again: ")
    with open("accounts.txt", "r") as f:
        while existing != 0:
            for line in f:
                if line.strip().split('%')[0] == username:
                    existing = 1
            if existing == 1:
                username = input("That username already exists. Please enter a new username: ")
                while '%' in username:
                    username = input("Not a valid username. Please try again: ")
                existing = -1
            else:
                existing = 0
    return username


def make_password():
    while True:
        password = input("Enter a password (Not containing the % symbol): ")
        while '%' in password:
            password = input("Not a valid password. Please enter a new password: ")
        if input("Re-enter the password: ") != password:
            print("Those passwords don't match. Please try again")
        else:
            return password


def make_account():
    username = make_user()
    password = make_password()
    with open('accounts.txt', 'a') as f:
        f.write(username + '%' + password + '\n')
    print("You've successfully created an account! Please log in now.")
    auth = 0
    while auth == 0:
        auth = login()
