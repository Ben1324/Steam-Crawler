import requests, json, urllib, datetime, time, os

def get_steam_reviews(game_ID, cursor = ""):
    url = f"https://store.steampowered.com/appreviews/{game_ID}?json=1&filter=recent&purchase_type=all"
    if cursor == "":
        steam_review_api = requests.get(url)
    else:
        steam_review_api = requests.get(url+"&cursor="+cursor)
    return steam_review_api.json()

def find_replace(game_ID, find, replace, number = "0"):
    text = open(f"steam_review_page_{game_ID}_{number}.json", "r")
    for line in text:
        if find in line:
            replace_text = (line.replace(find, replace))
            write_on_file(game_ID, "w", replace_text, number = number)
    text.close()


def write_on_file(game_ID, type, write = "", number = "0", encoding = "utf-8-sig"):
    steam_reviews = open(f"steam_review_page_{game_ID}_{number}.json", mode= type)
    steam_reviews.write(write)
    steam_reviews.close()

def get_review_stats(API_json_text):
    query = API_json_text["query_summary"]
    return query

def check_file(game_ID, number):
    write_on_file(game_ID, "a", "]", number)
    find_replace(game_ID, "][", ", ", number)
    find_replace(game_ID, "],[", ", ", number)
    find_replace(game_ID, ",]", "]", number)
    find_replace(game_ID, ", ]", "]", number)
    find_replace(game_ID, "],", "]", number)
    

def normal_sort(game_ID):
    API_json_text = get_steam_reviews(game_ID)
    total = get_review_stats(API_json_text)["total_reviews"]
    current = get_review_stats(API_json_text)["num_reviews"]
    pages = int(total)//int(current) + 1
    counter = 0
    length = 0
    new_counter = 0
    file_number = 0
    write_on_file(game_ID, "w", "[", file_number)
    while counter <= pages and length < total:
        num_of_reviews = len(API_json_text["reviews"])
        if counter == 0:
            API_json_text = get_steam_reviews(game_ID)
        else:
            cursor = API_json_text["cursor"]
            API_json_text = get_steam_reviews(game_ID, urllib.parse.quote(cursor))
        length += num_of_reviews
        json_file = (json.dumps(API_json_text["reviews"])[1:-1] )
        if new_counter >= 50:
            write_on_file(game_ID, "a", json_file, file_number)
            check_file(game_ID, file_number)
            new_counter = 0
            file_number = file_number + 1
            print(f"file {file_number}: completed")
            write_on_file(game_ID, "w", "[", file_number)
        else:
            write_on_file(game_ID, "a", json_file + ",", file_number)
        print(f"{counter + 1} reviews printed")
        counter = counter + 1
        new_counter = new_counter + 1
    check_file(game_ID, file_number)


def sort_by_date(recent_unix, distant_unix, game_ID):
    API_json_text = get_steam_reviews(game_ID)
    counter = 0
    num_of_reviews = 0
    write_on_file(game_ID, "w", "[")
    while True:
        if counter != 0:
            cursor = API_json_text["cursor"]
            API_json_text = get_steam_reviews(game_ID, urllib.parse.quote(cursor))
        for individual_review in API_json_text["reviews"]:
            time = individual_review["timestamp_created"]
            if time >= distant_unix and time <= recent_unix:
                print("Printing Steam reviews")
                json_file = (json.dumps(individual_review) + ",")
                write_on_file(game_ID, "a", json_file)
                num_of_reviews = num_of_reviews + 1
        if time <= distant_unix:
            print(num_of_reviews)
            write_on_file(game_ID, "a", "]")
            find_replace(game_ID, "][", ", ")
            find_replace(game_ID, ",]", "]")
            print("File sorted!")
            return
        counter = counter + 1

def start_code(game_ID, recent_date, distant_date, user_input):
    if int(user_input) == 1:
        print("Commence gathering Steam reviews")
        normal_sort(game_ID)
    elif int(user_input) == 2:
        recent_unix = time.mktime(recent_date.timetuple())
        distant_unix = time.mktime(distant_date.timetuple())
        print("Commence gathering Steam reviews")
        sort_by_date(recent_unix, distant_unix, game_ID)
    else:
        print("Only valid options accepted")
        return


game_ID = os.getenv("STEAM_ID")
if game_ID == None:
    game_ID = 1044720

# year, month, day, hour, minute
recent_date = datetime.datetime(2022, 8, 15, 0, 0)
distant_date = datetime.datetime(2022, 7, 29, 0, 0)

# input = 1 is sorting reviews normoly orderd by date
# input = 2 is getting reviews within a specific time frame
user_input = 1

start_code(game_ID, recent_date, distant_date, user_input)
print("Steam reviews gathered")
