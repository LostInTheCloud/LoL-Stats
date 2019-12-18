import main

f = open("log.txt", "w")
numberofgames = main.get_number_of_games(main.NAME)
print('Games played: ' + str(numberofgames))
for index in range(int(numberofgames)):
    print('\nChecking Game ' + str(index + 1) + '/' + str(numberofgames))
    match_id = main.get_match_id(index)
    players = main.get_players(match_id)
    print(players)
    f.write(str(index + 1) + '/' + str(numberofgames) + ' ' + str(str(players).encode("utf-8")) + '\n')
f.close()

input("Press enter to exit...")
