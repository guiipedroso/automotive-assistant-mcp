# 🤖 AI Multi-Agent System with Model Context Protocol (MCP)

[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![OpenAI](https://img.shields.io/badge/OpenAI-GPT--4-412991.svg)](https://openai.com/)
[![MCP](https://img.shields.io/badge/MCP-1.7.1-green.svg)](https://modelcontextprotocol.io/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.45.0-FF4B4B.svg)](https://streamlit.io/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-13+-336791.svg)](https://www.postgresql.org/)

---

## 📋 Overview

This project demonstrates the implementation of an **intelligent multi-agent system** using the **Model Context Protocol (MCP)**, a modern architecture for integrating LLMs with external tools and data sources. The system was developed for **Driva Motors**, a fictional automotive dealership, implementing specialized agents for customer service, sales, and maintenance.

The project is divided into two complementary implementations:
- **MCP Base**: Protocol fundamentals with practical examples of tools, resources, and prompts
- **MCP Multi-Agent**: Advanced system with orchestration of multiple specialized agents

---

## 🎯 Business Problem

Driva Motors needed an automated customer service solution capable of:

- ✅ **24/7 customer service** with contextualized responses
- ✅ **Real-time data queries** from corporate database
- ✅ **Specialized service** by demand type (sales vs. maintenance)
- ✅ **Intelligent scheduling** of personalized visits
- ✅ **Scale operations** without proportionally increasing costs

---

## 💡 Solution

An AI system based on **specialized agents** that communicate through the **Model Context Protocol**, enabling:

### Multi-Agent Architecture
```
┌─────────────────────────────────────────────────────────────┐
│                    Client (Streamlit UI)                     │
└──────────────────────────┬──────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────┐
│              Reception Agent (Orchestrator)                  │
│  • Presents the company                                      │
│  • Identifies customer needs                                 │
│  • Performs handoff to specialized agent                     │
└──────────────┬────────────────────────────┬─────────────────┘
               │                            │
       ┌───────▼────────┐          ┌───────▼────────┐
       │  Sales Agent   │          │ Maintenance Agent│
       │ • Queries DB   │          │ • Finds customer │
       │ • Presents     │          │ • Schedules      │
       │   vehicles     │          │   service        │
       │ • Schedules    │          │ • Purchase       │
       │   test drive   │          │   history        │
       └────────┬───────┘          └────────┬─────────┘
                │                           │
                └───────────┬───────────────┘
                            ▼
                ┌───────────────────────┐
                │   MCP Server Tools    │
                │  • get_veiculos       │
                │  • get_concessionarias│
                │  • get_info_cliente   │
                │  • agenda_visita_*    │
                └───────────┬───────────┘
                            ▼
                ┌───────────────────────┐
                │  PostgreSQL Database  │
                │  (Driva Motors)       │
                └───────────────────────┘
```

### Key Components

**1. MCP Servers** - Expose tools and data via standardized protocol
- `server_sql.py`: Generic database access
- `server_test.py`: Example server with tools, resources, and prompts
- `server_agente_atendente.py`: Business domain-specific tools

**2. MCP Clients** - Manage connection and communication with servers
- Support for **stdio** (local processes) and **SSE** (remote servers)
- Automatic tool formatting for OpenAI API
- Connection lifecycle management

**3. LLM Integration** - OpenAI call orchestration
- Conversation history
- Automatic tool call execution
- Parallel tool calls support

**4. Multi-Agent System** - Specialized agents with handoff
- **Reception**: Triage and routing
- **Sales**: Consulting and test drive scheduling
- **Maintenance**: After-sales support and service appointments

---

## 🏗️ Technical Architecture

### Application Layers

#### 1. Presentation Layer (Streamlit)
- Conversational user interface
- Tool calls and responses visualization
- Real-time feedback of active agent

#### 2. Agent Orchestration Layer
- Multiple specialized agents management
- Intelligent handoff between agents
- Shared context across agents

#### 3. MCP Protocol Layer
- Standardized communication with tools
- Automatic capability discovery
- Execution of tools, resources, and prompts

#### 4. Data Layer (PostgreSQL)
- Normalized schema with tables:
  - `veiculos`: Product catalog
  - `concessionarias`: Store network
  - `vendedores`: Sales team
  - `clientes`: Customer base
  - `vendas`: Transaction history

---

## 🔑 Key Features

### ✅ MCP Base (Fundamentals)

**Tools**
- `adiciona(a, b)`: Simple tool example
- `get_schema()`: Returns database structure
- `health_check()`: Verifies connectivity
- `query(sql)`: Executes SQL queries

**Resources**
- `memory://despesas_mensais`: Text file access

**Prompts**
- `formatar_dado_cadastral(cpf)`: Reusable templates

### ✅ MCP Multi-Agent (Production)

**Reception Agent**
- Institutional presentation
- Needs identification
- Intelligent routing

**Sales Agent**
- Available vehicles query
- Personalized recommendations
- Test drive scheduling with specific salesperson

**Maintenance Agent**
- Customer identification by name
- Purchase history
- Service appointment at original dealership

---

## 🛠️ Tech Stack

| Category | Technologies |
|-----------|-------------|
| **Language** | Python 3.9+ |
| **LLM** | OpenAI GPT-4 Turbo |
| **Protocol** | Model Context Protocol (MCP) 1.7.1 |
| **Agent Framework** | OpenAI Agents SDK 0.0.14 |
| **Database** | PostgreSQL 13+ |
| **UI Framework** | Streamlit 1.45.0 |
| **Async Runtime** | asyncio, httpx |
| **Database Driver** | psycopg2 |

---

## 📊 Data Model

### Database Schema

```sql
-- Main Tables
veiculos (id_veiculos, nome, tipo, valor)
concessionarias (id_concessionarias, concessionaria, id_cidades)
vendedores (id_vendedores, nome, id_concessionarias)
clientes (id_clientes, cliente, id_concessionarias)
vendas (id_vendas, id_clientes, id_veiculos, id_vendedores, data_venda, valor_pago)

-- Location Tables
cidades (id_cidades, cidade, id_estados)
estados (id_estados, estado, sigla)
```

### Relationships
- Clientes → Concessionarias (where purchased)
- Vendedores → Concessionarias (where works)
- Vendas → Clientes + Veiculos + Vendedores
- Concessionarias → Cidades → Estados

---

## 🚀 Getting Started

### Prerequisites

```bash
# Python 3.9 or higher
python --version

# Updated pip
pip install --upgrade pip

# uv (to run MCP servers)
pip install uv
```

### Installation

**1. Clone the repository**
```bash
git clone https://github.com/guiipedroso/mcp-multi-agent-system.git
cd mcp-multi-agent-system
```

**2. Create a virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or
venv\Scripts\activate  # Windows
```

**3. Install dependencies**
```bash
# For MCP base project
cd MCP
pip install -r requirements.txt

# For Multi-Agent project
cd ../MCPMultiAgente
pip install -r requirements.txt
```

**4. Configure environment variables**
```bash
# Copy the example file and add your credentials
cp .env.example .env

# Edit the .env file with your actual credentials:
# OPENAI_API_KEY=your_openai_api_key_here
# DB_HOST=your_database_host
# DB_PORT=5432
# DB_NAME=your_database_name
# DB_USER=your_database_user
# DB_PASSWORD=your_database_password
```

### Running the Projects

#### Option 1: MCP Base (Fundamentals)

**Native Client (CLI)**
```bash
cd MCP/cliente_nativo
python client_use.py
```

**Streamlit Interface**
```bash
cd MCP/streamlit
streamlit run chat.py
```

#### Option 2: Multi-Agent System (Production)

```bash
cd MCPMultiAgente/streamlit_agents
streamlit run chat_multi_agent.py
```

Access: `http://localhost:8501`

---

## 🔒 Security

This project follows security best practices:

- ✅ **No hardcoded credentials** - All sensitive data is stored in environment variables
- ✅ **.env files excluded** - Git ignores all .env files to prevent credential leaks
- ✅ **.env.example provided** - Template files show required variables without exposing secrets
- ✅ **Database credentials** - Loaded from environment variables using python-dotenv

**Important:** Never commit your `.env` files to version control. Always use `.env.example` as a template.

---

## 📈 Demo

### Multi-Agent System Interface

**Home Screen**
```
┌─────────────────────────────────────────┐
│       Driva Motors                      │
│       [Company Logo]                    │
├─────────────────────────────────────────┤
│ 🤖 Current Agent: ReceptionAssistant    │
├─────────────────────────────────────────┤
│ User: Hi, I'd like to buy a car         │
│                                         │
│ Assistant: Hello! Welcome to Driva      │
│ Motors! We have several vehicles...     │
│                                         │
│ 🔧 LLM calling tool get_veiculos...     │
│   └─ View arguments                     │
│                                         │
│ 📊 Tool response                        │
│   └─ View response                      │
│                                         │
│ Assistant: We have the following models:│
│ • Executive Sedan - $85,000             │
│ • Premium SUV - $120,000                │
│ ...                                     │
└─────────────────────────────────────────┘
```

### Conversation Flow

**Scenario 1: Vehicle Purchase**
1. Customer expresses interest in buying
2. Reception Agent → Handoff → Sales Agent
3. Sales Agent queries available vehicles
4. Presents options and collects preferences
5. Queries nearby dealerships
6. Lists available salespeople
7. Schedules test drive

**Scenario 2: Maintenance**
1. Customer requests service
2. Reception Agent → Handoff → Maintenance Agent
3. Maintenance Agent requests customer name
4. Retrieves purchase history
5. Identifies original dealership
6. Schedules maintenance visit

---

## 🔍 Implementation Highlights

### 1. MCP Client Pattern

```python
class McpClient:
    async def initialize_with_stdio(self, command: str, args: list):
        """Initialize stdio connection with local MCP server"""
        self.server_params = StdioServerParameters(
            command=command, args=args
        )
        self.client = await self.exit_stack.enter_async_context(
            stdio_client(self.server_params)
        )
        # ...
    
    async def call_tool(self, tool_name: str, args: dict):
        """Execute tool on MCP server"""
        return await self.session.call_tool(tool_name, arguments=args)
```

**Benefits:**
- Protocol complexity abstraction
- Reusability across multiple projects
- Support for stdio and SSE

### 2. Agent Orchestration

```python
agentRecepcao = Agent(
    name="ReceptionAssistant",
    handoffs=[agentVendas, agenteManutencao],
    instructions="You are a reception assistant..."
)

result = await Runner.run(
    starting_agent=current_agent,
    input=history,
    context=history
)
```

**Benefits:**
- Domain specialization
- Automatic handoff between agents
- Shared context

### 3. LLM + MCP Integration

```python
# 1. Get tools from MCP server
tools = client.format_tools_llm(await client.get_tools())

# 2. Call LLM with available tools
response = llm_client.complete_chat(tools)

# 3. Execute tool calls via MCP
if response.choices[0].finish_reason == 'tool_calls':
    for call in response.choices[0].message.tool_calls:
        result = await client.call_tool(
            call.function.name,
            json.loads(call.function.arguments)
        )
```

**Benefits:**
- Separation of concerns
- Dynamic and extensible tools
- Safe and isolated execution

---

## 📁 Project Structure

```
.
├── MCP/                              # MCP base implementation
│   ├── classes/
│   │   ├── llm_client.py            # OpenAI API wrapper
│   │   └── mcp_client.py            # Generic MCP client
│   ├── servers/
│   │   ├── server_sql.py            # Server with DB access
│   │   ├── server_test.py           # Example server
│   │   └── contas_a_pagar.txt       # Example resource
│   ├── cliente_nativo/
│   │   ├── client_example.py        # Basic example
│   │   └── client_use.py            # Complete usage (tools/resources/prompts)
│   ├── cliente_openai/
│   │   └── chat_agent_example.py    # LLM + MCP integration
│   ├── streamlit/
│   │   └── chat.py                  # Interactive web interface
│   └── requirements.txt
│
├── MCPMultiAgente/                   # Multi-agent system
│   ├── servers/
│   │   └── server_agente_atendente.py  # Specialized tools
│   ├── streamlit_agents/
│   │   └── chat_multi_agent.py      # Agent orchestration
│   └── requirements.txt
│
└── slides/                           # Educational material
    ├── 1.Introdução/
    ├── 2.Agentes com MCP/
    ├── 3.Testando Servidores e Clientes/
    └── 5.Aplicações Multi-Agente com MCP/
```

---

## 🎓 Demonstrated Concepts

### Model Context Protocol (MCP)
- ✅ Client-server architecture for LLMs
- ✅ Dynamic capability discovery
- ✅ Safe tool execution
- ✅ Stdio and SSE transport

### Multi-Agent Systems
- ✅ Domain specialization
- ✅ Agent handoff
- ✅ Shared context
- ✅ Orchestration with OpenAI Agents SDK

### LLM Engineering
- ✅ Function calling with OpenAI
- ✅ History management
- ✅ Tool choice strategies
- ✅ Parallel vs sequential tool calls

### Software Engineering
- ✅ Layered architecture
- ✅ Separation of concerns
- ✅ Async/await patterns
- ✅ Context managers for resources

---

## 🔮 Future Enhancements

- [ ] **Authentication & Authorization**: Implement per-user access control
- [ ] **Observability**: Add structured logging and metrics
- [ ] **Automated Testing**: Unit tests and integration tests
- [ ] **Response Caching**: Redis for frequent queries
- [ ] **Deployment**: Containerization with Docker and cloud deployment
- [ ] **New Agents**: Finance, After-sales, Marketing
- [ ] **RAG Integration**: Semantic search in documentation
- [ ] **Voice Interface**: Speech-to-text integration
- [ ] **Analytics Dashboard**: Usage and performance metrics
- [ ] **A/B Testing**: Experimentation with different prompts

---

## 👨‍💻 About the Author

**Guilherme Pedroso** | Data Engineer

Specialist in building scalable data pipelines and AI solutions. This project demonstrates expertise in:

- 🔹 AI systems architecture
- 🔹 LLM integration with corporate data
- 🔹 Conversational agent design
- 🔹 Real-time data engineering
- 🔹 Full-stack development with Python

### 🔗 Connect

[![LinkedIn](https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/gui-pedroso/)
[![GitHub](https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white)](https://github.com/guiipedroso)
[![Portfolio](https://img.shields.io/badge/Portfolio-FF5722?style=for-the-badge&logo=todoist&logoColor=white)](https://github.com/guiipedroso)

### 🏆 Other Projects

- [📊 End-to-End Data Pipeline](https://github.com/guiipedroso/data-pipeline-end-to-end) - Complete pipeline with Airflow, Snowflake, and dbt

---

## 📚 References

- [Model Context Protocol Documentation](https://modelcontextprotocol.io/)
- [OpenAI Agents SDK](https://github.com/openai/openai-agents-python)
- [Streamlit Documentation](https://docs.streamlit.io/)
- [FastMCP Framework](https://github.com/jlowin/fastmcp)

---

## 📄 License

This project is available for educational and portfolio purposes.

---

## 🙏 Acknowledgments

- Anthropic for developing the Model Context Protocol
- OpenAI for the API and Agents SDK
- Python community for amazing tools

---

<div align="center">

**If this project was helpful, consider giving it a ⭐!**

*Built with ❤️ by [Guilherme Pedroso](https://github.com/guiipedroso)*

</div>
