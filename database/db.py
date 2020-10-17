import time, datetime, random, sqlite3
import  matplotlib.pyplot as plt
import  matplotlib.pyplot as mdates
from matplotlib import style

style.use("fivethirtyeight")

conn = sqlite3.connect("tutorial.db")
c = conn.cursor()

def create_table():
    c.execute("CREATE TABLE IF NOT EXISTS stuffToPlot(unix REAL, datestamp TEXT, keyword TEXT, value REAL)")

def data_entry():
    c.execute("INSERT INTO stuffToPlot VALUES(1242421, '2019-06-17', 'Python', 5)")
    conn.commit()
    c.close()
    conn.close()

def dynamic_data_entry():
    unix = time.time()
    date =str(datetime.datetime.fromtimestamp(unix).strftime("%Y-%m-%d %H:%M:%S"))
    keyword = "Python"
    value = random.randrange(0, 10)
    c.execute("INSERT INTO stuffToPlot (unix, datestamp, keyword, value) VALUES (?, ?, ?, ?)",
               (unix, date, keyword, value))
    conn.commit()

def read_from_db():
    c.execute("SELECT * FROM stuffToPlot WHERE value=3 AND keyword='Python'")
    data = c.fetchall()
    for row in data:
        print(row)

def graph_data():
    c.execute("SELECT unix, value FROM stuffToPlot")
    values = []
    dates = []
    for row in c.fetchall():
        dates.append(datetime.datetime.fromtimestamp(row[0]))
        values.append(row[1])
    plt.plot_date(dates, values, '-')
    plt.show()

def del_and_update():
    c.execute("SELECT * FROM stuffToPlot")
    [print(row) for row in c.fetchall()]
##    dog = 4
##    c.execute("UPDATE stuffToPlot SET value=99 WHERE value=(?)", (dog,))
##    conn.commit()
##
##    print()
##
##    c.execute("SELECT * FROM stuffToPlot")
##    [print(row) for row in c.fetchall()]
    print()
    c.execute("DELETE FROM stuffToPlot WHERE value = 99")
    conn.commit()

    c.execute("SELECT * FROM stuffToPlot")
    [print(row) for row in c.fetchall()]

#create_table()
#data_entry()
#for x in range(10):
#    dynamic_data_entry()
#    time.sleep(1)
#graph_data()
del_and_update()
c.close()
conn.close()
