### Write code for the new module here and import it from agent.py.
from datetime import datetime
from uuid import uuid4
from typing import Any

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

from arithmetic_solver import calculate_arithmetic, ArithmeticRequest

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
            
            prompt = f"""
Extract just the arithmetic expression to calculate from this message: "{item.text}" The user wants to calculate a numeric expression. Extract only the mathematical expression, removing any other text. For example: - From "Calculate 123 * 456" extract "123 * 456" - From "What's 789 + 1000?" extract "789 + 1000"- From "Can you compute 5^3 + 2" extract "5^3 + 2" Only return the actual expression to calculate. """
            
            await ctx.send(
                AI_AGENT_ADDRESS,
                StructuredOutputPrompt(
                    prompt=prompt,
                    output_schema=ArithmeticRequest.schema()
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
                "Sorry, I couldn't identify an arithmetic expression in your message. Please provide a clear numerical calculation to perform."
            ),
        )
        return

    request = ArithmeticRequest.parse_obj(msg.output)
    
    # Extra validation
    if not request.expression or len(request.expression.strip()) == 0:
        await ctx.send(
            session_sender,
            create_text_chat(
                "I couldn't identify an arithmetic expression in your message. Please provide a calculation like '123 * 456' or '789 + 1000'."
            ),
        )
        return

    try:
        calculation_result = await calculate_arithmetic(request.expression)
    except Exception as err:
        ctx.logger.error(f"Error calculating expression: {err}")
        await ctx.send(
            session_sender,
            create_text_chat(
                "Sorry, I encountered an error while calculating your expression. Please ensure it's a valid arithmetic expression."
            ),
        )
        return

    chat_message = create_text_chat(calculation_result)
    await ctx.send(session_sender, chat_message)