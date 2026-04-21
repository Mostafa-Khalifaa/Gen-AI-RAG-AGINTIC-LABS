import base64
import uuid
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage
from langgraph.checkpoint.memory import MemorySaver
from langgraph.prebuilt import create_react_agent
class ChefChatbot:
    def __init__(self):
        self.my_memory = MemorySaver()
        self.rules = """You are a professional, friendly chef. Speak like a real chef.
        Your rules:
        1. Accept the ingredients the user has.
        2. Guide the user step-by-step to a meal decision. NEVER skip steps.
        3. First, suggest 2-3 simple meal ideas. Wait for their choice.
        4. Once they choose, give them the recipe.
        """
        self.reset_chat()
    def reset_chat(self):
        self.my_memory = MemorySaver()
        self.my_config = {"configurable": {"thread_id": "current_session"}}

    def ask_chef(self, text, image_file, temp_val, size):
        final_txt = f"{text} (Please keep your response {size})"
        msg_content = [{"type": "text", "text": final_txt}]
        
        if image_file:
            img_data = base64.b64encode(image_file.read()).decode('utf-8')
            msg_content.append({
                "type": "image_url",
                "image_url": {"url": f"data:image/jpeg;base64,{img_data}"}
            })
        
        my_model = ChatOpenAI(model="gpt-4o-mini", temperature=temp_val)
        
        my_agent = create_react_agent(
            my_model, 
            tools=[], 
            checkpointer=self.my_memory, 
            prompt=self.rules
        )
        
        user_msg = HumanMessage(content=msg_content)
        result = my_agent.invoke({"messages": [user_msg]}, config=self.my_config)
        
        return result["messages"][-1].content