import main

f = open("previous players.txt", "w", encoding='utf-8')
numberofgames = main.get_number_of_games(main.NAME)
print('Games played: ' + str(numberofgames))
for index in range(int(numberofgames)):
    print('\nChecking Game ' + str(index + 1) + '/' + str(numberofgames))
    match_id = main.get_match_id(index)
    players = main.get_players(match_id)
    print(str(index + 1) + '/' + str(numberofgames) + ' ')
    f.write(str(index + 1) + '/' + str(numberofgames) + ' ')
    for player in players:
        print(player)
        f.write(player + ', ')
    f.write('\n')
f.close()
