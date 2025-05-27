from langchain_core.messages import convert_to_messages

def pretty_print_message(message, indent=False):
    pretty_message = message.pretty_repr(html=True)
    if not indent:
        print(pretty_message)
        return
    print("\n".join("\t" + line for line in pretty_message.split("\n")))

def pretty_print_messages(update, last_message=False):
    is_subgraph = False
    if isinstance(update, tuple):
        ns, update = update
        if len(ns) == 0:
            return
        print(f"Update from subgraph {ns[-1].split(':')[0]}:\n")
        is_subgraph = True

    for node_name, node_update in update.items():
        print(f"\tUpdate from node {node_name}:\n" if is_subgraph else f"Update from node {node_name}:\n")
        messages = convert_to_messages(node_update["messages"])
        if last_message:
            messages = messages[-1:]
        for m in messages:
            pretty_print_message(m, indent=is_subgraph)
        print()
