# MasterClass: GitHub Actions para Data Science y Machine Learning

<p align="center">
  <img src="https://www.soyhenry.com/_next/static/media/HenryLogo.bb57fd6f.svg" alt="Henry Logo" width="280"/>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/python-3.10+-blue?logo=python&logoColor=white" alt="Python"/>
  <img src="https://img.shields.io/badge/uv-package_manager-blueviolet?logo=astral&logoColor=white" alt="uv"/>
  <img src="https://img.shields.io/badge/CI-GitHub_Actions-2088FF?logo=githubactions&logoColor=white" alt="GitHub Actions"/>
  <img src="https://img.shields.io/badge/ML-scikit--learn-F7931E?logo=scikit-learn&logoColor=white" alt="scikit-learn"/>
</p>

---

## Que vas a aprender

Este repositorio es una clase practica que te lleva **de cero a un pipeline de Machine Learning automatizado** con GitHub Actions. Esta organizado en 3 niveles progresivos:

| Nivel | Workflow | Que aprendes |
|-------|----------|--------------|
| 1 | Mi Primer Workflow | Que es un Trigger, un Job, un Step y un Runner |
| 2 | Jobs con Dependencias | Como encadenar Jobs con `needs` |
| 3 | Pipeline Completo de ML | Lint + Test + Train + Deploy en un DAG real |

> [!NOTE]
> **Requisitos previos:** Conocimientos basicos de Python y Git. No se necesita experiencia previa con CI/CD.

---

## Tabla de contenidos

1. [Conceptos clave](#conceptos-clave)
2. [Estructura del repositorio](#estructura-del-repositorio)
3. [Nivel 1 -- Mi Primer Workflow](#nivel-1----mi-primer-workflow)
4. [Nivel 2 -- Jobs con Dependencias](#nivel-2----jobs-con-dependencias)
5. [Nivel 3 -- Pipeline Completo de ML](#nivel-3----pipeline-completo-de-ml)
6. [Guia paso a paso](#guia-paso-a-paso)
7. [Ejecucion local](#ejecucion-local)
8. [Glosario](#glosario)

---

## Conceptos clave

### Que es CI/CD?

| Sigla | Significado | Que hace |
|-------|-------------|----------|
| **CI** | Integracion Continua | Cada vez que subes codigo, se ejecutan pruebas automaticas para verificar que nada se rompio. |
| **CD** | Despliegue Continuo | Una vez validado, el codigo (o modelo) se despliega automaticamente a produccion. |

### Anatomia de un Workflow

```yaml
name: Nombre del flujo            # Identificador legible

on:                                # CUANDO se ejecuta (Trigger)
  push:
    branches: [main]

jobs:                              # QUE tareas se ejecutan
  mi-tarea:
    runs-on: ubuntu-latest         # DONDE corre (Runner)
    steps:                         # Pasos secuenciales
      - uses: actions/checkout@v4  # Accion preconstruida
      - run: echo "Hola"          # Comando de shell
```

> [!TIP]
> **Runner** = maquina virtual temporal que GitHub te presta gratis para ejecutar los pasos. Se crea al iniciar y se destruye al terminar.

---

## Estructura del repositorio

```text
MasterClass_GithubActions/
|-- .github/
|   |-- workflows/
|       |-- 01-basic-workflow.yml          # Nivel 1: Hola Mundo
|       |-- 02-dependencies-workflow.yml   # Nivel 2: Jobs dependientes
|       |-- 03-ml-pipeline.yml             # Nivel 3: Pipeline ML completo
|-- src/
|   |-- __init__.py
|   |-- hello.py                           # Script introductorio
|   |-- train_iris.py                      # Pipeline de entrenamiento (Iris)
|-- tests/
|   |-- test_hello.py                      # Tests del modulo hello
|   |-- test_train.py                      # Tests del pipeline ML
|-- pyproject.toml                         # Dependencias y config del proyecto
|-- uv.lock                               # Lockfile para builds reproducibles
|-- .gitignore
|-- README.md
```

### Stack tecnologico

| Herramienta | Rol |
|-------------|-----|
| [uv](https://docs.astral.sh/uv/) | Gestor de paquetes y entornos (reemplazo moderno de pip+venv) |
| [scikit-learn](https://scikit-learn.org/) | Entrenamiento del modelo de clasificacion |
| [pandas](https://pandas.pydata.org/) | Manipulacion de datos tabulares |
| [colorlog](https://github.com/borntyping/python-colorlog) | Logging con colores tipo semaforo en consola |
| [flake8](https://flake8.pycqa.org/) | Linter para verificar calidad de codigo |
| [pytest](https://pytest.org/) | Framework de pruebas unitarias |

---

## Nivel 1 -- Mi Primer Workflow

**Archivo:** `.github/workflows/01-basic-workflow.yml`

Este es el workflow mas sencillo posible. No necesita Python, ni dependencias, ni codigo. Solo ejecuta comandos de shell para que entiendas la mecanica basica.

### Que hace?

```text
[push a main] --> [ echo "Hola Mundo" + info del Runner ]
```

### Que aprendes?

- **`on`**: Define *cuando* se ejecuta el workflow (al hacer push, o manualmente).
- **`jobs`**: Contiene las tareas. Aqui solo hay una: `hola-mundo`.
- **`runs-on`**: En que tipo de maquina corre (Ubuntu gratuito de GitHub).
- **`steps`**: Los pasos secuenciales. Cada `run:` ejecuta un comando de terminal.
- **`workflow_dispatch`**: Permite ejecutar el workflow a mano desde la interfaz.

### Fragmento clave

```yaml
steps:
  - name: Saludar desde la nube
    run: echo "Hola Mundo desde GitHub Actions!"
```

> [!TIP]
> Empieza ejecutando este workflow manualmente desde la pestana Actions para ver que pasa.

---

## Nivel 2 -- Jobs con Dependencias

**Archivo:** `.github/workflows/02-dependencies-workflow.yml`

Aqui introducimos el concepto mas importante para construir pipelines: **las dependencias entre Jobs** usando la directiva `needs`.

### Que hace?

```text
[ejecutar-codigo] --> [confirmar-exito]
```

Dos Jobs:
1. **ejecutar-codigo**: Descarga el repo, instala dependencias con `uv`, y ejecuta `hello.py`.
2. **confirmar-exito**: Solo se ejecuta **si el Job anterior termino bien**. Si falla, este jamas corre.

### Que aprendes?

- **`uses: actions/checkout@v4`**: Accion preconstruida que "clona" tu repo dentro del Runner.
- **`uses: astral-sh/setup-uv@v5`**: Instala `uv` en el Runner.
- **`uv sync`**: Crea el entorno virtual e instala todas las dependencias.
- **`needs: [ejecutar-codigo]`**: La directiva que crea la relacion de dependencia.

### Fragmento clave

```yaml
confirmar-exito:
  runs-on: ubuntu-latest
  needs: [ejecutar-codigo]    # <-- Esto crea la dependencia
```

> [!IMPORTANT]
> Sin `needs`, los Jobs corren **en paralelo**. Con `needs`, corren **en secuencia** y el dependiente se cancela si el anterior falla.

---

## Nivel 3 -- Pipeline Completo de ML

**Archivo:** `.github/workflows/03-ml-pipeline.yml`

El pipeline completo con 4 eslabones encadenados formando un grafo dirigido (DAG):

```text
 [Lint]---+
          +--> [Train] --> [Deploy]
 [Test]---+
```

### Los 4 eslabones

| Eslabon | Job | Que hace | Depende de |
|---------|-----|----------|------------|
| 1 | **Lint** | Ejecuta `flake8` para revisar errores de sintaxis | -- |
| 2 | **Test** | Ejecuta `pytest` para validar la logica del codigo | -- |
| 3 | **Train** | Entrena un RandomForest sobre Iris y sube el `.pkl` como artefacto | Lint, Test |
| 4 | **Deploy** | Descarga el artefacto y simula un despliegue a produccion | Train |

### Que aprendes?

- **Jobs en paralelo**: Lint y Test corren al mismo tiempo (no dependen entre si).
- **`needs: [linting, testing]`**: Train espera a que **ambos** pasen.
- **Artefactos**: `upload-artifact` guarda archivos entre Jobs. `download-artifact` los recupera.
- **`paths:`**: El workflow solo se ejecuta si cambian archivos relevantes (src, tests, etc).
- **`permissions:`**: Principio de menor privilegio -- el workflow solo puede leer, no escribir.

### Logging tipo semaforo

El script `train_iris.py` usa `colorlog` para mostrar mensajes con colores segun su severidad:

| Color | Nivel | Significado |
|-------|-------|-------------|
| Verde | `INFO` | Operacion exitosa, progreso normal |
| Amarillo | `WARNING` | Precaucion o advertencia |
| Rojo | `ERROR` | Fallo critico |

---

## Guia paso a paso

### 1. Fork del repositorio

Presiona el boton **Fork** en la esquina superior derecha de esta pagina. Esto crea una copia completa bajo tu cuenta de GitHub.

### 2. Habilitar GitHub Actions

Al hacer un fork, GitHub desactiva los workflows por seguridad.

- Ve a la pestana **Actions** en tu repositorio.
- Haz clic en **"I understand my workflows, go ahead and enable them"**.

### 3. Ejecutar Nivel 1

- En la pestana **Actions**, selecciona **"01 - Mi Primer Workflow"** en el menu lateral.
- Haz clic en **Run workflow**.
- Observa los logs: veras los mensajes de `echo` que escribimos en el YAML.

### 4. Ejecutar Nivel 2

- Selecciona **"02 - Jobs con Dependencias"**.
- Haz clic en **Run workflow**.
- Observa el grafo: veras dos cajas conectadas. La segunda espera a la primera.

### 5. Ejecutar Nivel 3

- Selecciona **"03 - Pipeline Completo de ML (Iris)"**.
- Haz clic en **Run workflow**.
- Observa el DAG: Lint y Test corren en paralelo, Train espera a ambos, Deploy espera a Train.
- Al finalizar, en la seccion **Artifacts** podras descargar el modelo entrenado.

---

## Ejecucion local

### Prerequisitos

- Python 3.10 o superior
- [uv](https://docs.astral.sh/uv/getting-started/installation/) instalado

### Instalacion

```bash
# Clonar el repositorio (o tu fork)
git clone https://github.com/<tu-usuario>/MasterClass_GithubActions.git
cd MasterClass_GithubActions

# Sincronizar dependencias (crea el virtualenv automaticamente)
uv sync
```

### Comandos utiles

```bash
# Ejecutar el script basico
uv run python src/hello.py

# Ejecutar el pipeline de entrenamiento
uv run python src/train_iris.py

# Correr las pruebas unitarias
uv run pytest tests/ -v

# Revisar calidad de codigo
uv run flake8 src/ tests/
```

---

## Glosario

| Termino | Definicion |
|---------|------------|
| **Workflow** | Archivo YAML que define un proceso automatizado en GitHub Actions. |
| **Job** | Un conjunto de pasos que se ejecutan en el mismo Runner. |
| **Step** | Una accion individual dentro de un Job (un comando o una accion preconstruida). |
| **Runner** | Maquina virtual efimera donde se ejecutan los Jobs. |
| **Trigger** | Evento que dispara un Workflow (`push`, `pull_request`, `workflow_dispatch`). |
| **Artifact** | Archivo generado durante un Workflow que se puede descargar o pasar entre Jobs. |
| **needs** | Directiva YAML para declarar dependencias entre Jobs. |
| **DAG** | Grafo Dirigido Aciclico -- la estructura que forman los Jobs con sus dependencias. |
| **Linting** | Analisis estatico del codigo para detectar errores de sintaxis y estilo. |
| **uv** | Gestor de paquetes y entornos virtuales para Python, extremadamente rapido. |

---

*Hecho para los estudiantes de Henry.*
