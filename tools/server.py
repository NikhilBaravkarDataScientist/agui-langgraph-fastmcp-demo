from fastmcp import FastMCP
from tools import echo

app = FastMCP()

@app.tool()
def echo(text: str):
    return {"echo": text}

app.run(port=3333)
