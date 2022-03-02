import os 

command = "pip install"
dependencies = ["PySide2","bs4","requests","PyQt5"]

for dependency in dependencies: 
    install = "{COMMAND} {DEPENDENCY}".format(COMMAND=command, DEPENDENCY=dependency)
    os.system(install)