import sys
from Lib.DbList import TDbList, TDbRec


class TFExport():
    def __init__(self, aParent, aConf: dict):
        self.Conf = aConf
        self.Parent = aParent

    @staticmethod
    def GetRowInfo(aDBl: list, aMatch: list, aFileNo: int) -> tuple:
        ResPrice = sys.maxsize
        ResRecNo = -1
        for FileNo, RecNo in aMatch:
            DBl: TDbList = aDBl[FileNo]
            Rec: TDbRec = DBl.RecGo(RecNo)
            Price = Rec.GetField('Price')
            if (Price) and (Price < ResPrice):
                ResPrice = Price

            if (FileNo == aFileNo):
                ResRecNo = RecNo
        return (ResPrice, ResRecNo)

    @staticmethod
    def GetVendorIdx(aDBl: list, aName: str) -> int:
        for DBlNo, DBl in enumerate(aDBl):
            if (DBl.Tag == aName):
                return DBlNo
