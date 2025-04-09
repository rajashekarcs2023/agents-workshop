import sympy as sp
from sympy.parsing.sympy_parser import parse_expr, standard_transformations, implicit_multiplication_application
from uagents import Model, Field
import re

class ArithmeticRequest(Model):
    """Model for requesting arithmetic calculation"""
    expression: str = Field(description="The arithmetic expression to calculate")

class ArithmeticResponse(Model):
    """Model for arithmetic calculation response"""
    results: str

async def calculate_arithmetic(expression: str) -> str:
    """
    Calculate the result of an arithmetic expression with high precision
    
    Args:
        expression: The arithmetic expression to calculate
        
    Returns:
        Formatted string with the calculation result
    """
    try:
        # Clean the expression
        expression = expression.strip()
        
        if not expression:
            return "Error: Please provide a valid arithmetic expression."
        
        # Replace common symbols
        expression = expression.replace("^", "**")  # Convert caret to Python exponentiation
        expression = expression.replace("×", "*")   # Convert multiplication sign
        expression = expression.replace("÷", "/")   # Convert division sign
        
        # Setup parser with transformations for more intuitive parsing
        transformations = standard_transformations + (implicit_multiplication_application,)
        
        # Parse and evaluate the expression
        parsed_expr = parse_expr(expression, transformations=transformations)
        result = sp.N(parsed_expr)
        
        # Format the result
        formatted_result = f"🔢 ARITHMETIC CALCULATION 🔢\n\n"
        formatted_result += f"Expression: {expression}\n\n"
        formatted_result += f"Result: {result}\n"
        
        # Add integer check for whole numbers
        if result == int(result):
            formatted_result += f"\nInteger result: {int(result)}"
        
        # Add binary/hex for smaller integers
        if isinstance(result, sp.Number) and result.is_Integer and abs(result) < 10**10:
            int_value = int(result)
            if abs(int_value) < 2**32:  # Only show for reasonably sized integers
                formatted_result += f"\n\nAlternative formats:"
                formatted_result += f"\nBinary: {bin(int_value)}"
                formatted_result += f"\nHexadecimal: {hex(int_value)}"
        
        return formatted_result
        
    except Exception as e:
        error_msg = str(e)
        return f"Error calculating expression: {error_msg}\n\nPlease check your input and try again with a valid arithmetic expression."