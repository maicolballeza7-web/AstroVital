# AstroVital

**Astronaut Self-Health Monitoring System** para el reto NASA Space Apps:
**Create Health Monitoring Software for Astronauts on Space Missions**.

AstroVital es un prototipo de autoevaluación para misiones espaciales
prolongadas. Ayuda a registrar indicadores, observar cambios personales y
recibir orientación preventiva mediante el flujo:

**MONITOR → ANALYZE → UNDERSTAND → ACT**

> AstroVital es una herramienta educativa con datos simulados y registros
> introducidos por el usuario. No diagnostica, prescribe tratamientos ni
> autoriza actividades críticas como una EVA.

## Funcionalidades

- Registro parcial de frecuencia cardíaca, presión arterial, temperatura,
  glucosa, sueño, estrés, actividad física y estado de ánimo.
- Validación de datos y detección de indicadores faltantes.
- Persistencia local de evaluaciones del usuario en CSV.
- Separación entre historial del usuario y datos simulados.
- Línea base personal después de al menos tres evaluaciones guardadas.
- Comparación transparente con la media individual.
- Insights sobre desviaciones y tendencias recientes.
- Human Health Map con cinco grupos de indicadores.
- Gráficas independientes para unidades diferentes.
- Mission Readiness experimental, sin valor de autorización médica.

## Estructura

```text
SPACE APP/
├── app.py
├── modules/
│   ├── __init__.py
│   ├── assessment.py
│   ├── baseline.py
│   ├── insights.py
│   └── persistence.py
├── data/
│   └── .gitkeep
├── requirements.txt
├── README.md
└── .gitignore
```

## Ejecutar localmente

Requiere Python 3.11 o superior.

### Windows PowerShell

```powershell
git clone <URL_DEL_REPOSITORIO>
cd "SPACE APP"
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
streamlit run app.py
```

La aplicación estará disponible normalmente en
`http://localhost:8501`.

### Ejecutar sin activar el entorno

```powershell
.\.venv\Scripts\streamlit.exe run app.py
```

## Publicar en Streamlit Community Cloud

1. Crea un repositorio público en GitHub.
2. Sube `app.py`, `modules/`, `data/.gitkeep`, `requirements.txt`,
   `README.md` y `.gitignore`.
3. Entra en [share.streamlit.io](https://share.streamlit.io/).
4. Selecciona el repositorio, la rama y el archivo `app.py`.
5. Pulsa **Deploy**.

No es necesario configurar secretos ni variables de entorno para este MVP.

### Persistencia en la nube

Las evaluaciones se guardan en `data/assessments.csv`. En Streamlit Community
Cloud el almacenamiento local del contenedor no debe considerarse permanente:
un reinicio o redeploy puede eliminar esos registros. Para una versión de
producción se necesita una base de datos o almacenamiento persistente.

## Datos y confiabilidad

- Los datos generados con NumPy aparecen como **simulated**.
- Los datos enviados desde el formulario aparecen como **user**.
- No se presentan datos sintéticos como mediciones reales de astronautas.
- La línea base requiere tres evaluaciones del usuario como mínimo.
- Las reglas actuales son heurísticas de prototipo, no criterios clínicos
  universales.
- El Readiness Score es experimental y no determina aptitud para EVA.

La versión actual no integra datasets externos de NASA Human Research Program,
Human Research Roadmap, OSDR o GeneLab. Esta limitación es intencional: no se
atribuyen resultados científicos a fuentes que todavía no se han verificado o
integrado.

## Comprobación antes de publicar

```powershell
python -m py_compile app.py modules\assessment.py modules\baseline.py modules\insights.py modules\persistence.py
streamlit run app.py
```

Verifica manualmente:

- Que se pueda guardar una evaluación.
- Que aparezca `data/assessments.csv` localmente.
- Que los indicadores faltantes se muestren claramente.
- Que la línea base indique cuándo aún no es confiable.
- Que las gráficas se rendericen sin mezclar unidades.
