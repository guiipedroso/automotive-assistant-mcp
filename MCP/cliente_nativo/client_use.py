import asyncio, sys, os, json

async def main():
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
    from classes.mcp_client import McpClient

    client = McpClient()

    try:
        await client.initialize_with_stdio("mcp", ["run", "servers/server_test.py"])
        # ou, para SSE: 
        #await client.initialize_with_sse("http://localhost:8000/sse")

        print("=== EXECUTANDO TOOL: adiciona(a=42, b=58) ===")
        result = await client.call_tool("adiciona", {"a": 42, "b": 58})
        soma = ''.join([c.text for c in result.content if c.type == "text"])
        print("Resultado da soma:", soma)

        print("\n=== LENDO RESOURCE: memory://despesas_mensais ===")
        result = await client.get_resource("memory://despesas_mensais")
        texto = result.contents[0].text
        print("Despesas mensais:\n", texto)

        print("\n=== INVOCANDO PROMPT: formatar_dado_cadastral(cpf='12345678901') ===")
        result = await client.invoke_prompt("formatar_dado_cadastral", {"cpf": "12345678901"})
        resposta = result.messages[0].content.text
        print("Resposta do prompt:", resposta)

    finally:
        await client.cleanup()


if __name__ == "__main__":
    asyncio.run(main())
