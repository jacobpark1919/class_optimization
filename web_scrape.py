import requests
from bs4 import BeautifulSoup
import os, sys
os.chdir(sys.path[0])

buildings = ["AGG", "BAB", "BCN", "BRB", "BUA", "CAS", "CDS", "CFA", "CGS", "COM", "CSE", "EMA", "EMB",
             "ENG", "EOP", "EPC", "ERA", "ERB", "FAB", "FCB", "FCC", "FLR", "FPH", "FRC", "GSU", "HAR", 
             "HAW", "HIL", "IEC", "IRC", "JSC", "KCB", "KHC", "LAW", "MCH", "MCS", "MET", "MOR", "MUG", 
             "OSW", "PHO", "PRB", "PSY", "PTH", "RKC", "SAC", "SAR", "SCI", "SHA", "SOC", "STH", "STO",
             "THA", "The Castle", "WED", "YAW"]


def grabBuilding(buildingCode, recursion = None):
    
    if (recursion != None ):
        buildingUrl = recursion
    else:
        buildingUrl = "https://www.bu.edu/classrooms/find-a-classroom/?cts_building%5B%5D=" + buildingCode
    result = requests.get(buildingUrl)
    if (result.status_code == 200):
        soup = BeautifulSoup(result.text, "html.parser")
        tags = soup.find_all("a", class_= "cts-button cts-button-primary")
        urls = [tag["href"] for tag in tags if tag.has_attr("href")]
        next_results = soup.find("p", class_ = "cts-next-results")
        if (next_results):
            finder = next_results.find("a")
            nextUrl = finder["href"]
            print("trying recursion on", nextUrl)
            return urls + grabBuilding(None, nextUrl) 
        else: 
            return urls    
    else:
        print("status_code wasn't 200 in grabBuilding")
        return False



def grabClassInfo(url):
    result = requests.get(url)
    if(result.status_code == 200):
        soup = BeautifulSoup(result.text, "html.parser")
        parent = soup.find("span", class_ = "meta-name", string = "Capacity")
        if(parent):
            mainTag = parent.find_next_sibling("span", class_= "meta-value")
            if(mainTag):
                capacity = mainTag.text
                print(capacity)
                return capacity
            else:
                print("no capacity found for", url)
                return False
        else:
            print("no parent found for", url)
            return False
    else:
        print("status code wasn't 200 in grabClassInfo")
        return False

def handler():
    for building in buildings:
        urls = grabBuilding(building)
        if(urls):
            for url in urls:
                capacity = grabClassInfo(url)
                if(capacity):
                    print("grabbed capacity at" , url , " and " , building)
                    save(building, url, capacity)
            print("Finished all urls")
    print("Finished all buildings")


def save(building, url, capacity):
    classroomName = url.rstrip("/").split("/")[-1]
    output = "BURoomCapacity.txt"
    line = building + "," + classroomName + "," + capacity
    with open (output, "a") as file:
        file.writelines(line + "\n")

            
if(__name__ == "__main__"):
    handler()
