#This file is Zeran's footprint of learning the os module in Python.
import os
from datetime import datetime

#method that returns the path to the current working directory as a String.
print(os.getcwd())

#method that navigates to a new location.
os.chdir("/Users/simon/autograder_CP/autograder_CP_24Fall/")
print(os.getcwd())

#method that returns a list that contains files and folders are in the current directory.
"""can be used to get the filename of files, to get students' names."""
print(os.listdir())

#create a folder on the current working directory.
#os.mkdir("goody_test") #delete the folder you created

#same to .mkdir(), but can make deep folders
#os.makedirs("goody_test/bady_test") #delete the folder you created

#delete folders. If the file does not exist, would raise an error.
#os.rmdir("")
#os.removedirs("")

#rename folders/filesd
#os.rename("old.txt", "new.txt")

#os.stat(): method that returns information about the file.
#.st_mtime: attribute that shows last time that the file was modified.
""".st_mtime can be a useful attribute to determine if a student submits hw late."""
"""deadline = datetime(2024, 12, 25, 23, 59, 59)"""
t_stp = os.stat("os_test.py").st_mtime
date_time = datetime.fromtimestamp(t_stp)
print(date_time)#would always returns the time I changed this py file.

#os.walk(): pre-order traverse each directory in the argument directory.
#root: directories only from what you specified.
#dirs: sub-directories from root.
#files: files in this directory.
for root, dirs, files in os.walk(".", topdown = True):
    print("Current Path:", root)
    print("Directories within:", dirs)
    print("Files within: ", files)
    print()

#os.path.basename("path_name")
#os.path.dirname("path_name")
#os.path.split("path_name"): list format: [dirname, filename]
#os.path.exists("if_path_name_really_exists_in_dir_system")
#os.path.isdir("return true if the path is a directory")
#os.path.isfile("return true if the path is a file")
path_and_extension = os.path.splitext("./autograder_CP_24Fall/os_test.py")
print(path_and_extension)
print()

print(dir(os.path)) #for more methods!

"""You were here!"""
#learn with open ..... file.... as...
