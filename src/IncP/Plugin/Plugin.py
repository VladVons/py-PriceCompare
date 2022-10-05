import logging
from Inc.Util.UMod import DynImport


class TDynClass():
    def __init__(self):
        self.Data = {}

    def Create(self, aItems: list):
        for Item in aItems:
            Class = Item.get('Class')
            Alias = Item.get('Alias', Class)
            Param = Item.get('Param', {})
            if (not self.Data.get(Alias)):
                TClass = DynImport('IncP.Plugin.' + Class, 'T' + Class)
                if (TClass):
                    Obj = TClass(self, Param)
                    Obj.Alias = Alias
                    self.Data[Alias] = Obj
                else:
                    logging.error('Cant load plugin %s' % (Class))


class TPluginManager():
    def __init__(self, aParent):
        self.aParent = aParent
        self.Conf = aParent.Conf

        self.Plugin = {}
        self.Init('OnEnter')
        self.Init('OnExit')

    def Init(self, aName: str):
        Plugins = self.Conf.get(aName)
        if (Plugins):
            self.Plugin[aName] = []
            for Plugin in Plugins:
                Obj = DynClass.Data[Plugin]
                Obj.Parent = self.aParent
                self.Plugin[aName].append(Obj)

    def Exec(self, aName: str, aData) -> bool:
        Plugins = self.Plugin.get(aName)
        if (Plugins):
            for Plugin in Plugins:
                if (Plugin.Exec(aData)):
                    return True


class TPluginBase():
    def __init__(self, aParent, aParam: dict):
        self.Parent = aParent
        self.Param = aParam


DynClass = TDynClass()
