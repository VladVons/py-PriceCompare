import logging
import xml.etree.ElementTree as ET
from xml.dom import minidom
#
from Inc.DB.DbList import TDbList, TDbRec
from Inc.Util.UObj import GetNestedKey
from .FExport import TFExport


class TFExport_xml(TFExport):
    @staticmethod
    def Prettify(aElem) -> str:
        Rough = ET.tostring(aElem, 'utf-8')
        Reparsed = minidom.parseString(Rough)
        return Reparsed.toprettyxml(indent = '\t')

    def Save(self, aDBl: list, aMatch: dict):
        logging.info('Result: xml')

        ConfType = GetNestedKey(self.Conf, 'Type.xml')
        ConfOrder = self.Conf['Order']

        MainVendorIdx = self.GetVendorIdx(aDBl, ConfOrder[0])
        DblFinal: TDbList = aDBl[MainVendorIdx].New()

        for MatchKey, MatchVal in aMatch.items():
            Price, RecNo = self.GetRowInfo(aDBl, MatchVal, MainVendorIdx)
            if (RecNo != -1):
                Rec1 = aDBl[MainVendorIdx].RecGo(RecNo)
                Rec2 = DblFinal.RecAdd(Rec1)
                Rec2.SetField('Price', Price)
                Rec2.Flush()

        Root = ET.Element('Price')
        Element = ET.SubElement(Root, 'Catalog')

        TableEscape = ''.maketrans({
            '<': '&lt;',
            '>': '&gt;',
            '&': '&amp;',
            "'": '&apos;',
            '"': '&quot;'
            })

        ParentToName = DblFinal.ExportPair('ParentCode', 'Parent')
        for Key, Val in ParentToName.items():
            ItemA = ET.SubElement(Element, 'Category', ID = Key, ParentID = '0')
            ItemA.text = Val.translate(TableEscape)

        CategoryToName = DblFinal.ExportPair('CategoryCode', 'Category')
        CategoryToParent = DblFinal.ExportPair('CategoryCode', 'ParentCode')
        for Key, Val in CategoryToName.items():
            ItemA = ET.SubElement(Element, 'Category', ID = Key, ParentID = CategoryToParent.get(Key, '0'))
            ItemA.text = Val.translate(TableEscape)

        TransField = {
            'Mpn': 'Articul',
            'Code': 'Code',
            'Name': 'Name',
            'CategoryCode': 'CategoryID',
            'Price': 'PriceOut'
        }

        Element = ET.SubElement(Root, 'Items')
        for Rec in DblFinal:
            ItemA = ET.SubElement(Element, 'Item')
            for Key, Val in TransField.items():
                ItemB = ET.SubElement(ItemA, Val)
                ItemB.text = str(Rec.GetField(Key)).translate(TableEscape)

            ItemB = ET.SubElement(ItemA, 'PriceIn')
            ItemB.text = '0'
            ItemB = ET.SubElement(ItemA, 'Quantity')
            ItemB.text = '1'

        print('CategoryParent %s' % (len(ParentToName)))
        print('Category %s' % (len(CategoryToName)))
        print('Products %s' % (DblFinal.GetSize()))
        ConfFile = ConfType['File']
        logging.info('Save %s'  % (ConfFile))

        #Tree = ET.ElementTree(Root)
        #Tree.write(ConfFile, 'utf-8')

        Data = self.Prettify(Root)
        with open(ConfFile, 'w') as File:
            File.write(Data)
