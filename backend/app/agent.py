import asyncio
from google import genai
from google.genai import types
import os
import json
import base64
from app.personas import PERSONAS
from app.tools import detect_objection, score_sales_skill

api_key = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

async def connect_to_gemini_live(websocket, persona_id):
    """Manages the bidirectional Live API stream."""
    persona = PERSONAS.get(persona_id, PERSONAS["skeptic"])
    
    config = types.LiveConnectConfig(
        response_modalities=[types.LiveModality.AUDIO],
        system_instruction=types.Content(parts=[types.Part.from_text(text=persona["prompt"])]),
        tools=[detect_objection, score_sales_skill]
    )

    async with client.aio.live.connect(model="gemini-2.0-flash-exp", config=config) as session:
        print(f"Connected to Gemini Live with Persona: {persona['name']}")
        
        async def frontend_to_gemini():
            try:
                while True:
                    message = await websocket.receive()
                    if "bytes" in message:
                        await session.send(input=types.LiveClientRealtimeInput(
                            media_chunks=[types.Blob(data=message["bytes"], mime_type="audio/pcm")]
                        ))
                    elif "text" in message:
                        try:
                            data = json.loads(message["text"])
                            if data.get("realtime_input", {}).get("media_chunks"):
                                chunks = []
                                for chunk in data["realtime_input"]["media_chunks"]:
                                    mime_type = chunk.get("mime_type")
                                    str_data = chunk.get("data")
                                    if mime_type and str_data:
                                        # Remove data:image/jpeg;base64, if present
                                        if "," in str_data:
                                            str_data = str_data.split(",")[1]
                                        raw_bytes = base64.b64decode(str_data)
                                        chunks.append(types.Blob(data=raw_bytes, mime_type=mime_type))
                                if chunks:
                                    await session.send(input=types.LiveClientRealtimeInput(media_chunks=chunks))
                        except Exception as json_err:
                            print(f"JSON parsing error: {json_err}")
            except Exception as e:
                print(f"frontend_to_gemini error: {e}")
                
        async def gemini_to_frontend():
            try:
                async for response in session.receive():
                    server_content = response.server_content
                    if server_content is not None:
                        # Handle audio output
                        model_turn = server_content.model_turn
                        if model_turn is not None:
                            for part in model_turn.parts:
                                if part.inline_data:
                                    await websocket.send_bytes(part.inline_data.data)
                                    
                        # Handle tool calls
                        if server_content.model_turn is None and server_content.turn_complete is False:
                            # Actually, Google GenAI SDK tool calls happen in a specific way.
                            # We might need to handle tool call blocks if they appear in parts.
                            pass
                            
                    # Check for tool calls
                    if response.tool_call is not None:
                        for call in response.tool_call.function_calls:
                            print(f"Tool called: {call.name}")
                            if call.name == "detect_objection":
                                arg_dict = {k: v for k, v in call.args.items()}
                                result = detect_objection(**arg_dict)
                                await websocket.send_json({"type": "tool_call", "name": call.name, "result": result})
                                await session.send(input=types.LiveClientToolResponse(
                                    function_responses=[types.FunctionResponse(
                                        name=call.name,
                                        id=call.id,
                                        response=result
                                    )]
                                ))
                            elif call.name == "score_sales_skill":
                                arg_dict = {k: v for k, v in call.args.items()}
                                result = score_sales_skill(**arg_dict)
                                await websocket.send_json({"type": "scorecard", "data": arg_dict})
                                await session.send(input=types.LiveClientToolResponse(
                                    function_responses=[types.FunctionResponse(
                                        name=call.name,
                                        id=call.id,
                                        response=result
                                    )]
                                ))
            except Exception as e:
                print(f"gemini_to_frontend error: {e}")

        await asyncio.gather(frontend_to_gemini(), gemini_to_frontend())
