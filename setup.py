import pkgutil
from cx_Freeze import setup, Executable

# functions
def AllPackage(): 
    return [i.name for i in list(pkgutil.iter_modules()) if i.ispkg]
def notFound(A,v):
    try: 
        A.index(v) 
        return False
    except: 
        return True

# app settings
APPNAME = "Auto Clicker"
DESCRIPTION = "An auto clicker made by las-r on GitHub. @COPYRIGHT 2025 NAYIF EHAN"
VERSION = "1.0.1"
FILENAME = "autoclicker.py"
INCLUDEDFILES = "icon.ico"
ICONPATH = "icon.ico"
LIBRARIES = ["tkinter", "ttkthemes", "keyboard"]
PACKAGES = ["ctypes", "re", "PIL", "logging", "json"]

# exclude unneed packages
BasicPackages = ["collections", "encodings", "importlib"] + LIBRARIES
build_exe_options = {
    "include_files": INCLUDEDFILES,
    "includes": BasicPackages,
    "excludes": [i for i in AllPackage() if notFound(BasicPackages, i)],
    "packages": PACKAGES
}

# setup
setup(name = APPNAME,
      description = DESCRIPTION,
      version = VERSION,
      options = {"build_exe": build_exe_options},
      executables = [Executable(FILENAME, base='Win32GUI', icon=ICONPATH)]
)
