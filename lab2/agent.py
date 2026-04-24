from dotenv import load_dotenv
load_dotenv()   
from langchain.agents import create_agent
from langgraph.checkpoint.memory import InMemorySaver    
from langchain.agents.middleware import SummarizationMiddleware
from tools import WebSearch, StoreCase
from middleware import trim_messages


medical_prompt = """ you are a medical assistant agent that helps patients to find 
the nearst hospital based on their daignoses 
user will upload images or lab results and provide the patient information .
you have a tool for searching web for nearst hospital based on daignoses and location if user asks for it.
you have a tool for storing patient case data into a csv file if user asks for it.
you should use the tools when needed and you should not use them if not needed.
do not provide a diagnosis or prescriptions.
always end your response with: This is not a medical diagnosis. Consult a doctor.
"""

doctor = create_agent(
    model='gpt-4o-mini',          
    system_prompt=medical_prompt,
    checkpointer=InMemorySaver(),  
    tools=[WebSearch, StoreCase], 
    middleware=[
        trim_messages,             
        SummarizationMiddleware(   
            model="gpt-4o-mini",
            trigger=("tokens", 500),
            keep=("messages", 1)
        )
    ]
)