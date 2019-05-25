import urllib.parse
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
from datetime import datetime, date

# Realm names
realmA = "Light's Hope"
realmB = "Skywall"
realmC = "Wrathbringer"

# Raiders
raiders = [
    { "name": "Darc", "realm": realmA },
    { "name": "龍蝦三爭霸", "realm": realmA },
    { "name": "喔啊啊布德爾", "realm": realmC },
    { "name": "阿強號", "realm": realmA },
    { "name": "香茅千層蛋糕", "realm": realmA },
    { "name": "沙發破一個洞", "realm": realmA },
    { "name": "緋月淮星", "realm": realmA },
    { "name": "妹妹大人", "realm": realmB },
    { "name": "快來踩我", "realm": realmB },
    { "name": "一灰羽一", "realm": realmA },
    { "name": "Yoyoman", "realm": realmB },
    { "name": "嬌穴組長", "realm": realmB },
    { "name": "貓語者", "realm": realmB },
    { "name": "Seraphen", "realm": realmA },
    { "name": "撞牆當練功", "realm": realmA },
    { "name": "闇之咒術師", "realm": realmA },
    { "name": "江城子", "realm": realmA },
    { "name": "伊蘇露", "realm": realmA },
    { "name": "絕緋", "realm": realmA },
    { "name": "阿魔達", "realm": realmA },
    { "name": "Yinuo", "realm": realmB },
    { "name": "性感大蘿蔔", "realm": realmA },
    { "name": "一塊錢的功德", "realm": realmB },
    { "name": "開朗小露娜", "realm": realmA },
    { "name": "安琪莉可可", "realm": realmB },
    { "name": "遺忘賽德勒斯", "realm": realmA },
    {"name": "Latina", "realm": realmA},
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


