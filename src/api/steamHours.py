from steam import Steam
from decouple import config
import math
import json



#digit is # after .
def truncate(number, digits) -> float:
    nbDecimals = len(str(number).split('.')[1]) 
    if nbDecimals <= digits:
        return number
    stepper = 10.0 ** digits
    return math.trunc(stepper * number) / stepper

def getHeaderImage(appid) -> str:
    appDataJson = json.loads(steam.apps.get_app_details(appid))
    return appDataJson[str(appid)]["data"]["header_image"]

def steamHours(steamid) -> str:
    KEY = config("STEAM_API_KEY")
    steam = Steam(KEY)
    # arguments: steamid
    # my steam id: 76561198431671719
    user = steam.users.get_owned_games(steamid)
    games = user["games"]

    result = ""

    for attribute in games:
         result += (getHeaderImage(attribute["appid"]) + "  "  + attribute["name"] 
            + "  " + str(truncate(attribute["playtime_forever"]/60.0, 1)) + " hours\n")
         
    return result






    

