import os
import re


def DynImport(aPath: str, aClass: str) -> object:
    try:
        Mod = __import__(aPath, None, None, [aClass])
        TClass = getattr(Mod, aClass, None)
        return TClass
    except ModuleNotFoundError:
        pass

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

def GetNestedKey(aData: dict, aKeys: str, aDef = None) -> object:
    for Key in aKeys.split('.'):
        if (isinstance(aData, dict)):
            aData = aData.get(Key)
            if (aData is None):
                return aDef
        else:
            return aDef
    return aData
