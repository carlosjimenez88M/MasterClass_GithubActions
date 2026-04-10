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

Este repositorio es una clase practica que te lleva desde cero hasta construir un **pipeline completo de Machine Learning** automatizado con GitHub Actions. Al finalizar seras capaz de:

- Entender que es CI/CD y por que es indispensable en proyectos reales.
- Escribir tus propios workflows en YAML.
- Encadenar tareas dependientes (DAG de jobs).
- Automatizar linting, testing, entrenamiento y deploy de un modelo.

> [!NOTE]
> **Requisitos previos:** Conocimientos basicos de Python y Git. No se necesita experiencia previa con CI/CD ni con GitHub Actions.

---

## Tabla de contenidos

1. [Conceptos clave](#conceptos-clave)
2. [Estructura del repositorio](#estructura-del-repositorio)
3. [Los Pipelines](#los-pipelines)
4. [Guia paso a paso](#guia-paso-a-paso)
5. [Ejecucion local](#ejecucion-local)
6. [Glosario](#glosario)

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
> **Runner** = maquina virtual temporal que GitHub te presta para ejecutar los pasos. Se destruye al terminar.

---

## Estructura del repositorio

```text
MasterClass_GithubActions/
|-- .github/
|   |-- workflows/
|       |-- 01-basic-workflow.yml      # Pipeline basico (Hola Mundo)
|       |-- 02-ml-pipeline.yml         # Pipeline ML con eslabones
|-- src/
|   |-- __init__.py
|   |-- hello.py                       # Script introductorio
|   |-- train_iris.py                  # Pipeline de entrenamiento (Iris)
|-- tests/
|   |-- test_hello.py                  # Tests del modulo hello
|   |-- test_train.py                  # Tests del pipeline ML
|-- pyproject.toml                     # Dependencias y config del proyecto
|-- uv.lock                           # Lockfile para builds reproducibles
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

## Los Pipelines

### Pipeline 1: Flujo Basico

**Archivo:** `.github/workflows/01-basic-workflow.yml`

Un solo job que clona el repo, instala `uv`, sincroniza dependencias y ejecuta `hello.py`. Sirve para entender la mecanica fundamental.

```text
[push a main] --> [checkout] --> [setup uv] --> [uv sync] --> [run hello.py]
```

### Pipeline 2: ML con Eslabones Dependientes

**Archivo:** `.github/workflows/02-ml-pipeline.yml`

Cuatro jobs encadenados que forman un grafo dirigido (DAG):

```text
 [Lint]---+
          +--> [Train] --> [Deploy]
 [Test]---+
```

| Eslabon | Job | Que hace | Depende de |
|---------|-----|----------|------------|
| 1 | **Lint** | Ejecuta `flake8` para revisar errores de sintaxis | -- |
| 2 | **Test** | Ejecuta `pytest` para validar la logica | -- |
| 3 | **Train** | Entrena un RandomForest sobre Iris y sube el `.pkl` como artefacto | Lint, Test |
| 4 | **Deploy** | Descarga el artefacto y simula un despliegue a produccion | Train |

> [!IMPORTANT]
> El job de **Train** solo se ejecuta si Lint y Test pasan exitosamente. Esto se logra con la directiva `needs: [linting, testing]` en el YAML.

### Logging tipo semaforo

El script `train_iris.py` usa `colorlog` para mostrar mensajes con colores segun su severidad:

| Color | Nivel | Significado |
|-------|-------|-------------|
| Verde | `INFO` | Operacion exitosa, resultado, progreso normal |
| Amarillo | `WARNING` | Precaucion o advertencia real |
| Rojo | `ERROR` | Fallo critico en el pipeline |

---

## Guia paso a paso

### 1. Fork del repositorio

Presiona el boton **Fork** en la esquina superior derecha de esta pagina. Esto crea una copia completa bajo tu cuenta de GitHub.

### 2. Habilitar GitHub Actions

Al hacer un fork, GitHub desactiva los workflows por seguridad.

- Ve a la pestana **Actions** en tu repositorio.
- Haz clic en **"I understand my workflows, go ahead and enable them"**.

### 3. Disparar un workflow manualmente

- En la pestana **Actions**, selecciona el workflow que quieras probar en el menu lateral.
- Haz clic en **Run workflow** a la derecha.

### 4. Observar el grafo

Una vez que inicie la ejecucion, haz clic sobre ella para ver el **grafo de dependencias** en tiempo real. Veras como Lint y Test corren en paralelo, y Training espera a que ambos terminen.

### 5. Descargar el modelo

Al finalizar el pipeline ML, en la pagina del workflow aparece una seccion **Artifacts** con el archivo `ml-model-iris` disponible para descarga.

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
| **Trigger** | Evento que dispara un Workflow (push, pull\_request, workflow\_dispatch, etc.). |
| **Artifact** | Archivo generado durante un Workflow que se puede descargar o pasar entre Jobs. |
| **needs** | Directiva YAML para declarar dependencias entre Jobs. |
| **DAG** | Grafo Dirigido Aciclico -- la estructura que forman los Jobs con sus dependencias. |
| **Linting** | Analisis estatico del codigo para detectar errores de sintaxis y estilo. |
| **uv** | Gestor de paquetes y entornos virtuales para Python, extremadamente rapido. |

---

*Hecho para los estudiantes de Henry.*
