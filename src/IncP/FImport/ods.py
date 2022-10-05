'''
VladVons@gmail.com
2022.09.24
'''


from pyexcel_ods import get_data
from .FImport import TFImport


class TFImport_ods(TFImport):
    def Load(self, aName):
        Data = get_data(aName)

        ConfSheet = self.Conf.get('Sheet')
        if (ConfSheet):
            Sheet = ConfSheet
        else:
            Sheet = list(Data.keys())[0]

        ConfSkip = self.Conf.get('Skip', 0)
        Rows = Data.get(Sheet)

        ConfFields = self.Conf.get('Fields')
        for i in range(ConfSkip, len(Rows)):
            Data = {'No': i}
            for Field, (FieldIdx, _) in ConfFields.items():
                Val = Rows[i][FieldIdx - 1]
                Data[Field] = Val
            self.AddItem(Data)
