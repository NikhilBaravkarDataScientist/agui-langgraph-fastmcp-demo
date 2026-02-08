from fastmcp import FastMCP

mcp = FastMCP("tools")

@mcp.tool()
def search_docs(query: str) -> str:
    """Search internal docs"""
    from tools import search_docs as search_func
    return search_func(query)

if __name__ == "__main__":
    mcp.run(transport="sse", host="0.0.0.0", port=9000)
