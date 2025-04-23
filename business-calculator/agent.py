# agent.py
import os
from enum import Enum

from uagents import Agent, Context, Model
from uagents.experimental.quota import QuotaProtocol, RateLimit
from uagents_core.models import ErrorMessage

from chat_proto import chat_proto, struct_output_client_proto
from business_calculator import perform_business_calculation, BusinessCalculationRequest, BusinessCalculationResponse

# Create the agent
agent = Agent(
    name="business_calculator",
    port=8003,
    mailbox=True        
)

# Print the agent's address for reference
print(f"Your agent's address is: {agent.address}")

# Set up rate limiting protocol
proto = QuotaProtocol(
    storage_reference=agent.storage,
    name="BusinessCalculator-Protocol",
    version="0.1.0",
    default_rate_limit=RateLimit(window_size_minutes=60, max_requests=30),
)

# Handle direct business calculation requests (without natural language processing)
@proto.on_message(
    BusinessCalculationRequest, replies={BusinessCalculationResponse, ErrorMessage}
)
async def handle_request(ctx: Context, sender: str, msg: BusinessCalculationRequest):
    ctx.logger.info(f"Received business calculation request of type: {msg.calculation_type}")
    try:
        results = await perform_business_calculation(
            calculation_type=msg.calculation_type,
            parameters=msg.parameters
        )
        ctx.logger.info(f"Successfully performed business calculation")
        await ctx.send(sender, BusinessCalculationResponse(results=results))
    except Exception as err:
        ctx.logger.error(f"Error in handle_request: {err}")
        await ctx.send(sender, ErrorMessage(error=str(err)))

# Include the main protocol
agent.include(proto, publish_manifest=True)

# Health check implementation
def agent_is_healthy() -> bool:
    """
    Check if the agent's calculation capabilities are working
    """
    try:
        import asyncio
        # Try a simple discount calculation
        params = {
            "original_price": 100,
            "discount_type": "percentage",
            "discount_value": 20,
            "quantity": 1
        }
        result = asyncio.run(perform_business_calculation("discount", params))
        return "DISCOUNT CALCULATION" in result
    except Exception as e:
        print(f"Health check failed: {e}")
        return False

class HealthCheck(Model):
    pass

class HealthStatus(str, Enum):
    HEALTHY = "healthy"
    UNHEALTHY = "unhealthy"

class AgentHealth(Model):
    agent_name: str
    status: HealthStatus

# Health monitoring protocol
health_protocol = QuotaProtocol(
    storage_reference=agent.storage, name="HealthProtocol", version="0.1.0"
)

@health_protocol.on_message(HealthCheck, replies={AgentHealth})
async def handle_health_check(ctx: Context, sender: str, msg: HealthCheck):
    status = HealthStatus.UNHEALTHY
    try:
        if agent_is_healthy():
            status = HealthStatus.HEALTHY
    except Exception as err:
        ctx.logger.error(f"Health check error: {err}")
    finally:
        await ctx.send(sender, AgentHealth(agent_name="business_calculator_agent", status=status))

# Include all protocols
agent.include(health_protocol, publish_manifest=True)
agent.include(chat_proto, publish_manifest=True)
agent.include(struct_output_client_proto, publish_manifest=True)

if __name__ == "__main__":
    agent.run()