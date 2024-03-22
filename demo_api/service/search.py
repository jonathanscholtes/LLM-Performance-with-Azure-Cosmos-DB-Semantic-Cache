
from data.mongodb import search as search 

from .init import llm
from langchain.chains.combine_documents.stuff import StuffDocumentsChain
from langchain.chains.llm import LLMChain
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain.prompts import PromptTemplate
import time


from model.airesults import AIResults
from model.resource import Resource


template:str = """Use the following pieces of context to answer the question at the end.
                    If none of the pieces of context answer the question, just say you don't know.
                    If you don't know the answer, just say that you don't know, don't try to make up an answer.
                    Use three sentences maximum and keep the answer as concise as possible.

                    {context}

                    Question: {question}

                    Answer:"""


def get_query(query:str)-> list[Resource]:
    resources, docs = search.similarity_search(query)
    return resources


def get_query_summary(query:str) -> str:
    prompt_template = """Write a summary of the following:
    "{text}"
    CONCISE SUMMARY:"""
    prompt = PromptTemplate.from_template(prompt_template)

    resources, docs = search.similarity_search(query)

    if len(resources)==0:return AIResults(text="No Documents Found",ResourceCollection=resources,ResponseSeconds=0.0)

    
    start_time = time.time()
    llm_chain = LLMChain(llm=llm, prompt=prompt)

    stuff_chain = StuffDocumentsChain(llm_chain=llm_chain, document_variable_name="text")

    return AIResults(stuff_chain.run(docs),resources, ResponseSeconds=(time.time() - start_time)) 


def get_qa_from_query(query:str) -> str:
   
    resources, docs = search.similarity_search(query)

    if len(resources) ==0 :return AIResults(text="No Documents Found",ResourceCollection=resources,ResponseSeconds=0.0)

    custom_rag_prompt = PromptTemplate.from_template(template)

    def format_docs(docs):
        return "\n\n".join(doc.page_content for doc in docs)

    content = format_docs(docs)

    start_time = time.time()
    rag_chain = (
    {"context": lambda x: content , "question": RunnablePassthrough()}
    | custom_rag_prompt
    | llm
    | StrOutputParser()
    )

    return AIResults(text=rag_chain.invoke(query),ResourceCollection=resources,ResponseSeconds=(time.time() - start_time))






