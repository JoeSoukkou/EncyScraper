import os 

virt_env = "python3.11 -m venv encyenv; source encyenv/bin/activate"
os.system(virt_env)
command = "pip install "
dependencies = ["PySide2","bs4","requests","PyQt5"]
for dependency in dependencies: 
    install = "{COMMAND} {DEPENDENCY}".format(COMMAND=command, DEPENDENCY=dependency)
    os.system(install)
