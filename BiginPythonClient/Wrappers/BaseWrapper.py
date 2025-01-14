

class BaseWrapper():
    dict = None
    client = None
    loginSesison = None
    def __init__(self, client, loginSession, dict):
        self.client = client
        self.loginSession = loginSession
        self.dict = dict

class ArrayWrapper(BaseWrapper):
    items = None
    def __init__(self, client, loginSession, dict, array_tag):
        super().__init__(client, loginSession, dict)
        self.items = []
        for x in dict[array_tag]:
            self.items.append(self.itemFactory(x))

    def itemFactory(self, item):
        return item