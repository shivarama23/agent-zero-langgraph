from utils.env import *
from utils.messages import pretty_print_messages
from supervisor.main import supervisor

query = "Get the latest news about Narendra Modi by searching in google.com and summarize it. Write this summary back into a PPT with 3 slides"

for chunk in supervisor.stream({"messages": [{"role": "user", "content": query}]}):
    pretty_print_messages(chunk)

final_message_history = chunk["supervisor"]["messages"]
