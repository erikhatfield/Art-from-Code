# Python program to recursively traverse directories starting at a path
# and provide data visualization for all the sub-directories and files 
    
import bpy
import os 
    
# List to store all directories 
ListOfDir = []
    
# Traversing through '/tmp/' the default output path in blender 3 pt oh one
for root, dirs, files in os.walk('/tmp/'): 
    
    # Adding the empty directory to list 
    ListOfDir.append((root, dirs, files)) 
  
print("List of all sub-directories and files:") 
for i in ListOfDir:
    print(i)
