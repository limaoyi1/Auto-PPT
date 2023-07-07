from readconfig.myconfig import MyConfig
from chain.gpt_memory import GptChain


# 抽象父类
class Gen:
    config: MyConfig = None
    GptChain: GptChain = None

    def __init__(self, session_id):
        self.config = MyConfig()
        self.GptChain = GptChain(openai_api_key = self.config.OPENAI_API_KEY , session_id = session_id, redis_url=self.config.REDIS_URL)


# ----------------------------------------------------------------
# 生成标题
class GenTitle(Gen):
    def __init__(self, session_id):
        super().__init__(session_id)

    def predict(self, query):
        self.GptChain.predict(query)








if __name__ == '__main__':
    title = GenTitle("1111")
    title.predict("如何生成一个ppt?")
