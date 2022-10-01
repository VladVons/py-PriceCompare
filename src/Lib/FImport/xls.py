'''
VladVons@gmail.com
2022.09.24
'''


from xlrd import open_workbook
from .FImport import TFImport


class TFImport_xls(TFImport):
    def Load(self, aName: str):
        WB = open_workbook(aName)

        Sheet = self.Conf.get('Sheet')
        if (Sheet):
            WS = WB.sheet_by_name(Sheet)
        else:
            WS = WB.sheet_by_index(0)

        ConfFields = self.Conf.get('Fields')
        ConfSkip = self.Conf.get('Skip', 0)
        for i in range(ConfSkip, WS.nrows):
            Data = {'No': i}
            for Field, (FieldIdx, _) in ConfFields.items():
                Val = WS.cell(i, FieldIdx - 1).value
                Data[Field] = Val
            self.AddItem(Data)
