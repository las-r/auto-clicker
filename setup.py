from cx_Freeze import setup, Executable

setup(
    name = "Auto Clicker",
    description = "An auto clicker by Nayif E.",
    executables = [Executable("autoclicker.py", base="Win32GUI", icon="icon.ico")],
)
