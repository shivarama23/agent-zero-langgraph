from utils.env import *
from utils.messages import pretty_print_messages
from supervisor.main import supervisor

query = "Get the stock price of TCS and INFosys in the last 10 days and create a graph comparing them, put that graph in a ppt for presentation."

for chunk in supervisor.stream({"messages": [{"role": "user", "content": query}]}):
    pretty_print_messages(chunk)

final_message_history = chunk["supervisor"]["messages"]
