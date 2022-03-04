# Python program to recursively traverse directories starting at a path
# and provide data visualization for all the sub-directories and files 

import bpy
import os 

# Lists to store all directories, paths, and roots
ListOfAll = []
ListOfDirs = []
ListOfFiles = []
ListOfRoots = []

# Traversing through '/tmp/' the default output path in blender 3 pt oh one
for root, dirs, files in os.walk('/tmp/'): 

    # Adding the empty directory to list 
    ListOfAll.append((root, dirs, files)) 
    ListOfDirs.append((dirs)) 
    ListOfFiles.append((files)) 
    ListOfRoots.append((root)) 
  
print("List of all sub-directories and files:") 
for i in ListOfAll:
    print(i)

print("\n\n")

print("List of all directories:") 
for i in ListOfDirs:
    print(i)

print("\n\n")

print("List of all files:") 
for i in ListOfFiles:
    print(i)

print("\n\n")

print("List of all roots:") 
for i in ListOfRoots:
    print(i)


