🚀 NASA Space Apps Challenge 2026 — Roadmap del Proyecto
Reto elegido: Create Health Monitoring Software for Astronauts on Space Missions
Participante: Individual (equipo de 1)
Evento: Virtual Universal
Hackathon: 14–15 de noviembre de 2026
Entrega: Antes del 15 de noviembre, 11:59 PM (hora local del evento)

🎯 1. Concepto del proyecto
Nombre tentativo: AstroVital — Panel de Automonitoreo de Salud para Astronautas

Problema:
En misiones de larga duración, los astronautas deben detectar por sí mismos cambios en su salud (radiación, aislamiento, gravedad alterada, pérdida ósea, eventos cardiovasculares, salud conductual). No siempre tienen comunicación inmediata con Tierra ni personal médico al lado.

Solución:
Una aplicación web que:

Recolecta indicadores de salud (reales o simulados)

Los evalúa con reglas claras

Muestra un estado general tipo semáforo

Sugiere acciones concretas al astronauta

🧩 2. Alcance mínimo viable (MVP) — lo que SÍ o SÍ va
Esto es lo que debe estar listo para que el proyecto sea válido y funcional.

2.1 Indicadores monitoreados (5 mínimo)
Indicador	Fuente	Frecuencia
Frecuencia cardíaca (HR)	Simulado / dataset	Cada hora
Horas de sueño	Simulado	Diario
Nivel de estrés (1–10)	Entrada manual	Diario
Actividad física (min)	Simulado	Diario
Estado de ánimo	Entrada manual	Diario
2.2 Funcionalidades mínimas
□ Dashboard con los 5 indicadores en tarjetas
□ Semáforo general (verde / amarillo / rojo)
□ Alertas cuando un indicador sale de rango
□ Recomendaciones básicas según la alerta
□ Vista histórica simple (últimos 7 días)
□ Datos simulados precargados (para que funcione sin hardware)
2.3 Stack técnico
Lenguaje: Python 3.11+

Framework web: Streamlit

Datos: CSV o JSON simulados

Gráficas: Plotly

Control de versiones: Git + GitHub

2.4 Entregables obligatorios del hackathon
□ Proyecto subido a la plataforma
□ Repositorio en GitHub con README
□ Video de presentación (30–60 seg)
□ Descripción del proyecto (problema, solución, tecnología, impacto)
⏱️ 3. Tiempo estimado
Fase previa (antes del 14 de noviembre)
Tarea	Tiempo estimado
Definir indicadores y reglas	1 h
Crear dataset simulado realista	1.5 h
Armar estructura del proyecto	0.5 h
Dashboard básico con Streamlit	3 h
Lógica de semáforo y alertas	2 h
Gráficas históricas	1.5 h
README y documentación	1 h
Total previo	~10.5 h
Durante el hackathon (14–15 nov)
Tarea	Tiempo estimado
Pulir UI/UX	2 h
Corregir bugs	1.5 h
Grabar video	1 h
Subir proyecto y formularios	1 h
Total hackathon	~5.5 h
Total general: ~16 horas de trabajo efectivo.

🌟 4. Extras para destacar (si da tiempo)
Estos son los diferenciadores que pueden hacer que el proyecto resalte entre los demás.

4.1 Nivel 1 — Fáciles y de alto impacto
□ Modo "simulación de misión" (acelerar el tiempo para ver cómo evoluciona la salud)
□ Exportar reporte PDF con resumen del estado del astronauta
□ Multi-idioma (español / inglés)
□ Alertas por voz (text-to-speech)
4.2 Nivel 2 — Intermedios
□ Integración con datos abiertos reales de OSDR (NASA Open Science Data Repository)
□ Módulo de salud conductual (aislamiento, estado emocional, interacción)
□ Gráficas comparativas contra promedios de referencia
□ Sistema de "recomendaciones inteligentes" basado en reglas más finas
4.3 Nivel 3 — Avanzados (solo si sobra mucho tiempo)
□ Modelo simple de ML para detectar anomalías
□ Modo offline con almacenamiento local
□ Interfaz tipo "consola espacial" (estética retro-futurista)
□ Integración con wearables simulados (API mock)
📁 5. Estructura del proyecto
text
astrovital/
├── app.py                  # Entrada principal Streamlit
├── data/
│   ├── health_data.csv     # Dataset simulado
│   └── rules.json          # Reglas de alerta
├── modules/
│   ├── indicators.py       # Lógica de indicadores
│   ├── alerts.py           # Sistema de alertas
│   └── recommendations.py  # Recomendaciones
├── assets/
│   └── logo.png
├── requirements.txt
└── README.md
📅 6. Plan de trabajo sugerido
Semana 1 (antes del hackathon)
Definir indicadores y reglas

Crear dataset simulado

Armar estructura del repo

Semana 2
Dashboard funcional

Lógica de semáforo y alertas

Semana 3
Gráficas históricas

README y documentación

Pruebas

14–15 de noviembre
Pulir, grabar video, subir

✅ 7. Checklist final antes de entregar
□ La app corre sin errores
□ Los datos simulados se cargan correctamente
□ El semáforo y las alertas funcionan
□ El README explica el proyecto
□ El video está grabado y subido
□ El proyecto está subido a la plataforma
□ Formulario de participante completado
