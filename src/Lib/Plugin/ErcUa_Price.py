from Lib.DbList import TDbRec
from .Plugin import TPluginBase


class TErcUa_Price(TPluginBase):
    def Exec(self, aRec: TDbRec) -> bool:
        if (aRec.GetField('Currency') == 'у.о.'):
            Price = aRec.GetField('Price') * self.Parent.Conf.get('USD')
            aRec.SetField('Price', Price)
