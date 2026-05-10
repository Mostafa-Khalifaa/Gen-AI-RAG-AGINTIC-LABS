from langchain.chat_models import init_chat_model
from langchain_core.prompts import PromptTemplate

def get_answer(db, question):
    similar_chunks = db.similarity_search(question, k=3)
    context = "\n".join([chunk.page_content for chunk in similar_chunks])
    sources = [chunk.page_content for chunk in similar_chunks]
    
    llm = init_chat_model("gpt-4o-mini", temperature=0.2) 
    
    rag_template = PromptTemplate(
        template="""
        You are a specialized customer service agent for the provided document.
        Read the user's question and follow THESE STRICT RULES:
        
        - YOU MUST ALWAYS ANSWER IN ENGLISH.
        
        1. Out of Scope: If the user's question is completely unrelated to the content of the document, DO NOT answer. Reply EXACTLY with: "Welcome! I am a customer service assistant dedicated to answering questions related to this document only, and I cannot assist you with outside topics."
        2. In Scope: If the question asks for specific details, OR asks for general tasks like summarizing the document, listing skills, or describing what is in the file, THIS IS IN SCOPE. Use the provided context to fulfill the request.
        3. Not Found: If the question is in scope BUT the provided context does not contain any relevant information, reply with exactly: "I do not know."

        Context: {context}
        Question: {question}
        
        Answer:
        """,
        input_variables=['context', 'question']
    )
    
    res = llm.invoke(rag_template.format(context=context, question=question))
    
    return {
        "answer": res.content,
        "sources": sources
    }