from Lib.DbList import TDbList
from Lib.Plugin.Plugin import TPluginManager, DynClass


class TFImport():
    def __init__(self, aConf: dict):
        self.Conf = aConf

        Fields = [('No', int), ('Price', float)]
        for Name, (Idx, Type) in aConf.get('Fields').items():
            Obj = {'float': float, 'int': int}.get(Type, str)
            if (not Name in ['No', 'Price']):
                Fields.append((Name, Obj))
        self.Dbl = TDbList(Fields)

        self.Types = {Name:Type for (Name, Type) in Fields}

        DynClass.Create(self.Conf['Plugin'])
        self.Plugin = TPluginManager(self)

    @staticmethod
    def ToFloat(aVal: str) -> float:
        if (not aVal):
            aVal = 0
        elif (isinstance(aVal, str)):
            aVal = aVal.replace(',', '.').replace(' ', '')

        try:
            aVal = float(aVal)
        except ValueError:
            aVal = 0.0
        return aVal

    def AddItem(self, aData: dict):
        if (self.Plugin.Exec('OnEnter', aData)):
            return

        #if (aData['Mpn'] == 'BK650EI'):
        #    print('--x', aData['Mpn'])

        Rec = self.Dbl.RecAdd()
        for Key, Val in aData.items():
            Type = self.Types[Key]
            if (Key == 'Mpn'):
                if (not isinstance(Val, str)):
                    Val = str(int(Val))
                Remove = ''.maketrans('', '', ' -/_.&@()#+')
                Val = Val.translate(Remove).upper().strip()
            elif ('Code' in Key) and (not isinstance(Val, str)):
                Val = str(int(Val))
            elif (Type == float) and (not isinstance(Val, Type)):
                Val = self.ToFloat(Val)

            Rec.SetField(Key, Val)

        self.Plugin.Exec('OnExit', Rec)
        Rec.Flush()
