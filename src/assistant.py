"""Core AI assistant implementation with streaming support."""
import json
from typing import Optional, Dict, Any
from openai import AsyncOpenAI
from src import config
from src.display import Display
from src.tools import ToolRegistry
from src.tools.implementations import available_tools

class Assistant:
    def __init__(self):
        self.client = AsyncOpenAI(api_key=config.OPENAI_API_KEY)
        self.display = Display()
        self.conversation_history = []
        
        # Initialize and register tools
        self.tool_registry = ToolRegistry()
        for tool_class in available_tools:
            self.tool_registry.register(tool_class)

    def _create_messages(self, user_input: str) -> list[dict]:
        """Create messages list for the API call."""
        return [
            {"role": "system", "content": config.DEFAULT_SYSTEM_MESSAGE},
            *self.conversation_history,
            {"role": "user", "content": user_input}
        ]

    async def get_response(self, user_input: str) -> None:
        """Get streaming response from the AI."""
        try:
            # Add user message to history right away
            self.conversation_history.append({"role": "user", "content": user_input})
            
            self.display.show_user_input(user_input)
            self.display.show_thinking()

            response = await self.client.chat.completions.create(
                model=config.DEFAULT_MODEL,
                messages=self._create_messages(user_input),
                tools=self.tool_registry.get_tools(),
                stream=True
            )

            self.display.clear_thinking()
            self.display.start_streaming()

            full_response = ""
            current_tool_call: Optional[Dict[str, Any]] = None
            current_tool_args = ""

            async for chunk in response:
                delta = chunk.choices[0].delta
                
                # Handle tool calls
                if delta.tool_calls:
                    tool_call = delta.tool_calls[0]
                    if tool_call.function:
                        if current_tool_call is None and tool_call.function.name:
                            current_tool_call = {
                                "name": tool_call.function.name,
                                "arguments": ""
                            }
                        if tool_call.function.arguments:
                            current_tool_args += tool_call.function.arguments
                            
                            # Try to parse JSON to see if it's complete
                            try:
                                json.loads(current_tool_args)
                                # Execute the tool immediately when we have valid JSON
                                try:
                                    args = json.loads(current_tool_args)
                                    result = await self.tool_registry.execute_tool(
                                        current_tool_call["name"],
                                        **args
                                    )
                                    
                                    # Add tool call and result to conversation
                                    self.conversation_history.extend([
                                        {
                                            "role": "assistant",
                                            "content": None,
                                            "tool_calls": [{
                                                "id": "call_" + str(len(self.conversation_history)),
                                                "type": "function",
                                                "function": {
                                                    "name": current_tool_call["name"],
                                                    "arguments": current_tool_args
                                                }
                                            }]
                                        },
                                        {
                                            "role": "tool",
                                            "content": result,
                                            "tool_call_id": "call_" + str(len(self.conversation_history))
                                        }
                                    ])
                                    
                                    self.display.update_streaming(f"The current time in {args['timezone']} is {result}")
                                    current_tool_call = None
                                    current_tool_args = ""
                                    return  # Exit after tool execution
                                    
                                except Exception as e:
                                    self.display.update_streaming(f"\n[Tool Error: {str(e)}]\n")
                                    current_tool_call = None
                                    current_tool_args = ""
                            except json.JSONDecodeError:
                                # Not complete JSON yet, keep collecting
                                pass
                
                # Handle normal content
                elif delta.content:
                    text_chunk = delta.content
                    full_response += text_chunk
                    self.display.update_streaming(text_chunk)

            # Add final response to conversation history if not empty
            if full_response:
                self.conversation_history.append(
                    {"role": "assistant", "content": full_response}
                )

        except Exception as e:
            self.display.show_error(str(e))
        finally:
            self.display.end_streaming()
