
def get_files_data():
    high_score_file = "Backend/High_score.txt"
    with open(high_score_file, 'r', encoding='UTF-8') as file:
        high_score = int(file.readline())

    player_name_file = "Backend/Name.txt"
    with open(player_name_file, 'r', encoding='UTF-8') as file:
        player_name = file.readline()

    return high_score_file, high_score, player_name_file, player_name