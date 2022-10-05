from .Plugin import TPluginBase


class THasMpnPrice(TPluginBase):
    def Exec(self, aData: dict) -> bool:
        if (not aData['Mpn']):
            return True

        if (not aData.get('Price')) and (not aData.get('PriceUSD')):
            return True
