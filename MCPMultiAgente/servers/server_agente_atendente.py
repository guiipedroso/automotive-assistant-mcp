from mcp.server.fastmcp import FastMCP
import psycopg2, json
import os
from dotenv import load_dotenv

load_dotenv()

mcp = FastMCP("FerramentasAssistenteDrivaMotors", dependencies=["psycopg2"])

CONN_STR = {
    "host": os.getenv("DB_HOST"),
    "port": os.getenv("DB_PORT", "5432"),
    "dbname": os.getenv("DB_NAME"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
}

def get_connection():
    return psycopg2.connect(**CONN_STR)

@mcp.tool()
def get_veiculos_disponiveis():
    """Retorna os veículos/carros disponíveis para a compra"""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        cursor.execute("select nome, tipo, valor from veiculos v;")
        
        rows = cursor.fetchall()
        result = [dict(zip([desc[0] for desc in cursor.description], row)) for row in rows]
        cursor.close()
        conn.close()
        return json.dumps(result, indent=4, sort_keys=True, default=str)
    except Exception as e:
        return {"error": str(e)}
    
@mcp.tool()
def get_concessionarias():
    """Retorna as concessionárias e suas informações de localização"""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            select c.id_concessionarias, c.concessionaria, c2.cidade, e.estado, e.sigla 
            from concessionarias c
            join cidades c2 on c2.id_cidades = c.id_cidades
            join estados e on c2.id_estados = e.id_estados;
        """)
        
        rows = cursor.fetchall()
        result = [dict(zip([desc[0] for desc in cursor.description], row)) for row in rows]
        cursor.close()
        conn.close()
        return json.dumps(result, indent=4, sort_keys=True, default=str)
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def get_vendedores_por_concessionaria(id_concessionarias: int):
    """Retorna os vendedores por id de concessionária"""
    try:
        with get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute("""
                    SELECT v.id_vendedores, v.nome 
                    FROM vendedores v 
                    WHERE v.id_concessionarias = %s;
                """, (id_concessionarias,))
                
                rows = cursor.fetchall()
                result = [dict(zip([desc[0] for desc in cursor.description], row)) for row in rows]
        return json.dumps(result, indent=4, sort_keys=True, default=str)
    except Exception as e:
        return {"error": str(e)}
    
@mcp.tool()
def get_info_cliente(nome: str):
    """Retorna as informações do cliente pelo nome. Retorna junto com carros/veículos que foram comprados e onde."""
    try:
        with get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute("""
                    select c.id_clientes, c.cliente, c2.concessionaria, c3.cidade, e.estado, v.data_venda, v.valor_pago, v2.nome as carro from clientes c
                    join concessionarias c2 on c.id_concessionarias = c2.id_concessionarias
                    join cidades c3 on c3.id_cidades = c2.id_cidades
                    join estados e on e.id_estados  = c3.id_estados
                    join vendas v on v.id_clientes = c.id_clientes
                    join veiculos v2 on v.id_veiculos = v2.id_veiculos
                    where c.cliente  = %s;
                """, (nome,))
                
                rows = cursor.fetchall()
                result = [dict(zip([desc[0] for desc in cursor.description], row)) for row in rows]
        return json.dumps(result, indent=4, sort_keys=True, default=str)
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def agenda_visita_para_compra(id_concessionaria: int, id_vendedor: int, data_hora: str):
    """Agenda uma visita na concessionária e vendedor no horário estipulado"""
    try:
        # TODO: fazemos de conta
        return {"message": "Visita agendada com sucesso!"}
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def agenda_visita_para_assistencia(id_cliente: int, id_concessionaria: int, nome_carro: str, detalhes: str, data_hora: str):
    """Agenda uma visita na concessionária para manutenções ou revisões, apenas para clientes que já possuem carro/veículo"""
    try:
        # TODO: fazemos de conta
        return {"message": "Visita de manutenção/revisão agendada com sucesso!"}
    except Exception as e:
        return {"error": str(e)}
    
