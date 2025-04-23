# chat_proto.py
from datetime import datetime
from uuid import uuid4
from typing import Any
from textwrap import dedent

from uagents import Context, Model, Protocol

# Import the necessary components of the chat protocol
from uagents_core.contrib.protocols.chat import (
    ChatAcknowledgement,
    ChatMessage,
    EndSessionContent,
    StartSessionContent,
    TextContent,
    chat_protocol_spec,
)

from business_calculator import perform_business_calculation, BusinessCalculationRequest

# Replace the AI Agent Address with an LLM that supports StructuredOutput
# OpenAI Agent: agent1q0h70caed8ax769shpemapzkyk65uscw4xwk6dc4t3emvp5jdcvqs9xs32y
# Claude.ai Agent: agent1qvk7q2av3e2y5gf5s90nfzkc8a48q3wdqeevwrtgqfdl0k78rspd6f2l4dx
AI_AGENT_ADDRESS = 'agent1q0h70caed8ax769shpemapzkyk65uscw4xwk6dc4t3emvp5jdcvqs9xs32y'

if not AI_AGENT_ADDRESS:
    raise ValueError("AI_AGENT_ADDRESS not set")

def create_text_chat(text: str, end_session: bool = True) -> ChatMessage:
    content = [TextContent(type="text", text=text)]
    if end_session:
        content.append(EndSessionContent(type="end-session"))
    return ChatMessage(
        timestamp=datetime.utcnow(),
        msg_id=uuid4(),
        content=content,
    )

chat_proto = Protocol(spec=chat_protocol_spec)
struct_output_client_proto = Protocol(
    name="StructuredOutputClientProtocol", version="0.1.0"
)

class StructuredOutputPrompt(Model):
    prompt: str
    output_schema: dict[str, Any]

class StructuredOutputResponse(Model):
    output: dict[str, Any]

@chat_proto.on_message(ChatMessage)
async def handle_message(ctx: Context, sender: str, msg: ChatMessage):
    # Check if message has content before trying to access it
    if msg.content and any(isinstance(item, TextContent) for item in msg.content):
        # Get the first TextContent item
        text_content = next((item for item in msg.content if isinstance(item, TextContent)), None)
        if text_content:
            ctx.logger.info(f"Got a message from {sender}: {text_content.text}")
    else:
        ctx.logger.info(f"Got a message from {sender} without text content")
    
    ctx.storage.set(str(ctx.session), sender)
    await ctx.send(
        sender,
        ChatAcknowledgement(timestamp=datetime.utcnow(), acknowledged_msg_id=msg.msg_id),
    )

    for item in msg.content:
        if isinstance(item, StartSessionContent):
            ctx.logger.info(f"Got a start session message from {sender}")
            continue
        elif isinstance(item, TextContent):
            ctx.logger.info(f"Processing text message: {item.text}")
            ctx.storage.set(str(ctx.session), sender)
            
            prompt_text = dedent(f"""
                Extract the business calculation type and parameters from this message:

                "{item.text}"
                
                The user wants to perform a business calculation. Extract:
                1. The calculation_type: One of "discount", "tax", or "inventory"
                2. The parameters required for that calculation type:
                   
                   For discount calculations:
                   - original_price: The price before discount
                   - discount_type: One of "percentage", "fixed", or "bulk"
                   - discount_value: The discount percentage or fixed amount
                   - quantity: Number of items (default: 1)
                   
                   For tax calculations:
                   - amount: The pre-tax amount
                   - tax_rate: The tax percentage
                   - tax_exempt_amount: Amount exempt from tax (default: 0)
                   
                   For inventory optimization:
                   - annual_demand: Units needed per year
                   - order_cost: Cost to place an order
                   - holding_cost_percentage: Annual holding cost as percentage of unit cost
                   - unit_cost: Cost per unit
                   - lead_time_days: Days between order and delivery
                   - working_days: Working days per year (default: 252)
                
                Only include parameters that are mentioned or can be reasonably inferred.
            """)
            
            await ctx.send(
                AI_AGENT_ADDRESS,
                StructuredOutputPrompt(
                    prompt=prompt_text,
                    output_schema=BusinessCalculationRequest.schema()
                ),
            )
        else:
            ctx.logger.info(f"Got unexpected content type: {type(item)}")

@chat_proto.on_message(ChatAcknowledgement)
async def handle_ack(ctx: Context, sender: str, msg: ChatAcknowledgement):
    ctx.logger.info(
        f"Got an acknowledgement from {sender} for {msg.acknowledged_msg_id}"
    )

@struct_output_client_proto.on_message(StructuredOutputResponse)
async def handle_structured_output_response(
    ctx: Context, sender: str, msg: StructuredOutputResponse
):
    session_sender = ctx.storage.get(str(ctx.session))
    if session_sender is None:
        ctx.logger.error(
            "Discarding message because no session sender found in storage"
        )
        return

    if "<UNKNOWN>" in str(msg.output):
        await ctx.send(
            session_sender,
            create_text_chat(
                "Sorry, I couldn't identify the business calculation you want to perform. Please specify if you want to calculate discounts, taxes, or inventory optimization."
            ),
        )
        return

    request = BusinessCalculationRequest.parse_obj(msg.output)
    
    # Extra validation
    if not request.calculation_type or not request.parameters:
        await ctx.send(
            session_sender,
            create_text_chat(
                "I couldn't identify the calculation type or parameters. Please provide more details for the calculation."
            ),
        )
        return

    try:
        result = await perform_business_calculation(
            calculation_type=request.calculation_type,
            parameters=request.parameters
        )
    except Exception as err:
        ctx.logger.error(f"Error performing business calculation: {err}")
        await ctx.send(
            session_sender,
            create_text_chat(
                "Sorry, I encountered an error while performing the calculation. Please check the parameters and try again."
            ),
        )
        return

    chat_message = create_text_chat(result)
    await ctx.send(session_sender, chat_message)