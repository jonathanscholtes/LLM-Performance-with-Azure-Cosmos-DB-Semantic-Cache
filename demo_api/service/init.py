
from dotenv import load_dotenv
from langchain.globals import set_llm_cache
from langchain_openai import ChatOpenAI
from data.mongodb.init import semantic_cache


load_dotenv(override=True)


llm : ChatOpenAI | None=None

def LLM_init():
    global llm
    llm = ChatOpenAI(model_name="gpt-3.5-turbo-16k",temperature=0)
    set_llm_cache(semantic_cache) ##comment this line to turn-off cache

LLM_init()

