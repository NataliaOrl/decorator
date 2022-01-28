import csv
import re
from logger_decorator import decor

def get_contacts(contacts_list):
    contacts = []
    for el in contacts_list:
        if len(el[0].split()) == 3:
            lastname = el[0].split()[0]
            firstname = el[0].split()[1] 
            surname = el[0].split()[2]
        elif len(el[0].split()) == 2:
            lastname = el[0].split()[0]
            firstname = el[0].split()[1] 
            surname = el[1]  
        else:
            lastname = el[0].split()[0]
            firstname = el[1] if len(el[1].split()) == 1 else el[1].split()[0]
            surname = el[2] if len(el[1].split()) == 1 else el[1].split()[1]
        organization = el[3]
        position = el[4]
        email = el[6]
        if 'доб' in el[5]:
            phone = re.sub(r'(\+7|8).*?(\d{3}).*?(\d{3}).*?(\d{2}).*?(\d{2})\s*\(*доб\.*\s*(\d+)*\)*', r'+7(\2)\3-\4-\5 доб.\6', el[5])
        else:
            phone = re.sub(r'(\+7|8).*?(\d{3}).*?(\d{3}).*?(\d{2}).*?(\d{2})', r'+7(\2)\3-\4-\5', el[5])
        contacts.extend([lastname, firstname, surname, organization, position, phone, email])
    return contacts

@decor()
def get_list(contacts, column=7):
    contacts_new = [contacts[x:column+x] for x in range(0,len(contacts),column)]
    return contacts_new

def find_duplicates(contacts):
    dupl = []
    d = []
    for el in contacts:
        dupl.extend([el[0]])
    for duplicate in dupl:
        if dupl.count(duplicate) > 1:
            if duplicate not in d:
                d.append(duplicate)
    return d

def get_indices(list, duplicates):
    index = []
    for el in duplicates:
        index.extend([[i for i in range(len(list)) if list[i] == el]])
    return index

def upgrade_contacts(contacts, index):
    for [a, b] in index:
        for i in range(2, 7):
            if contacts[a + 1] != contacts[b + 1]:
                break
            else:
                if contacts[a + i] == contacts[b +i] or contacts[a + i]:
                    continue
                elif contacts[b + i]:
                    contacts[a + i] = contacts[b + i]
    for el in index[::-1]:
        del contacts[el[1]:(el[1] + 7)]
    return contacts

if __name__ == '__main__':
      
    with open("phonebook_raw.csv", encoding="utf-8") as f:
        rows = csv.reader(f, delimiter=",")
        contacts_list = list(rows)

    getContacts = get_contacts(contacts_list)
    getList = get_list(getContacts)
    findDuplicates = find_duplicates(getList)
    getIndices = get_indices(getContacts, findDuplicates)
    upgradeContacts = upgrade_contacts(getContacts, getIndices)
    get_List_new = get_list(upgradeContacts)

    with open("phonebook_2.csv", "w", newline='', encoding="utf-8") as f:
        datawriter = csv.writer(f, delimiter=',')
        datawriter.writerows(get_List_new)
