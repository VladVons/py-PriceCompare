import os
import re


def DirGetFiles(aPath: str, aMask: str = '.*', aSubdir: bool = False) -> list:
    Res = []
    for File in sorted(os.listdir(aPath)):
        Path = aPath + '/' + File
        if (os.path.isfile(Path)):
            if (re.search(aMask, File)):
                Res.append(Path)
        elif (aSubdir):
            Res += DirGetFiles(Path, aMask, aSubdir)
    return Res
