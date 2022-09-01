def HMDB(idd):
    import requests
    import xmltodict
    r = requests.get("http://www.hmdb.ca/metabolites/" + idd)

    read = r.content
    read = str(read)
    #Common Name

    find1 = read.find("Common Name")
    find1 = find1 + len("Common Name")

    find2 = read.find("<strong>", find1)
    find2 = find2 + len("<strong>") 

    find3 = read.find("</strong>", find2)

    Name = read[find2:find3]

    #formula
    find1 = read.find("Chemical Formula")
    find1 = find1 + len("Chemical Formula")

    find2 = read.find("<td>", find1)
    find2 = find2 + len("<td>")

    find3 = read.find("</td>", find2)

    Formula = read[find2:find3]

    Formula = Formula.replace("<sub>","")
    Formula = Formula.replace("</sub>","")

    #Biospecimen location
    find1 = read.find("Biospecimen Locations")
    find1 = find1 + len("Biospecimen Locations")

    find2 = read.find("<ul>", find1)
    find2 = find2 + len("<ul>")

    find3 = read.find("</ul>", find2)

    location = read[find2:find3]
    location = location.replace("<li>","")
    location = location.replace("</li>","")
    location = location.replace("\\n"," | ")

    return Name, Formula, location

