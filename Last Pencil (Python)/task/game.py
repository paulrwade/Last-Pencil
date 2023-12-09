print("How many pencils would you like to use:")

pencil_number = int(input())

print("Who will be the first (John, Jack):")

player_1 = str(input())

pencils = "".join("|" for i in range(pencil_number))

print(pencils)

print(player_1, "is going first!")

