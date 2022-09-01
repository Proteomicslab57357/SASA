'''
Retrive by formila
get the id
search by id on the pathway hits
'''
def KEGG(formula,Name):
    from Bio.KEGG import Compound
    from Bio.KEGG import REST
    import time

    ## get all the id that has formula x
    formula_list = list(REST.kegg_find("compound", str(formula), "formula"))
    Id_list = []
    for i_get_id in formula_list:
        try:
            entry, description = i_get_id.split("\t")
        except:
            break
        if str(description.strip()) == formula:
            Id_list.append(entry.strip())
    Id_list = set(Id_list)
    #get the infromation about each id and filter by name for the darget one
    true_list = []
    for i_each_id in Id_list:
        time.sleep(1)
        info_fake = REST.kegg_get(i_each_id)
        open("KEGG.txt", "w").write(info_fake.read())
        records = Compound.parse(open("KEGG.txt"))
        true = False
        for i_info in records:
            if Name in i_info.name:
                true = True
            else:
                true_list.append("False")
        if true:
            break

    if len(true_list) == len (Id_list):
        path_id = ''
        path_name = ''
        return path_name, path_id
    else:
        records = Compound.parse(open("KEGG.txt"))
        for i_pathway in records:
            list_path = i_pathway.pathway

        path_id = [i[1] for i in list_path]
        path_name = [i[2] for i in list_path]

        return path_id, path_name

