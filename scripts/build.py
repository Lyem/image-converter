import PyInstaller.__main__
from pathlib import Path
from sys import platform

is_posix = platform.startswith(("darwin", "cygwin", "linux", "linux2"))
is_mac = platform.startswith('darwin')

src_path = Path(__file__).resolve().parent.parent / 'src'
path_to_main = str(src_path / 'main.py')

separator = ':' if is_posix else ';'

args = [
    path_to_main,
    '--onefile',
    '--noconfirm',
    '--noconsole',
    f'--icon=assets/icon.ico',
]

def install():
    PyInstaller.__main__.run(args)