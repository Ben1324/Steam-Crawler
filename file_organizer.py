import json, os
from datetime import datetime

def date(organized_list):
    # rearanges the dates so it is readable by the system
    unix_date = organized_list["timestamp_created"]
    not_unix_date = datetime.utcfromtimestamp(unix_date).strftime("%Y-%m-%d - %H:%M")
    return not_unix_date

def count_file_directory(a_path):
    # reads the directory and counts number of files
    absolute_path = os.path.abspath(a_path)
    count = 0
    for path in os.listdir(absolute_path):
        # checks if the files starts with 'ben'
        if os.path.isfile(os.path.join(a_path, path)) and path.startswith('steam'):
            count += 1
    print(f"{count} files detected")
    return count

def get_json(file, path = "."):
    # reads the file and returns it as a list
    discord_file = open(file, "r", encoding = "utf-8-sig")
    json_file = discord_file.read()
    json_text = json.loads(json_file)
    discord_file.close()
    return json_text

def open_files(a_path):
    counter_a = 0
    mega_list = list()
    absolute_path = os.path.abspath(a_path)
    for filename in os.listdir(absolute_path):
        if os.path.isfile(os.path.join(absolute_path, filename)) and filename.endswith(".json") and filename.startswith('steam'):
            path_a_json = get_json(filename, path = absolute_path)
            counter_a += 1
            mega_list += path_a_json
    print("opened all files")

    # removes any duplicate from the lists
    final_list = {item["recommendationid"]: item for item in mega_list}
    final_list = final_list.values()
    print("deduplicated")

    # sorts the list again
    final_sorted = sorted(final_list, key = lambda d: date(d))
    print("sorted")

    #writes it all to a file
    write_to_file = open(os.path.join(absolute_path,"final_sorted_list.json"), "w", encoding = "utf-8-sig")
    json.dump(final_sorted, write_to_file)
    write_to_file.close()
    print("complete")

dirname = os.path.dirname(__file__)
filename = os.path.join(dirname, "Users\\ChristelFranklinson\\Documents\\Ben O'Riordan\\Python\\Sample project\\")

print("Starting consolidation process")

path_c = "."
open_files(path_c)