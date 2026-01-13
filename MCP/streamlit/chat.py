
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import streamlit as st
from dotenv import load_dotenv

from classes.llm_client import LLmClient
from classes.mcp_client import McpClient

import asyncio, sys, json

tool = "servers/server_sql.py"

# Corrige bug
if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())


st.markdown("<h1 style='text-align: center;'>Driva Motors</h1>", unsafe_allow_html=True)

left_co, cent_co, last_co = st.columns(3)
with cent_co:
    st.image("arquivos/driva.png", caption="Driva Motors")

if "llmClient" not in st.session_state:
    load_dotenv()  
    st.session_state.llmClient = LLmClient("gpt-4-1106-preview")

def run_task(coro):
    loop = asyncio.new_event_loop()            
    asyncio.set_event_loop(loop)                
    task = loop.create_task(coro)              
    return loop.run_until_complete(asyncio.wait_for(task, timeout=None)) 

if "tools" not in st.session_state:
    with st.spinner("Lendo ferramentas..."): 
        try:
            async def init_mcp():
                client = McpClient() 
                await client.initialize_with_stdio("mcp", ["run", tool])
                await asyncio.sleep(1) 
                tools = client.format_tools_llm(await client.get_tools())
                await client.cleanup() 
                return tools
            
            st.session_state.tools = run_task(init_mcp())
            st.success("Ferramentas lidas com sucesso!")
        except Exception as e:
            st.error(f"Erro ao utilizar MCP Client: {str(e)}")
            st.stop()  


def process_single_tool_call(call):
    try:
        async def do_call():
            client = McpClient()  
            await client.initialize_with_stdio("mcp", ["run", tool])  

            tool_result = await client.call_tool(
                call.function.name,
                json.loads(call.function.arguments)
            )

            await client.cleanup()
            return tool_result

        call_result = run_task(do_call())

        return ''.join(item.text for item in call_result.content if item.type == 'text')
    except Exception as e:
        return f"Error calling tool: {str(e)}"  

def resolve_chat(response):
    llm_client = st.session_state.llmClient
    tools = st.session_state.tools

    if response.choices[0].finish_reason == 'tool_calls':
        tool_reply = response.choices[0].message.content 

        if tool_reply is not None:
            with st.chat_message("assistant"):
                st.markdown(tool_reply)

        calls = response.choices[0].message.tool_calls  

        llm_client.add_assistant_message({
            "content": tool_reply,
            "tool_calls": calls,
            "role": "assistant"
        })

        for call in calls:
            with st.chat_message(name="tool", avatar=":material/build:"):
                st.markdown(f'LLM chamando tool {call.function.name}')
                with st.expander("Visualizar argumentos"):
                    st.code(call.function.arguments)

            with st.spinner(f"Processando chamada para {call.function.name}..."):
                result = process_single_tool_call(call)

            with st.chat_message(name="tool", avatar=":material/data_object:"):
                with st.expander("Visualizar resposta"):
                    st.code(result)

            llm_client.add_tool_message({
                "tool_call_id": call.id,
                "content": result,
                "role": "tool"
            })

        with st.spinner("Gerando resposta final..."):
            next_response = llm_client.complete_chat(tools)

        resolve_chat(next_response)
    
    else:
        assistant_reply = response.choices[0].message.content

        with st.chat_message("assistant"):
            st.markdown(assistant_reply)

        llm_client.add_assistant_message({
            "content": assistant_reply,
            "role": "assistant"
        })

for message in st.session_state.llmClient.history:
    if message["role"] != "tool":
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

        if message["role"] == 'assistant' and "tool_calls" in message and message["tool_calls"]:
            for call in message["tool_calls"]:
                with st.chat_message(name="tool", avatar=":material/build:"):
                    st.markdown(f'LLM chamando tool {call.function.name}')
                    with st.expander("Visualizar resultado"):
                        st.code(call.function.arguments)
    else:
        with st.chat_message(name="tool", avatar=":material/data_object:"):
            with st.expander("Visualizar resposta"):
                st.code(message["content"])

prompt = st.chat_input("Digite sua pergunta:")

if prompt:
    llm_client = st.session_state.llmClient
    llm_client.add_user_message(prompt)
    st.chat_message("user").markdown(prompt)

    with st.container():
        with st.spinner("Processando sua pergunta..."):
            response = llm_client.complete_chat(st.session_state.tools)
            resolve_chat(response)  
