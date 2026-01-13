from agents import Agent, ModelSettings, Runner
from agents.mcp import MCPServerStdio 
import streamlit as st
from dotenv import load_dotenv
import asyncio, json, sys

if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())

st.markdown("<h1 style='text-align: center;'>Driva Motors</h1>", unsafe_allow_html=True)

_, cent_co, _ = st.columns(3)
with cent_co:
    st.image("arquivos/driva.png", caption="Driva Motors")

if "history" not in st.session_state:
    load_dotenv()  
    st.session_state.history = []

for message in st.session_state.history:
    type = message.get("role", None) or message.get("type", None)

    match type:
        case 'user': 
            with st.chat_message(type):
                st.markdown(message["content"])
        case 'assistant': 
            with st.chat_message(type):
                st.markdown(message["content"][0]["text"])
        case 'function_call': 
            if "transfer_to" not in message["name"]: 
                with st.chat_message(name="tool", avatar=":material/build:"):
                        st.markdown(f'LLM chamando tool {message["name"]}')
                        with st.expander("Visualizar argumentos"):
                            st.code(message["arguments"])
        case 'function_call_output':
            try:
                obj = json.loads(message['output'])
                with st.chat_message(name="tool", avatar=":material/data_object:"):
                    with st.expander("Visualizar resposta"):
                        st.code(obj["text"])
            except:
                continue
        
if "agentRecepcao" not in st.session_state: 
        agenteManutencao = Agent( 
            name="MaintenanceAssistant", 
            model="gpt-4-1106-preview",
            handoff_description="Maintenance/service assistant for customers who already own a vehicle.",
            instructions="You are an assistant at Driva Motors who should help the customer schedule a maintenance or service visit." \
                "Ask for the full name to identify the customer and then use the tools to discover the vehicles they own (get_info_cliente). " \
                "Based on that, collect information about what they need, schedule an appointment at the dealership where they purchased the vehicle (with agenda_visita_para_assistencia)." \
                "It's not necessary to choose a salesperson, just schedule the visit at the dealership where they bought the vehicle. ",
            model_settings=ModelSettings(tool_choice="auto", temperature=0, parallel_tool_calls=False), 
        )

        agentVendas = Agent(  
            name="SalesAssistant", 
            model="gpt-4-1106-preview",
            handoff_description="Assistant for sales handling, vehicle information and visit/test drive scheduling.",
            instructions="You are an assistant at Driva Motors who should help and convince the customer to buy a vehicle." \
                "First of all, use the get_veiculos_disponiveis tool to know the available options and present them. " \
                "You can ask questions to understand what the customer needs and offer the best vehicle options based on the tool you called. " \
                "When the customer decides, schedule a visit at the nearest dealership, to discover dealerships use get_concessionarias " \
                "and to discover salespeople at that dealership use get_vendedores_por_concessionaria. " \
                "Then, schedule the visit with the agenda_visita_para_compra tool, where you will choose the salesperson and the nearest dealership to the customer.",
            model_settings=ModelSettings(tool_choice="auto", temperature=0, parallel_tool_calls=False), 
        )

        agentRecepcao = Agent( 
            name="ReceptionAssistant", 
            model="gpt-4-1106-preview",
            handoffs=[agentVendas, agenteManutencao], 
            instructions="You are a reception assistant at Driva Motors, a national vehicle company in Brazil." \
                "You are responsible for reception and should only present the company and offer available options. " \
                "Present Driva Motors as a vehicle company and proudly Brazilian." \
                "Show the website https://www.drivamotors.com.br/ to learn more about the company." \
                "Offer to see the cars and schedule a visit with a salesperson with the possibility of a test drive." \
                "Or in case they want maintenance or service, they can schedule a visit to the dealership.",
            model_settings=ModelSettings(tool_choice="auto", temperature=0, parallel_tool_calls=False), 
        )

        st.session_state.agentRecepcao = agentRecepcao
        st.session_state.agentVendas = agentVendas
        st.session_state.agenteManutencao = agenteManutencao
        st.session_state.current_agent = agentRecepcao 

async def resolve_chat(): 
    async with MCPServerStdio(params={"command": "mcp", "args": ["run", "servers/server_agente_atendente.py"]}) as server:
        st.session_state.agentVendas.mcp_servers = [server] 
        st.session_state.agenteManutencao.mcp_servers = [server] 

        result = await Runner.run(
            starting_agent=st.session_state.current_agent, 
            input=st.session_state.history, 
            context=st.session_state.history
        )
       
        st.session_state.current_agent = result.last_agent
        st.session_state.history = result.to_input_list()
      
prompt = st.chat_input("Digite sua pergunta:")

if prompt:
    st.session_state.history.append({
        "role": "user",
        "content": prompt
    })

    with st.chat_message("user"):
        st.markdown(prompt)

    with st.spinner("Pensando..."):
        asyncio.run(resolve_chat())
        st.rerun()

if "current_agent" in st.session_state: 
    st.toast(f"Agente atual: { st.session_state.current_agent.name }")
