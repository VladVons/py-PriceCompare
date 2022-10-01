from Lib.DbList import TDbRec
from .Plugin import TPluginBase


class TUsdToLocal(TPluginBase):
    def Exec(self, aRec: TDbRec) -> bool:
        if (not aRec.GetField('Price')) and (aRec.GetField('PriceUSD')):
            Price = aRec.GetField('PriceUSD') * self.Parent.Conf['USD']
            aRec.SetField('Price', Price)
