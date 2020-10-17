from .db_connect import conn, c
from .guardian_stars import GuardianStarsContainer

c.execute("SELECT * FROM Player")

data = c.fetchall()


for row in data:
    print(row)

print()

Guardian_Stars_Container = GuardianStarsContainer()

while True:
    try:
        choice = int(input("Enter the ID of the player whose data you want to load: "))
        correct_id = False

        for row in data:
            if choice == row[0]:
                ACTIVE_PLAYER = {"ID": choice, "Name": row[1], "Deck_ID": row[2]}
                correct_id = True

        if correct_id:
            break
        print("Please enter an active ID.\n")
    except ValueError:
        print("Please enter a valid ID.\n")

#c.close()
#conn.close()
