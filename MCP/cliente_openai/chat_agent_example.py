import asyncio
from agents import Agent, ModelSettings, Runner, TResponseInputItem
from agents.mcp import MCPServerStdio
from dotenv import load_dotenv

async def chat_agent():
    load_dotenv()

    async with MCPServerStdio(params={"command": "mcp", "args": ["run", "servers/server_sql.py"]}) as server:
        
        agent = Agent(
            name="Assistant", 
            model="gpt-4-1106-preview",  
            instructions="Você é um assistente de banco de dados. Utilize as ferramentas necessárias para acessar o schema ou acessar dados do banco.",
            mcp_servers=[server], 
            model_settings=ModelSettings(tool_choice="auto", temperature=0) 
        )

        print("Digite sair, exit ou quit para encerrar a conversa.")

        history: list[TResponseInputItem] = []

        while True:
            message = input("Você: ")

            if message.lower() in ["sair", "exit", "quit"]:
                print("Encerrando a conversa.")
                break

            history.append({
                "role": "user",
                "content": message
            })

            result = await Runner.run(starting_agent=agent, input=history)

            history = result.to_input_list()

            print(f"Assistente: {result.final_output}")


if __name__ == "__main__":
    asyncio.run(chat_agent())