import cx_Freeze, sys

base = None
if sys.platform == "win32":
    base = "Win32GUI"

executables = [cx_Freeze.Executable("main.py")]

cx_Freeze.setup(
    name="The Life of Robert",
    version = "1.0",
    description = "Fun and more Fun",
    author = "Andre van Tonder",
    options={"build_exe": {"packages":["pygame","random","pytmx"],
                           "include_files":["Images/","Sounds/","Maps/","Houses/","OptimusPrinceps.ttf"]
                           }},
    executables = executables
    )
