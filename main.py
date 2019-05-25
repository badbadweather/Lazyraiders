import urllib.parse
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
from datetime import datetime, date

# Realm names
realmA = "realmA"
realmB = "realmB"
realmC = "realmC"

# Raiders
raiders = [
    { "name": "raiderD", "realm": realmA },
    { "name": "raiderE", "realm": realmB },
    { "name": "raiderF", "realm": realmC },
]

print("\n" + "Checking raider.io data..." + "\n")

for raider in raiders:
    # Generate raider.io API URI
    uri = "https://raider.io/api/v1/characters/profile?region=tw&realm=" + urllib.parse.quote(raider["realm"]) + "&name=" + urllib.parse.quote(raider["name"]) + "&fields=mythic_plus_recent_runs"

    # Pretend to be a popular browser
    req = Request(uri, headers={"User-Agent": "Mozilla/5.0"})
    webpage = urlopen(req).read()
    soup = BeautifulSoup(webpage, features="lxml")

    # Find <p> and </p>; strip it to use in script
    dict_string = str(soup.find("p"))
    dict_string = eval(str(soup.find("p"))[3:len(dict_string) - 4])

    # Compare dates between most recent run and today
    date_leniency = 8      # This is how nice you are
    date_format = "%Y-%M-%d"
    date_raider = datetime.strptime(dict_string["mythic_plus_recent_runs"][0]["completed_at"][:10], date_format)
    date_today = datetime.strptime(str(date.today()), date_format)
    if ((date_today - date_raider).days > date_leniency):
        print(dict_string["name"], "(" + str((date_today - date_raider).days) + " days ago at " + dict_string["mythic_plus_recent_runs"][0]["dungeon"] + ")")


