from .Plugin import TPluginBase


class TWordsSkip(TPluginBase):
    def Exec(self, aData: dict) -> bool:
        Category = aData.get('Category')
        if (Category):
            Category = Category.lower()

            Words = self.Param.get('Whole')
            if (Words) and (Category in Words):
                return True

            Words = self.Param.get('Part')
            if (Words) and (any(x in Category for x in Words)):
                return True
