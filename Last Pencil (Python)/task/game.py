import random


def player_johns_turn():

    global pencil_number

    print("John's turn:")

    while True:

        while True:

            try:
                pencils_taken = int(input())

                if pencils_taken < 0:
                    print("Possible values: '1', '2', or '3'")
                else:
                    if pencils_taken not in {1, 2, 3}:
                        print("Possible values: '1', '2', or '3'")
                    else:
                        break

            except ValueError:

                print("Possible values: '1', '2', or '3'")

        if pencils_taken > pencil_number:
            print("Too many pencils were taken")
        else:
            break

    pencil_number -= pencils_taken

    if pencil_number < 0:
        pencil_number = 0

    if pencil_number == 0:
        return "Jack"

    print("".join("|" for i in range(pencil_number)))

    return ""


def bot_jacks_turn():

    global pencil_number

    is_loser = False

    print("Jack's turn:")

    if pencil_number == 1:
        print("1")
        return "John"
    elif pencil_number % 4 == 0:
        bots_take = 3
    elif (pencil_number + 1) % 4 == 0:
        bots_take = 2
    elif (pencil_number + 2) % 4 == 0:
        bots_take = 1
    else:
        bots_take = random.randint(1, 3)

    print(bots_take)

    pencil_number -= bots_take

    print("".join("|" for i in range(pencil_number)))

    return ""


# Main Program Starts Here

print("How many pencils would you like to use:")

while True:

    while True:

        try:
            pencil_number = int(input())
            break
        except ValueError:
            print("The number of pencils should be numeric")

    if pencil_number < 1:
        print("The number of pencils should be positive")
    else:
        break

print("Who will be the first (John, Jack):")

while True:

    players_turn = str(input())

    if players_turn not in {"John", "Jack"}:
        print("Choose between 'John' and 'Jack'")
    else:
        break

pencils = "".join("|" for i in range(pencil_number))

print(pencils)

total_pencils_taken = 0

while True:

    if players_turn == "John":

        winners_name = player_johns_turn()
        players_turn = "Jack"

    else:

        winners_name = bot_jacks_turn()
        players_turn = "John"

    if winners_name != "": break

print(winners_name,"won!")