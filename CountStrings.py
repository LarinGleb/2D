import os

path = os.path.dirname(__file__)
files = []
with os.scandir(path) as listOfEntries:  
    for entry in listOfEntries:
        if entry.is_file():
            files.append(entry.name)

        if entry.is_dir():
            with os.scandir(entry) as listOfFilesroot:
                for entryinroot in listOfFilesroot:
                    if entryinroot.is_file():
                        files.append(entry.name + '/' + entryinroot.name)

count = 0         
for i in files:
    if i.endswith(".py"):
       count += sum(1 for line in open(path + '/' + i, "r")) 

print(count)