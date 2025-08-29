# Helper function for formatting the stream nicely
from graph import build_graph
graph= build_graph()
def print_stream(stream):

    """Print the stream nicely."""
    
    for s in stream:
        message = s["messages"][-1]
        if isinstance(message, tuple):
            print(message)
        else:
            message.pretty_print()


inputs = {"messages": [("user","tell me about meril life science")]}
print_stream(graph.stream(inputs, stream_mode="values"))
