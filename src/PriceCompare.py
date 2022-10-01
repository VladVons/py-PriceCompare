'''
VladVons@gmail.com
2022.09.23

Compare prices from *.xls, *.xlsx, *.csv by Mpn
Create new xlsx file as result

iconv -f cp1251 -t UTF-8 kts.ua.csv -o kts.ua.csv.txt
https://openpyxl.readthedocs.io/en/stable/styles.html
USD = 'https://bank.gov.ua/NBUStatService/v1/statdirectory/exchange?valcode=USD&json'
'''


import os
import sys
import json
import time
import logging
#
from Lib.DbList import TDbList
from Lib.Common import DirGetFiles, DynImport, GetNestedKey
from Lib.Plugin.Plugin import DynClass


class TConf(dict):
    @staticmethod
    def Join(aMaster: dict, aSlave: dict) -> dict:
        for Key, Val in aSlave.items():
            if (isinstance(Val, list)):
                Val += aMaster.get(Key, [])
            elif (isinstance(Val, dict)):
                Val.update(aMaster.get(Key, {}))

            aMaster[Key] = Val

    @staticmethod
    def _GetVendor(aConf: dict, aName: str) -> dict:
        Res = aConf.get('Common', {}).copy()
        Conf = aConf.get('Vendor', {}).get(aName)
        if (Conf):
            Vendor = Conf.get('VendorRef')
            if (Vendor):
                Conf = aConf.get('Vendor').get(Vendor)
            Res.update(Conf)
        return Res

    def GetVendor(self, aFile: str) -> dict:
        Res = self._GetVendor(self, aFile)
        if (Res):
            Dir = self.get('DirConf')
            if (Dir):
                Files = DirGetFiles(Dir, '.json')
                for File in Files:
                    Conf = self.Read(File)
                    Conf = self._GetVendor(Conf, aFile)
                    if (File.endswith('_add.json')):
                        self.Join(Res, Conf)
                    else:
                        Res.update(Conf)
        return Res

    def Read(self, aFile: str):
        with open(aFile, 'r') as File:
            return json.load(File)

    def Load(self):
        Data = self.Read('conf.json')
        super().__init__(Data)



class TParse():
    def __init__(self):
        self.Conf = TConf()
        self.Conf.Load()

        Plugins = GetNestedKey(self.Conf, 'Common.Plugin', {})
        DynClass.Create(Plugins)

    def GetFiles(self) -> list:
        Dir = self.Conf.get('DirPrice')
        return DirGetFiles(Dir, '(.xls$|.xlsx$|.ods$|.csv$|.json$)')

    def LoadFile(self, aName: str) -> TDbList:
        #logging.info('load file %s' % (aName))

        FileName = os.path.basename(aName)
        ConfVendor = self.Conf.GetVendor(FileName)
        Ext = os.path.splitext(FileName)[1][1:]
        if (ConfVendor):
            TimeStart = time.time()
            Ext = ConfVendor.get('Module', Ext)
            TClass = DynImport('Lib.FImport.' + Ext, 'TFImport_' + Ext)
            if (TClass):
                Class = TClass(ConfVendor)
                Class.Load(aName)
                Class.Dbl.Tag = FileName
                logging.info('File: %20s, Records: %6s, Time: %0.2f' % (FileName, Class.Dbl.GetSize(), time.time() - TimeStart))
                return Class.Dbl
            else:
                logging.error('File: %s, Unknown format' % (aName))
        else:
            logging.error('File: %s, Unknown format' % (aName))
            sys.exit(1)

    def LoadFiles(self, aFiles: list) -> list:
        ArrDBl = []
        Match = {}
        for FileNo, File in enumerate(aFiles):
            DBl = self.LoadFile(File)
            if (DBl):
                Uniq = {}
                for RecNo, Rec in enumerate(DBl):
                    Mpn = Rec.GetField('Mpn')
                    if (not Match.get(Mpn)):
                        Match[Mpn] = []

                    UniqVal = Uniq.get(Mpn, 0) + 1
                    Uniq[Mpn] = UniqVal
                    if (UniqVal < 2):
                        Match[Mpn].append((FileNo, RecNo))
            ArrDBl.append(DBl)

        ConfMatches = self.Conf.get('Matches', 2)
        Match = {Key: Val for Key, Val in Match.items() if len(Val) >= ConfMatches}
        return (ArrDBl, Match)

    def Save(self, aDBl: list, aMatch: dict):
        for x in self.Conf.get('Resultes'):
            TClass = DynImport('Lib.FExport.' + x, 'TFExport_' + x)
            if (TClass):
                Conf = self.Conf['Result']
                Class = TClass(self, Conf)
                Class.Save(aDBl, aMatch)

def Main():
    AppName = os.path.basename(sys.argv[0])
    print('%s, v1.02, 2022.09.27, vladvons@gmail.com' % (AppName))

    logging.basicConfig(
        level=logging.INFO,
        format = '%(asctime)s [%(levelname)s] %(message)s',
        datefmt = '%Y-%m-%d %H:%M:%S',
        handlers = [
            logging.FileHandler(AppName + '.log'),
            logging.StreamHandler()
        ]
    )

    TimeStart = time.time()
    Parse = TParse()
    Files = Parse.GetFiles()
    Matches = Parse.LoadFiles(Files)
    Parse.Save(Matches[0], Matches[1])
    logging.info('Done. Time %0.2f' % (time.time() - TimeStart))

Main()
