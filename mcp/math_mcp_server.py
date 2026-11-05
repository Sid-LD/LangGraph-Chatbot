
import math
from mcp.server import MCPServer

# Create MCP server
mcp = MCPServer("Math Operations Server")


@mcp.tool()
def add(a: float, b: float) -> float:
    """Add two numbers."""
    return a + b


@mcp.tool()
def subtract(a: float, b: float) -> float:
    """Subtract b from a."""
    return a - b


@mcp.tool()
def multiply(a: float, b: float) -> float:
    """Multiply two numbers."""
    return a * b


@mcp.tool()
def divide(a: float, b: float) -> float:
    """Divide a by b."""
    if b == 0:
        raise ValueError("Division by zero is not allowed.")
    return a / b


@mcp.tool()
def power(base: float, exponent: float) -> float:
    """Calculate base raised to exponent."""
    if abs(exponent) > 1000:
        raise ValueError("Exponent is too large.")

    try:
        result = math.pow(base, exponent)
    except (ValueError, OverflowError):
        raise ValueError("Invalid or excessively large power operation.")

    if not math.isfinite(result):
        raise ValueError("Result is not finite.")

    return result


@mcp.tool()
def square_root(number: float) -> float:
    """Calculate the square root of a number."""
    if number < 0:
        raise ValueError("Cannot calculate square root of a negative number.")

    return math.sqrt(number)


@mcp.tool()
def modulo(a: float, b: float) -> float:
    """Calculate the remainder when a is divided by b."""
    if b == 0:
        raise ValueError("Modulo by zero is not allowed.")

    return a % b


@mcp.tool()
def percentage(number: float, percent: float) -> float:
    """Calculate a percentage of a number."""
    return (number * percent) / 100


if __name__ == "__main__":
    # Use stdio transport for local MCP clients
    mcp.run()
