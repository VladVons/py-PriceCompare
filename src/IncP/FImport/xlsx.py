'''
VladVons@gmail.com
2022.09.24
'''


from openpyxl import load_workbook
from .FImport import TFImport


class TFImport_xlsx(TFImport):
    def Load(self, aName):
        WB = load_workbook(aName, read_only = True, data_only = True)

        ConfSheet = self.Conf.get('Sheet')
        if (ConfSheet):
            WS = WB[ConfSheet]
        else:
            WS = WB.active

        ConfFields = self.Conf.get('Fields')
        ConfSkip = self.Conf.get('Skip', 0)
        for RowNo, Row in enumerate(WS.rows):
            if (RowNo >= ConfSkip):
                Data = {'No': RowNo}
                for Field, (FieldIdx, _) in ConfFields.items():
                    Val = Row[FieldIdx - 1].value
                    Data[Field] = Val
                self.AddItem(Data)

