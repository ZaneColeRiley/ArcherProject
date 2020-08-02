from cx_Freeze import setup, Executable
import sys

base = None

if sys.platform == "win32":
    base = "Win32GUI"

executables = [Executable("Archer.py", base=base, icon="favicon.ico")]

setup(name="Archer",
      version="1.0.0",
      options={"build_exe": {"packages": ["tkinter", "mysql", "PIL", "time", "requests", "os", "smtplib", "datetime", "pyAesCrypt"], "include_files": ["Screen_image.jpg", "favicon.ico", "Admin_screen.jpg", "Screen_image_small.jpg", "Journal.jpg", "db.sqlite3"]}},
      description="",
      executables=executables, requires=['requests', 'PIL', 'mysql', "smtplib", "tkinter", "time", "pyAesCrypt"])
