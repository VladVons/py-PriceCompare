from .Plugin import TPluginBase


class TBrainComUa_UrlImg(TPluginBase):
    def Exec(self, aData: dict) -> bool:
        Url = "https://opt.brain.com.ua/static/images/prod_img/2/6/U0540526.jpg"
        aData.get('URL')
