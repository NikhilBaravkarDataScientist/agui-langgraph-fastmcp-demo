from fastmcp import FastMCP

app = FastMCP()


@app.tool()
def echo(text: str):
    return {"echo": text}


if __name__ == "__main__":
    # Run HTTP server ONLY when executed directly
    app.run(port=3333)

