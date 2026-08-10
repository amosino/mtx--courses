# Cursos de Métodos Cuantitativos y Econometría

Este repositorio contiene el material de clase (diapositivas, tareas y códigos de R) para los siguientes cursos:

1. **[AppliedTS](AppliedTS/docs/index.html)**: Métodos Cuantitativos II (Series de Tiempo Aplicadas)
2. **[MTX1](MTX1/docs/index.html)**: Econometría I
3. **[MTX2](MTX2/docs/index.html)**: Econometría II
4. **[MTX3](MTX3/docs/index.html)**: Econometría III (Series de Tiempo Teóricas)

## Estructura de cada curso

Cada curso sigue la siguiente estructura estandarizada:

* `slides/`: Diapositivas fuente en formato R Markdown (`.Rmd`).
* `homeworks/`: Tareas y prácticas en R Markdown (`.Rmd`).
* `data/`: Conjuntos de datos utilizados en los ejemplos y tareas.
* `src/`: Recursos de estilo, como archivos CSS personalizados (`custom.css`).
* `docs/`: Archivos HTML y PDF compilados listos para visualizarse.

## Cómo trabajar con los cursos

Cada carpeta de curso es independiente y contiene su propio archivo de proyecto de RStudio (`.Rproj`). Se recomienda abrir el archivo `.Rproj` correspondiente al curso en el que se esté trabajando para que las rutas relativas se resuelvan de manera correcta mediante el paquete `here`.
