import os
import logging
from tqdm import tqdm
import yaml
from dotenv import load_dotenv
import wikipedia
from langchain.chat_models import ChatOpenAI
from langchain.agents import load_tools, initialize_agent, AgentType

# Load environment variables from .env file
load_dotenv()

# Load configuration
with open("../config.yaml", "r") as f:
    CONFIG = yaml.safe_load(f)

# Setup logging
if not os.path.exists(CONFIG["logs_folder"]):
    os.makedirs(CONFIG["logs_folder"])
logging.basicConfig(
    filename=os.path.join(CONFIG["logs_folder"], CONFIG["log_file"]),
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

llm = ChatOpenAI(temperature=0)
tools = load_tools(['serpapi', 'wikipedia', 'llm-math'], llm=llm)

# Initialize the agent
agent = initialize_agent(tools=tools, llm=llm, agent=AgentType.CHAT_ZERO_SHOT_REACT_DESCRIPTION, verbose=True)

if __name__ == "__main__":
    user_input = input("Enter your query: ")
    response = agent.run(user_input)
    print(f"Bot: {response}")
