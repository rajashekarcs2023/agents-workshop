import os
from enum import Enum

from uagents import Agent, Context, Model
from uagents.experimental.quota import QuotaProtocol, RateLimit
from uagents_core.models import ErrorMessage

from chat_proto import chat_proto, struct_output_client_proto
from stock_price import get_stock_price, StockPriceRequest, StockPriceResponse

# Create the agent
agent = Agent()

# Set up rate limiting protocol
proto = QuotaProtocol(
    storage_reference=agent.storage,
    name="StockPrice-Protocol",
    version="0.1.0",
    default_rate_limit=RateLimit(window_size_minutes=60, max_requests=30),
)

# Handle direct stock price requests (without natural language processing)
@proto.on_message(
    StockPriceRequest, replies={StockPriceResponse, ErrorMessage}
)
async def handle_request(ctx: Context, sender: str, msg: StockPriceRequest):
    ctx.logger.info(f"Received stock price request for {msg.symbol}")
    try:
        results = await get_stock_price(msg.symbol)
        ctx.logger.info(f"Successfully fetched stock price for {msg.symbol}")
        await ctx.send(sender, StockPriceResponse(results=results))
    except Exception as err:
        ctx.logger.error(f"Error in handle_request: {err}")
        await ctx.send(sender, ErrorMessage(error=str(err)))

# Include the main protocol
agent.include(proto, publish_manifest=True)

# Health check implementation
def agent_is_healthy() -> bool:
    """
    Check if the agent can connect to the Alpha Vantage API
    """
    try:
        import asyncio
        # Try to get a well-known stock price as a health check
        asyncio.run(get_stock_price("IBM"))
        return True
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
        await ctx.send(sender, AgentHealth(agent_name="stock_price_agent", status=status))

# Include all protocols
agent.include(health_protocol, publish_manifest=True)
agent.include(chat_proto, publish_manifest=True)
agent.include(struct_output_client_proto, publish_manifest=True)

if __name__ == "__main__":
    agent.run()