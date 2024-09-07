import os, sys, time
import gridfs
import base64
from pymongo import MongoClient
from dotenv import load_dotenv
from datetime import datetime

from bson import json_util
from bson.objectid import ObjectId
from bson.errors import InvalidId

import termtables as tt
from colorama import init, Fore

init() 
load_dotenv() 

# Database variables
MONGO_URI = os.getenv("MONGO_URI")
MONGO_DB = os.getenv("MONGO_DB")

client = MongoClient(MONGO_URI)
db = client[MONGO_DB]
collection = db["$COLLECTION_NAME"]

fs = gridfs.GridFS(db)

def connect_to_db():
    if not MONGO_URI or not MONGO_DB:
        raise Exception(f"{Fore.RED}[!]{Fore.RESET} Invalid MONGO URI or MONGO_DB")

    try:
        client.admin.command('ping')
        return True
    except Exception as e:
        print(e)


def get_all_files():
    headers = [f"{Fore.GREEN}File_Id{Fore.RESET}",
               f"{Fore.GREEN}Filename{Fore.RESET}",
               f"{Fore.GREEN}Upload_Date{Fore.RESET}", 
               f"{Fore.GREEN}Description{Fore.RESET}"
               ]

    db_files = list(collection.find())
    formatted_data = json_util.dumps(db_files, indent=4) # json pretty data

    table_info = []

    for file in db_files:
        fileId = file.get('fileId')
        filename = file.get('filename')
        uploadDate = file.get('uploadDate')
        description = file.get('description')

        table_info.append([fileId, filename, uploadDate, description])

    alignment = "llll"
    try:
        table_string = tt.to_string(
            table_info,
            header=headers, 
            style=tt.styles.ascii_thin_double,
            alignment=alignment, 
        )

        print(table_string)
    except:
        print(f"{Fore.RED}[!]{Fore.RESET} The database is currently empty!")
        sys.exit(1)


def get_file_from_db():
    get_all_files()
    print("\n")

    file_id = input(f"{Fore.GREEN}[?]{Fore.RESET} Enter the id of the file to decrypt: ")

    try: 
        file = collection.find_one({ "fileId" : ObjectId(file_id) })

        if file:
            file_content = fs.get(file['fileId'])
            encrypted_data = file_content.read()
            binary_data = base64.b64decode(encrypted_data)

            return binary_data, file['filename']
        else:
            print(f"{Fore.RED}[!]{Fore.RESET} Invalid fileId, make sure to enter an existent one!")
    
    except InvalidId:
        print(f"{Fore.RED}[!]{Fore.RESET} Invalid fileId format!")
    except Exception as e:
        print(f"{Fore.RED}[!]{Fore.RESET} Unexpected error ", e)
        

def upload_file_to_db(outputFile, description):
    connect_to_db() 

    currentTime = datetime.now()

    with open(outputFile, "rb") as in_file:
        binary_data = base64.b64encode(in_file.read())


    fileId = fs.put(binary_data, filename=outputFile)

    data = {
        "filename": outputFile,
        "fileId": fileId,
        "uploadDate": currentTime,
        "description": description
    }
    
    collection.insert_one(data)

    formatted_data = json_util.dumps(data, indent=4)
    print(f"\n{Fore.GREEN}Exporting register..{Fore.RESET}")

    for char in formatted_data:
        sys.stdout.write(char)   
        sys.stdout.flush()        
        time.sleep(0.015)  
    print("\n")


def delete_file_from_db():
    get_all_files()
    file_id = input(f"\n{Fore.GREEN}[?]{Fore.RESET} Enter the file_id of the file to delete: ")
    try: 
        while True:
            file = collection.find_one({ "fileId" : ObjectId(file_id) })

            if file:
                confirm = input(f"{Fore.RED}[!]{Fore.RESET} Are you sure to delete the encrypted file identified by {file_id} file_id? (y/n): ")
                match confirm:
                    case "y":
                        collection.delete_one(file)
                        print(f"\n{Fore.GREEN}[+]{Fore.RESET} File with file_id {Fore.GREEN}{file_id}{Fore.RESET} has been successfully deleted!")
                        break
                    case "n":
                        print(f"{Fore.RED}[!]{Fore.RESET} File deletion process interrupted!")
                        sys.exit(0)
                    case _:
                        print(f"\n{Fore.RED}[!]{Fore.RESET} Invalid option!\n")
            else:
                print(f"{Fore.RED}[!]{Fore.RESET} Invalid fileId, make sure to enter an existent one!")
    except InvalidId:
        print(f"{Fore.RED}[!]{Fore.RESET} Invalid fileId format!")
    except Exception as e:
        print(f"{Fore.RED}[!]{Fore.RESET} Unexpected error ", e)
