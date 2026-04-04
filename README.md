# 🧠 Agente Investigador con Google ADK

Sistema backend para la ejecución de agentes inteligentes utilizando Google ADK, diseñado con una arquitectura limpia y escalable que separa claramente la lógica de negocio, la infraestructura y la capa de inteligencia artificial.

---

## 🚀 Descripción

Este proyecto implementa un **agente investigador** capaz de:

- Analizar prompts del usuario  
- Buscar información externa  
- Generar respuestas estructuradas  
- Mantener historial de conversaciones  
- Orquestar múltiples agentes (investigador + editor)  

El sistema está diseñado para ser:

- ✅ Escalable  
- ✅ Mantenible  
- ✅ Controlado (el LLM no toma decisiones críticas del sistema)  

---

## 🏗️ Arquitectura

El proyecto sigue una **arquitectura por capas con enfoque Clean Architecture**, separando responsabilidades:

---
## Flujo

agents (ADK) → api → application → domain → infrastructure

agents (ADK)

---


### 📌 Capas principales

#### 🌐 API (`app/api`)
Punto de entrada HTTP (FastAPI).

- Recibe prompts del usuario  
- Llama a los casos de uso  
- Devuelve respuestas  

---

#### 🧠 Domain (`app/domain`)
Núcleo del sistema.

- Entidades (`entities.py`)  
- Modelos y validaciones (`models.py`)  
- Interfaces de repositorio (`repository_base.py`)  

> ❗ No depende de ninguna tecnología externa.

---

#### 🚀 Application (`app/application`)
Contiene la lógica del sistema.

- Casos de uso (`run_investigation.py`)  
- Manejo de historial (`history_manager.py`)  
- Ejecución de agentes (`agent_runner.py`)  

> 💡 Aquí vive el “cerebro” del sistema.

---

#### 🔌 Infrastructure (`app/infrastructure`)
Implementaciones externas.

- Firestore (persistencia)  
- SQL (opcional)  
- Logging y tracing  

---

#### 🤖 Agents (`app/services/agents`)
Capa de inteligencia (Google ADK).

- Prompts versionados  
- Tools que el agente puede usar  
- Definición de agentes  
- Configuración de equipos multi-agente  

---

## 🔄 Flujo de ejecución

1. Usuario envía un prompt → API  
2. Se ejecuta `run_investigation`  
3. Se carga el historial  
4. Se ejecutan los agentes (investigator → editor)  
5. Se guarda el resultado  
6. Se devuelve la respuesta  

---

## 🛠️ Tools del agente

Los agentes pueden ejecutar herramientas como:

- 🔍 `search_web` → búsqueda de información  
- 📄 `export_pdf` → generación de reportes  
- 🧹 `format_text` → limpieza de texto  

> 💡 Cada tool representa una acción específica que el LLM puede ejecutar.

---

## 🧾 Prompts

Los prompts están desacoplados del código:
 
app/services/agents/prompts/

Esto permite:

- Versionar comportamiento  
- Ajustar respuestas sin cambiar lógica  
- Iterar rápidamente  

---

## 📊 Observabilidad

El sistema incluye:

- Logging estructurado  
- Trazabilidad de ejecución  
- Debug de decisiones del agente  

---

## ⚙️ Instalación

```bash
git clone https://github.com/MiguelAngelNva/agente-investigador
cd agente-investigador
pip install -r requirements.txt