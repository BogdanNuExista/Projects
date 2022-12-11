import random
import string
import sqlite3

d={}
ok=True

def Lobby():
    print("1. Create an account")
    print("2. Long into account")
    print("0. Exit")

def Lobby2():
    print("1. Balance")
    print("2. Add income")
    print("3. Do transfer")
    print("4. Close account")
    print("5. Log out")
    print("0. Exit")

def Close_account():
    global ok
    c.execute("delete from card where number=?",(d[1][0],))
    conn.commit()
    ok=True
    print()
    print("The account has been closed!")
    print()

def Add_income():
    print()
    print("Enter income:")
    n=int(input())
    c.execute("update card set balance=balance+? where pin=? and number=?",(n,d[1][1],d[1][0]))
    conn.commit()
    print("Income was added!")
    print()

def Balance():
    print()
    c.execute("select balance from card where pin=? and number=?",(d[1][1],d[1][0]))
    res=c.fetchone()
    print("Balance: "+str(res[0]))
    print()

def Transfer():
    print()
    print("Enter card number:")
    n=str(input())
    if n==d[1][0]:
        print("You can't transfer money to the same account!")
    else:
        if Card_is_valid(n)==False:
            print("Probably you made a mistake in the card number. Please try again!")
            print()
        else:
            vf1 = 0
            for row in c.execute("select number from card"):
                if str(row[0])==n:
                    vf1=1
            if vf1==0:
                print("Such a card does not exist.")
                print()
            else:
                print("Enter how much money you want to transfer:")
                money=int(input())
                c.execute("select balance from card where pin=? and number=?", (d[1][1], d[1][0]))
                res = c.fetchone()
                if money>int(res[0]):
                    print("Not enough money!")
                    print()
                else:
                    c.execute("update card set balance=balance-? where pin=? and number=?", (money, d[1][1], d[1][0]))
                    conn.commit()
                    c.execute("update card set balance=balance+? where number=?", (money,n))
                    conn.commit()
                    print("Success!")
                    print()

def User_Input():
    n=int(input())
    return n

def Card_is_valid(n):
    l=list(n)
    s=0
    for i in range(0, len(l)-1):
        if (i + 1) % 2 == 1:
            l[i] = int(l[i]) * 2
        if int(l[i]) > 9:
            l[i] = int(l[i]) - 9
        s += int(l[i])
    s+=int(l[len(l)-1])
    if s%10==0:
        return True
    return False

def create_valid_card():
    while(True):
        s=0
        n = ''.join(random.choices(string.digits, k=16))
        l=list(n)
        ultim=l[len(l)-1]
        l.pop(len(l)-1)
        l[0]=4
        for i in range(1,6):
            l[i]=0

        for i in range(0,len(l)):
            if (i+1)%2==1:
                l[i]=int(l[i])*2
            if int(l[i])>9:
                l[i]=int(l[i])-9
            s+=int(l[i])

        s+=int(ultim)

        if s%10==0:
            card=""
            final=list(n)
            final[0]=4
            for i in range(1,6):
                final[i]=0
            for i in range(0,len(final)):
                card+=str(final[i])
            break
    return card


def Create_Account():
    n = create_valid_card()
    pin = ''.join(random.choices(string.digits, k=4))

    return n, pin

def Create_an_accout():

    number,pin=Create_Account()
    d.update({1:[number,pin]})
    print()
    print("Your card has been created")
    print("Your card number:")
    print(d[1][0])
    print("Your card PIN:")
    print(d[1][1])
    print()
    l=list()
    l.append(d[1][0])
    l.append(d[1][1])
    c.execute("insert into card (number,pin) values (?,?);",l)
    conn.commit()

def Log_into_acccount():

    verific=0
    print()
    global ok
    print("Enter your card number:")
    n=str(input())
    print("Enter your pin")
    pin=str(input())

    for row in c.execute("select pin,number from card"):
        if pin==str(row[0]) and n==str(row[1]):
            ok=False
            print("You have successfully logged in!")
            verific=1
            d.update({1: [n, pin]})

    if verific==0:
        print()
        print("Wrong card number or PIN!")

    print()

def LogOut():
    global ok
    ok=True
    print()
    print("You have successfully logged out!")
    print()

def Exit():
    print()
    print("Bye!")
    #for row in c.execute("select * from card"):       # afisare baza de date
    #    print(row)
    quit()


if __name__ == '__main__':

    conn = sqlite3.connect('card.s3db')
    c=conn.cursor()
    conn.commit()
    c.execute("create table if not exists card(id INTEGER,number TEXT,pin TEXT,balance INTEGER DEFAULT 0);")
    conn.commit()

    print()
    for row in c.execute("select * from card"):
        print(row)
    print()

    while(True):

        if ok==True:
            Lobby()
            inp=User_Input()
            if inp==0:
                Exit()
            elif inp==1:
                Create_an_accout()
            elif inp==2:
                Log_into_acccount()
        else:
            Lobby2()
            inp=User_Input()
            if inp==0:
                Exit()
            if inp==1:
                Balance()
            if inp==2:
                Add_income()
            if inp==3:
                Transfer()
            if inp==4:
                Close_account()

            if inp==5:
                LogOut()

