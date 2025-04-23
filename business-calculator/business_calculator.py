# business_calculator.py
import sympy as sp
from sympy.parsing.sympy_parser import parse_expr, standard_transformations, implicit_multiplication_application
from uagents import Model, Field
from typing import Optional

class BusinessCalculationRequest(Model):
    """Model for requesting business calculations"""
    calculation_type: str = Field(description="Type of calculation (discount, tax, inventory)")
    parameters: dict = Field(description="Parameters for the calculation")

class BusinessCalculationResponse(Model):
    """Model for business calculation response data"""
    results: str

async def perform_business_calculation(calculation_type: str, parameters: dict) -> str:
    """
    Perform business calculations with high precision
    
    Args:
        calculation_type: Type of calculation to perform (discount, tax, inventory)
        parameters: Dictionary of parameters needed for the calculation
        
    Returns:
        Formatted string with the calculation result
    """
    try:
        if calculation_type == "discount":
            return calculate_discount(parameters)
        elif calculation_type == "tax":
            return calculate_tax(parameters)
        elif calculation_type == "inventory":
            return calculate_inventory_optimization(parameters)
        else:
            return f"Unsupported calculation type: {calculation_type}"
            
    except Exception as e:
        error_msg = str(e)
        return f"Error performing calculation: {error_msg}\n\nPlease check your parameters and try again."

def calculate_discount(params: dict) -> str:
    """Calculate precise discounts with various methods"""
    original_price = sp.Float(params.get("original_price", 0))
    discount_type = params.get("discount_type", "percentage")
    discount_value = sp.Float(params.get("discount_value", 0))
    quantity = sp.Integer(params.get("quantity", 1))
    
    if discount_type == "percentage":
        discount_amount = original_price * (discount_value / 100)
        final_price = original_price - discount_amount
    elif discount_type == "fixed":
        discount_amount = discount_value
        final_price = original_price - discount_amount
    elif discount_type == "bulk":
        # Bulk discounts increase with quantity
        discount_percentage = min(discount_value * (quantity / 10), 50)  # Cap at 50%
        discount_amount = original_price * (discount_percentage / 100)
        final_price = original_price - discount_amount
    else:
        return f"Unsupported discount type: {discount_type}"
    
    total_savings = discount_amount * quantity
    total_cost = final_price * quantity
    
    result = f"📊 DISCOUNT CALCULATION 📊\n\n"
    result += f"Original Price: ${original_price:.2f}\n"
    result += f"Discount Type: {discount_type.title()}\n"
    result += f"Discount Value: {discount_value:.2f}{' %' if discount_type == 'percentage' else ''}\n"
    result += f"Quantity: {quantity}\n\n"
    result += f"Discount Amount (per unit): ${discount_amount:.2f}\n"
    result += f"Final Price (per unit): ${final_price:.2f}\n"
    result += f"Total Savings: ${total_savings:.2f}\n"
    result += f"Total Cost: ${total_cost:.2f}\n"
    
    return result

def calculate_tax(params: dict) -> str:
    """Calculate precise tax implications"""
    pre_tax_amount = sp.Float(params.get("amount", 0))
    tax_rate = sp.Float(params.get("tax_rate", 0))
    tax_exempt_amount = sp.Float(params.get("tax_exempt_amount", 0))
    
    taxable_amount = max(pre_tax_amount - tax_exempt_amount, 0)
    tax_amount = taxable_amount * (tax_rate / 100)
    post_tax_amount = pre_tax_amount + tax_amount
    effective_tax_rate = (tax_amount / pre_tax_amount * 100) if pre_tax_amount > 0 else 0
    
    result = f"💰 TAX CALCULATION 💰\n\n"
    result += f"Pre-tax Amount: ${pre_tax_amount:.2f}\n"
    result += f"Tax Rate: {tax_rate:.2f}%\n"
    result += f"Tax Exempt Amount: ${tax_exempt_amount:.2f}\n\n"
    result += f"Taxable Amount: ${taxable_amount:.2f}\n"
    result += f"Tax Amount: ${tax_amount:.2f}\n"
    result += f"Post-tax Amount: ${post_tax_amount:.2f}\n"
    result += f"Effective Tax Rate: {effective_tax_rate:.2f}%\n"
    
    return result

def calculate_inventory_optimization(params: dict) -> str:
    """Calculate optimal inventory levels using Economic Order Quantity (EOQ) model"""
    annual_demand = sp.Float(params.get("annual_demand", 0))
    order_cost = sp.Float(params.get("order_cost", 0))
    holding_cost_percentage = sp.Float(params.get("holding_cost_percentage", 0))
    unit_cost = sp.Float(params.get("unit_cost", 0))
    lead_time_days = sp.Float(params.get("lead_time_days", 0))
    working_days = sp.Float(params.get("working_days", 252))  # Default: business days in a year
    
    # Calculate holding cost per unit
    holding_cost = unit_cost * (holding_cost_percentage / 100)
    
    # Calculate EOQ (Economic Order Quantity)
    eoq = sp.sqrt(2 * annual_demand * order_cost / holding_cost)
    
    # Calculate optimal number of orders per year
    orders_per_year = annual_demand / eoq
    
    # Calculate order cycle time in days
    cycle_time_days = working_days / orders_per_year
    
    # Calculate average inventory
    average_inventory = eoq / 2
    
    # Calculate total annual inventory cost
    annual_order_cost = orders_per_year * order_cost
    annual_holding_cost = average_inventory * holding_cost
    total_annual_cost = annual_order_cost + annual_holding_cost
    
    # Calculate reorder point
    daily_demand = annual_demand / working_days
    reorder_point = daily_demand * lead_time_days
    
    result = f"📦 INVENTORY OPTIMIZATION 📦\n\n"
    result += f"Annual Demand: {annual_demand:.0f} units\n"
    result += f"Order Cost: ${order_cost:.2f}\n"
    result += f"Holding Cost: {holding_cost_percentage:.2f}% (${holding_cost:.2f} per unit)\n"
    result += f"Unit Cost: ${unit_cost:.2f}\n"
    result += f"Lead Time: {lead_time_days:.0f} days\n\n"
    result += f"Economic Order Quantity (EOQ): {eoq:.0f} units\n"
    result += f"Optimal Orders Per Year: {orders_per_year:.2f}\n"
    result += f"Order Cycle Time: {cycle_time_days:.0f} days\n"
    result += f"Average Inventory: {average_inventory:.0f} units\n"
    result += f"Reorder Point: {reorder_point:.0f} units\n\n"
    result += f"Annual Order Cost: ${annual_order_cost:.2f}\n"
    result += f"Annual Holding Cost: ${annual_holding_cost:.2f}\n"
    result += f"Total Annual Inventory Cost: ${total_annual_cost:.2f}\n"
    
    return result