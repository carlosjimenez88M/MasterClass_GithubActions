# MasterClass: Introduccion a GitHub Actions (Especialidad Data & ML)

![alt text](https://www.soyhenry.com/_next/static/media/HenryLogo.bb57fd6f.svg)

Bienvenidos a la clase magistral sobre **GitHub Actions**. Este repositorio esta disenado paso a paso para que puedan comprender como funciona la Integracion Continua (CI) y Despliegue Continuo (CD), y como aplicarlo a proyectos de *Machine Learning*.

> [!TIP]
> **Que es GitHub Actions?** Es una plataforma que te permite automatizar tareas directamente en tu repositorio de GitHub. Piensa en ello como tener un "robot" (llamado *Runner*) que ejecuta scripts de forma automatica cada vez que ocurre un evento (por ejemplo, cuando alguien hace un `git push`).

---

## Que contiene este repositorio?

El codigo fuente de los ejercicios esta disenado en Python y hemos armado dos "Flujos de trabajo" (`workflows`) diferentes, desde lo elemental hasta simulaciones mas realistas de *pipelines* de datos.

### La estructura base
- `src/hello.py`: Un simple "Hola Mundo".
- `src/train_iris.py`: Un script real usando `scikit-learn` que carga el famoso *dataset* Iris, lo divide y entrena un modelo de clasificacion Random Forest, con logs colorizados.
- `tests/`: Contiene pruebas automatizadas para asegurar que nuestro codigo nunca se rompa.
- `pyproject.toml`: Declaracion de las dependencias controladas por `uv` (el gestor mas veloz en Python moderno).

### Los Flujos de Trabajo (Pipelines)

Todo lo que GitHub Actions ejecuta automaticamente esta en la carpeta secreta `.github/workflows/`. Aqui alojamos archivos `.yml` que son nuestras "instrucciones" para el robot.

#### 1. El Flujo Basico (`01-basic-workflow.yml`)
Un pipeline sencillo que se encarga de lo primordial. Un solo "tarea" (o **Job**).
* Clona el codigo fuente.
* Configura e instala `uv` y Python.
* Ejecuta nuestro script de Hola Mundo.
Ideal para entender la anatomia de un evento *Trigger* (el `on: push`).

#### 2. Pipeline Avanzado de Machine Learning (`02-ml-pipeline.yml`)
Esta es la joya de la corona. Un flujo con **Eslabones Dependientes**. Dividiremos el trabajo en 4 "Jobs" principales paralelos y dependientes:

1. **Linting:** Verifica que los estandares de codigo sean correctos usando *Flake8*.
2. **Testing:** Corre las pruebas unitarias usando *Pytest*. Nadie quiere desplegar modelos rotos.
3. **Training (Entrenamiento):** Entrena el modelo **SOLO SI** (depende de: `needs: [linting, testing]`) los eslabones #1 y #2 fueron exitosos. Genera un archivo `.pkl` (nuestro modelo entrenado) y lo sube como "Artefacto" para que lo podamos descargar.
4. **Deploy Simulado:** Toma el artefacto (.pkl) recien creado y simula el despliegue del mismo. Depende exclusivamente de que el `Training` finalice correctamente.

---

## Como ponerlo en practica (Paso a Paso)

Sigue estos pasos para observar tu mismo la magia de la automatizacion:

1. **Haz un Fork de este Repositorio:**
   Presiona el boton "Fork" arriba a la derecha de esta misma pagina. Esto clonara *todo* este contenido bajo tu propio usuario de GitHub.

2. **Habilita los Workflows:**
   Por seguridad, al hacer un fork, GitHub pausa los flujos de trabajo.
   * Ve a la pestana **Actions** en tu nuevo repositorio.
   * Presiona el boton verde gigante que dice **"I understand my workflows, go ahead and enable them"**.

3. **Dispara manualente una tarea:**
   * En la misma pestana de **Actions**, en la lista de la izquierda veras los nombres de nuestros pipelines (ej. `02 - Pipeline de Machine Learning`).
   * Haz clic sobre uno de ellos. Luego presiona el boton blanco a la derecha que dice **Run workflow**.

4. **Observa el grafico!**
   Una vez que inicie, haz clic sobre el evento en curso y podras ver un **grafo (DAG)** fascinante donde los eslabones (`Linting` y `Testing`) corren en paralelo y envian una senal a `Training` una vez que terminan.
   
   Al finalizar, en la pantalla principal del workflow veras un apartado llamado **Artifacts** que te dejara descargar tu modelo entrenado de Iris.

---
*Hecho para los estudiantes.*
