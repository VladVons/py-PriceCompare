'''
VladVons@gmail.com
2022.09.24
'''


import csv
from .FImport import TFImport


class TFImport_csv(TFImport):
    def Load(self, aName):
        ConfEncoding = self.Conf.get('Encoding', 'cp1251')
        with open(aName, 'r',  encoding=ConfEncoding, errors='ignore') as File:
            Rows = csv.reader(File, delimiter = ',')

            ConfSkip = self.Conf.get('Skip', 0)
            for _i in range(ConfSkip):
                next(Rows)

            ConfFields = self.Conf.get('Fields')
            for RowNo, Row in enumerate(Rows, ConfSkip):
                Data = {'No': RowNo}
                for Field, (FieldIdx, _) in ConfFields.items():
                    Val = Row[FieldIdx - 1]
                    Data[Field] = Val
                self.AddItem(Data)
