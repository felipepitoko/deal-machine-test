# Import relevant functionality
from langchain.chat_models import init_chat_model
from langgraph.prebuilt import create_react_agent

from dotenv import load_dotenv
import json

load_dotenv()

def analyze_ai_agent(message:str)->dict:
    try:
        if not message:
            print('No message sent to the agent')
            return None
        
        # Create the agent
        model = init_chat_model("google_genai:gemini-2.0-flash")
        agent_executor = create_react_agent(model, tools=[])

        # Use the agent
        config = {"configurable": {"thread_id": "abc123"}}

        input_messages = [
            {
                "role": "system",
                "content": (
                    "All your answers will be in brazilian portuguese."
                    "Analyze the message and output the intention of the one who sent it, in two words."
                    "Analyze the message and output the keywords in it."
                    "Guess the feeling of the user who sent the message."
                    "Your output must be only JSON objects with keys 'keywords', 'feeling' and 'intention', each one a list of what you've found."
                )
            },
            {
                "role": "user",
                "content": message
            }
        ]

        results = []
        import re

        def extract_json(text):
            # Find the first {...} or [...] block in the text
            match = re.search(r'({[\s\S]*?})', text)
            if match:
                try:
                    return json.loads(match.group(1))
                except Exception:
                    return None
            return None

        for step in agent_executor.stream(
            {"messages": input_messages}, config, stream_mode="values"
        ):
            # step["messages"][-1].pretty_print()
            output = step["messages"][-1].content
            json_obj = extract_json(output)
            if json_obj:
                results.append(json_obj)

        if results:
            print(results[-1])  # Print only the last valid JSON object
            return results[-1]
        else:
            print("No valid JSON found in agent response.")
    except Exception as e:
        print(e)
        
if __name__ == "__main__":
    analyze_ai_agent("Tell me some news about a unicorn.")