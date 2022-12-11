from datetime import date,datetime,timedelta
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.orm import sessionmaker

def menu():
    print("1) Today's tasks")
    print("2) Week's tasks")
    print("3) All tasks")
    print("4) Missed tasks")
    print("5) Add a task")
    print("6) Delete a task")
    print("0) Exit")
    return int(input())

engine = create_engine('sqlite:///todo.db?check_same_thread=False')

Base = declarative_base()

class Table(Base):
    __tablename__="task"

    id = Column(Integer, primary_key=True, autoincrement=True)
    task = Column(String)
    deadline = Column(Date, default=date.today())

    def __repr__(self):
        return self.task,self.deadline

Session = sessionmaker(bind=engine)
session = Session()

def add_a_task():
    print("Enter a task")
    t=str(input())
    print("Enter a deadline")
    d=str(input())
    l=list(d.split('-'))
    d=date(int(l[0]),int(l[1]),int(l[2]))
    n_task = Table(task=t,deadline=d)
    session.add(n_task)
    session.commit()

    print("The task has been added!")
    print()

def today_tasks():
    td=date.today()
    print("Today "+td.strftime('%d %b')+":")
    c=1
    for i in session.query(Table).order_by(Table.deadline).all():
        if i.deadline==date.today():
            print(str(c) + ") " + i.task)
            c += 1
    if c==1:
        print("Nothing to do!")
    print()

def same_week(dateString): # dont need
    '''returns true if a dateString in %Y%m%d format is part of the current week'''
    d1 = datetime.strptime(dateString,'%Y-%m-%d')
    d2 = datetime.today()
    return d1.isocalendar()[1] == d2.isocalendar()[1] \
              and d1.year == d2.year

def week_tasks():
    td = datetime.today()
    contor=0
    while contor<7:
        zi=td + timedelta(days=contor)
        contor += 1
        ok=1
        print(zi.strftime('%A %d %b')+":")
        for i in session.query(Table).order_by(Table.deadline).all():
            if i.deadline.year==zi.year and i.deadline.month==zi.month and i.deadline.day==zi.day:
                print(str(ok)+". "+i.task)
                ok+=1
        if ok==1:
            print("Nothing to do!")
        print()
    print()

def missed_tasks():
    td=date.today()
    print("Missed tasks:")
    c=1
    for i in session.query(Table).order_by(Table.deadline).all():
        if td>i.deadline:
            print(str(c)+". "+i.task+". "+i.deadline.strftime('%d %b'))
            c+=1
    if c==1:
        print("All tasks have been completed!")

    print()

def delete_task():
    print()
    c=1
    print("Choose the number of the task you want to delete:")
    for i in session.query(Table).order_by(Table.deadline).all():
        print(str(c) + ") " + i.task + ". " + str(i.deadline.strftime('%d %b')))
        c+=1
    n=int(input())
    c=1
    for i in session.query(Table).order_by(Table.deadline).all():
        if c==n:
            session.delete(i)
            session.commit()
            print("The task has been deleted!")
        c+=1

    print()

def all_tasks():
    c=1
    for i in session.query(Table).order_by(Table.deadline).all():
        print(str(c)+") "+i.task+". "+str(i.deadline.strftime('%d %b')))
        c+=1
    if c==1:
        print("Nothing to do!")
    print()

def Exit():
    print("Bye!")
    exit()

if __name__=="__main__":

    #Base.metadata.drop_all(engine)       # for new database at every start
    Base.metadata.create_all(engine)

    while(True):
        n=menu()
        print()
        if(n == 0):
            Exit()
        if(n == 1):
            today_tasks()
        if (n == 2):
            week_tasks()
        if (n == 3):
            all_tasks()
        if (n == 4):
            missed_tasks()
        if (n == 5):
            add_a_task()
        if (n == 6):
            delete_task()
