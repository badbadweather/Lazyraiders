import urllib.parse
from datetime import datetime, date
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
from prettytable import PrettyTable

# Config -- a.k.a. how nice you are
date_leniency = 8           # Recommended: 8    Number of days w/o Mythic+ run before reporting.
minimum_mythic_level = 10   # Recommended: 10   Minimum Mythic+ level to count as a run; set to 0 if you don't care.

# Config -- realm names
realmA = "realmA"
realmB = "realmB"
realmC = "realmC"

# Config -- raiders
raiders = [
    { "name": "raiderD", "realm": realmA },
    { "name": "raiderE", "realm": realmB },
    { "name": "raiderF", "realm": realmC },
]

report = PrettyTable(["Name", "ilv", "Report"])

print("\n" + "Checking raider.io data..." + "\n")

for raider in raiders:
    # Generate raider.io API URI
    uri = "https://raider.io/api/v1/characters/profile?region=tw&realm=" + urllib.parse.quote(raider["realm"]) + "&name=" + urllib.parse.quote(raider["name"]) + "&fields=mythic_plus_recent_runs"

    # Pretend to be a popular browser
    req = Request(uri, headers={"User-Agent": "Mozilla/5.0"})
    soup = BeautifulSoup(urlopen(req).read(), features="lxml")

    # Find <p> and </p>; strip it to use in script
    dict_string = str(soup.find("p"))
    dict_string = eval(str(soup.find("p"))[3:len(dict_string) - 4])

    # Repeat steps for item levels
    uri_ilv = "https://raider.io/api/v1/characters/profile?region=tw&realm=" + urllib.parse.quote(raider["realm"]) + "&name=" + urllib.parse.quote(raider["name"]) + "&fields=gear"
    req_ilv = Request(uri_ilv, headers={"User-Agent": "Mozilla/5.0"})
    soup_ilv = BeautifulSoup(urlopen(req_ilv).read(), features="lxml")
    dict_string_ilv = str(soup_ilv.find("p"))
    dict_string_ilv = eval(str(soup_ilv.find("p"))[3:len(dict_string_ilv) - 4])

    # Check against minimum_mythic_level
    runs = len(dict_string["mythic_plus_recent_runs"]) - 1
    while runs >= 0:
        if (int(dict_string["mythic_plus_recent_runs"][runs]["mythic_level"]) < minimum_mythic_level):
            del dict_string["mythic_plus_recent_runs"][runs]
            runs -= 1
        else:
            runs -= 1

    # Safety net against the void
    if (len(dict_string["mythic_plus_recent_runs"]) == 0):
        report.add_row([dict_string["name"], str(dict_string_ilv["gear"]["item_level_total"]), "No data"])

    if (len(dict_string["mythic_plus_recent_runs"]) != 0):

        # Compare dates between most recent run and today
        date_format = "%Y-%m-%d"
        date_raider = datetime.strptime(dict_string["mythic_plus_recent_runs"][0]["completed_at"][:10], date_format)
        date_today = datetime.strptime(str(date.today()), date_format)

        if ((date_today - date_raider).days > date_leniency):
            report.add_row([dict_string["name"], str(dict_string_ilv["gear"]["item_level_total"]), str((date_today - date_raider).days) + " days ago at " + dict_string["mythic_plus_recent_runs"][0]["dungeon"]])

# Set up reporting table
report.align = "l"
report.right_padding_width = 2

print(report.get_string(sortby = "ilv"))
