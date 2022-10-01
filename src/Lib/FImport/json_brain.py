'''
VladVons@gmail.com
2022.09.24

cat price_brain_all.json | json_reformat > price_brain_human.json
'''


import json
from .FImport import TFImport


class TFImport_json_brain(TFImport):
    def Load(self, aName):
        with open(aName, 'r') as File:
            SrcData = json.load(File)

        ConfFields = self.Conf.get('Fields')
        for RowNo, (_, Val) in enumerate(SrcData.items()):
            Data = {'No': RowNo}
            for Field, (FieldName, _) in ConfFields.items():
                Data[Field] = Val[FieldName]
            self.AddItem(Data)


