
# Write your code here


from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date
from datetime import datetime, timedelta
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///todo.db?check_same_thread=False')
Base = declarative_base()


class Table(Base):
    __tablename__ = 'task'
    id = Column(Integer, primary_key=True)
    task = Column(String)
    deadline = Column(Date, default=datetime.today())

    def __repr__(self):
        return self.task


Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()
exit_ = "off"


def wday(x):
    if x == 0:
        return "Monday"
    elif x == 1:
        return "Tuesday"
    elif x == 2:
        return "Wednesday"
    elif x == 3:
        return "Thursday"
    elif x == 4:
        return "Friday"
    elif x == 5:
        return "Saturday"
    elif x == 6:
        return "Sunday"


def todays_tasks():

    today = datetime.today()
    print("\nToday", str(today.day), today.strftime("%b"))
    rows = session.query(Table).filter(Table.deadline == today.date()).all()
    if not rows:
        print("Nothing to do!")
    else:
        count = 1
        for i in range(len(rows)):
            print(str(count), ".", rows[i])
            count += 1


def weeks_tasks():


    day_check = datetime.today()
    day_count = 1
    for i in range(7):

        print("\n", wday(day_check.weekday()), str(day_check.day), str(day_check.strftime("%b")) + ":")
        rows = session.query(Table).filter(Table.deadline == day_check.date()).all()

        count = 1

        for j in range(len(rows)):

            print(str(count) + ".", rows[j])
            count += 1

        day_check = datetime.today() + timedelta(days=day_count)
        day_count += 1


def all_tasks():

    print("\nAll tasks:")
    rows = session.query(Table).order_by(Table.deadline).all()
    count = 1
    for i in range(len(rows)):
        print(str(count) + ".", str(rows[i]) + ".", rows[i].deadline.day, rows[i].deadline.strftime("%b"))
        count += 1


def add_task():
    new_task = input("\nEnter task\n")
    new_deadline = input("\nEnter deadline\n")
    new_row = Table(task=new_task, deadline=datetime.strptime(new_deadline, "%Y-%m-%d").date())
    session.add(new_row)
    session.commit()
    print("The task has been added!")


def main():

    global exit_

    while exit_ == "off":

        option = int(input("\n1) Today's tasks\n2) Week's tasks\n3) All tasks\n4) Add task\n0) Exit\n"))

        if option == 1:
            todays_tasks()

        elif option == 2:
            weeks_tasks()

        elif option == 3:
            all_tasks()

        elif option == 4:
            add_task()

        else:
            exit_ = "on"

    else:
        print("\n\nBye!")


main()

