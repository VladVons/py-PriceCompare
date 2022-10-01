from .Plugin import TPluginBase


class THasValue(TPluginBase):
    def Exec(self, aData: dict) -> bool:
        for Field in self.Param:
            if (not aData.get(Field)):
                return True
