import os
from dotenv import load_dotenv 

load_dotenv()
environment = os.getenv("ENV")

def get_static_path(filename, folderName):
    static_path = 'static/' + filename
    link_url = '/' + static_path

    if (environment == 'dev'):
        static_path = folderName + '/' + static_path

    return (static_path, link_url)
