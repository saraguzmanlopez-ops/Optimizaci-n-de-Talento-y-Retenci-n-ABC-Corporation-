# **Proyecto: Optimización de Talento y Retención (ABC Corporation)**


# Documentación: Fase 1 - Análisis Exploratorio de Datos (EDA)

---

## 1. Introducción y Objetivos

Siguiendo la metodología de la Lección 3.3, hemos iniciado la fase de exploración para familiarizarnos con el conjunto de datos de ABC Corporation. El objetivo es auditar la calidad de la información antes de proceder a cualquier transformación o análisis predictivo.

Preguntas guía del análisis:

- ¿Qué inconsistencias técnicas (nulos, duplicados, tipos) debemos resolver para asegurar la fiabilidad de los datos?
- ¿Qué variables no aportan valor real al negocio por ser constantes o redundantes?

---

## 2. Validación del Modelo de Datos 

Tras una inspección técnica inicial, se han validado los siguientes pilares de calidad:

- Tamaño del dataset: 1,474 registros y 35 columnas.
- Unicidad: Se han localizado 4 registros duplicados (identificados en los índices finales: 1470, 1471, 1472 y 1473).
- Consistencia de expresiones: Se ha detectado "ruido" en variables categóricas, como variaciones de formato en JobRole y erratas tipográficas en MaritalStatus (valor 'Marreid').

---

## 3. Diccionario de Datos y Auditoría Completa (35 columnas)

### A. Variables con Hallazgos Críticos (Acción necesaria en Fase 2)

| Columna | Descripción | Hallazgos Detallados (Fase 1) |
| :--- | :--- | :--- |
| **BusinessTravel** | Frecuencia de viajes | Contiene **valores nulos**. |
| **Department** | Departamento actual | String. Presenta **nulos** e inconsistencias de escritura. |
| **EducationField** | Área de estudios | Contiene **valores nulos**. |
| **EmployeeCount** | Contador de empleados | **Redundante:** Valor constante (1). Se eliminará. |
| **EnvironmentSatisfaction** | Satisfacción entorno | Escala 1-4. Presenta **valores nulos**. |
| **JobRole** | Puesto de trabajo | **Muy sucia:** Espacios extra y mezcla de mayúsculas/minúsculas. |
| **JobRole (consistencia semántica)** | Puesto de trabajo | Se detecta que algunos roles como **"Manager"** aparecen en múltiples departamentos, generando ambigüedad en la interpretación. |
| **MaritalStatus** | Estado civil | **Errata detectada:** Contiene el valor `'Marreid'`. |
| **Over18** | Mayoría de edad | **Redundante:** Todos son "Y". Innecesaria existiendo `Age`. |
| **StandardHours** | Horas jornada | **Redundante:** Valor constante (80) o nulo. Se eliminará. |
| **TotalWorkingYears** | Experiencia total | **Punto Crítico:** Valores sospechosos y **32% de nulos**. |
| **TrainingTimesLastYear** | Formaciones año ant. | **Nulos** detectados. Formato `float64` (debe ser `int`). |
| **WorkLifeBalance** | Conciliación | **Nulos** detectados. Escala 1-4. |
| **YearsInCurrentRole** | Años puesto actual | Hallazgo de valores consecutivos sospechosos. |
| **YearsWithCurrManager** | Años con jefe actual | Contiene **nulos**. Formato `float64` (debe ser `int`). |

---

### B. Variables de Perfil y Compensación (Datos íntegros)

| Columna | Descripción | Estado / Hallazgo |
| :--- | :--- | :--- |
| **Age** | Edad del empleado | OK. Formato `float64` (se pasará a `int` tras limpiar nulos). |
| **DailyRate** | Salario por día | OK. Íntegra, aunque su valor analítico se evaluará en Fase 2. |
| **DistanceFromHome** | Distancia al trabajo | OK. Se detectan posibles valores atípicos o codificaciones no estándar. |
| **Education** | Nivel académico | OK. Escala del 1 al 5. |
| **EmployeeNumber** | ID de empleado | OK. Identificador único del registro. |
| **Gender** | Género | OK. Sin nulos. |
| **HourlyRate** | Salario por hora | OK. Variable íntegra, aunque su valor analítico se evaluará en Fase 2. |
| **JobInvolvement** | Compromiso laboral | OK. Escala 1-4. |
| **JobLevel** | Nivel jerárquico | OK. Escala 1-5. |
| **JobSatisfaction** | Satisfacción puesto | OK. Escala 1-4. |
| **MonthlyIncome** | Salario mensual | OK. Variable continua sin nulos. |
| **MonthlyRate** | Tasa mensual | OK. Variable íntegra, aunque su valor analítico se evaluará en Fase 2. |
| **NumCompaniesWorked** | Empresas anteriores | OK. Conteo numérico. |
| **OverTime** | Horas extra | OK. Categórica (Yes/No). |
| **PercentSalaryHike** | % aumento salarial | OK. Datos coherentes. |
| **PerformanceRating** | Evaluación desempeño | OK. Escala numérica. |
| **RelationshipSatisfaction** | Satisfacción social | OK. Escala 1-4. |
| **StockOptionLevel** | Opciones de acciones | OK. Escala 0-3. |
| **YearsAtCompany** | Antigüedad empresa | OK. Rango 0-40 años. |
| **YearsSinceLastPromotion** | Años últ. ascenso | OK. Rango 0-15 años. |
| **Attrition** | Rotación (Yes/No) | **Variable Objetivo.** Íntegra. |

---

## 4. Conclusiones y Estrategia de Limpieza

Tras la auditoría realizada en la Fase 1, el equipo concluye que el dataset requiere las siguientes intervenciones:

- Eliminación de registros duplicados.
- Eliminación de columnas constantes, redundantes o de baja interpretabilidad analítica.
- Normalización de variables categóricas.
- Gestión de nulos mediante una estrategia basada en moda y mediana, priorizando imputaciones condicionadas por variables de negocio.
- Conversión de tipos de datos.

Además, se identifica la necesidad de mejorar la interpretabilidad de ciertas variables categóricas, como **JobRole**, donde algunos valores resultan demasiado genéricos y pueden generar ambigüedad analítica.

---

## 5. Interpretación del contexto del dataset

A partir de la exploración de los datos, se identifican varios elementos que permiten contextualizar el dataset:

- La empresa parece estar basada en California.
- Las variables salariales sugieren que la moneda utilizada es el dólar, mientras que `DistanceFromHome` indica que la distancia se mide en millas.
- La variable `StandardHours` indica una jornada estándar de 80 horas (probablemente en formato quincenal).
- Existen variables que aportan información redundante o parcialmente solapada sobre otras, especialmente en el ámbito salarial y de experiencia.

---

# Documentación: Fase 2 - Transformación y Limpieza de Datos

---

## 1. Introducción y Objetivos

Tras la fase exploratoria, se ha llevado a cabo la limpieza y transformación del dataset con el objetivo de mejorar su calidad, coherencia y utilidad analítica.

---

## 2. Eliminación de Registros Duplicados

Se eliminan los registros duplicados detectados.

---

## 3. Eliminación de Variables

Se eliminan:

- EmployeeCount  
- Over18  
- StandardHours  
- DailyRate  
- HourlyRate  
- MonthlyRate  

Se eliminan por tratarse de variables constantes, redundantes o con menor capacidad explicativa frente a otras más representativas como `MonthlyIncome`.

---

## 4. Estandarización

- Limpieza de strings  
- Corrección de erratas  
- Columnas en formato Title_Case  

Adicionalmente, se ha llevado a cabo un enriquecimiento de la variable **JobRole**, incorporando el departamento en aquellos casos donde el puesto era demasiado genérico, con el objetivo de mejorar su interpretabilidad y evitar ambigüedades detectadas en la fase exploratoria.

---

## 5. Gestión de Nulos

Se aplica una estrategia diferenciada en función de la naturaleza de cada variable.

---

## 6. Auditoría de Imputación de Nulos

| Columna | Tipo | % Nulos | Método | Variable de referencia | Justificación técnica | Justificación de negocio | Alternativas descartadas |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **BusinessTravel** | Categórica | Bajo | Moda | Global | No es apropiado usar media o mediana en variables categóricas; la moda conserva la distribución original. | Mantiene el comportamiento más frecuente de viajes sin introducir categorías artificiales. | Eliminación de filas; imputación aleatoria; categoría “Unknown”. |
| **MaritalStatus** | Categórica | Bajo | Moda | Global | Tras corregir la errata (`Marreid`), la moda es la mejor opción. | Refleja el estado civil predominante sin alterar la estructura. | Mantener errata; imputación aleatoria; “Unknown”. |
| **TrainingTimesLastYear** | Discreta | Bajo | Moda | Global | Evita valores decimales irreales. | Mantiene comportamiento organizacional. | Media; mediana; imputación 0. |
| **EducationField** | Categórica | Medio | Moda | Department | Mantiene contexto interno. | Relación directa con el departamento. | Moda global; aleatorio; eliminar filas. |
| **YearsWithCurrManager** | Numérica | Bajo | Mediana | JobLevel | Robusta ante outliers. | Relación con jerarquía. | Media; moda; global. |
| **Age** | Numérica | Bajo | Mediana | JobLevel | Evita sesgos. | Relación con nivel profesional. | Media; moda; global. |

---

## 7. Conversión de Tipos

- Age  
- TrainingTimesLastYear  
- YearsWithCurrManager  

---

## 8. Resultado

Dataset limpio, coherente y preparado para análisis.

---

## 9. Conclusión

Se ha mejorado la calidad del dataset aplicando criterios técnicos y de negocio, garantizando una base sólida para fases posteriores del proyecto.

---

# Documentación: Fase 3 - Análisis, Visualización e Insights

---

## 1. Introducción

Tras la fase de exploración y limpieza de datos, se aborda el análisis del fenómeno de attrition con un enfoque orientado a negocio.

---

## 2. Enfoque del análisis

El análisis se estructura en:

- Variables individuales  
- Distribución de bajas  
- Impacto del Over Time  
- Variables combinadas  
- Salario  
- Satisfacción  

---

## 3. Principales insights

- El attrition es mayor en niveles jerárquicos bajos y empleados con menor antigüedad  
- El Over Time es uno de los factores más determinantes  
- La combinación de bajo Job Level y alta carga de trabajo genera los niveles más altos de attrition  
- El salario influye, aunque condicionado por el nivel jerárquico  
- Los empleados que abandonan presentan menores niveles de satisfacción  

---

## 4. Conclusiones

El attrition se concentra en segmentos específicos:

- Perfiles junior  
- Alta carga de trabajo  
- Baja satisfacción  

---

## 5. Recomendaciones

- Reducir el Over Time  
- Reforzar el onboarding  
- Definir planes de carrera  
- Mejorar la satisfacción  
- Incentivar la retención a largo plazo  

---

## 6. Cierre

El análisis permite identificar dónde ocurre el attrition, comprender sus causas y definir acciones para reducirlo.


---

# BONUS
# Documentación: Fase 4 - Proceso ETL (Extracción, Transformación y Carga de Datos)

---

## 1. Introducción y Objetivos

En esta fase se ha implementado un proceso ETL con el objetivo de integrar los datos transformados en una base de datos relacional.

A diferencia de las fases anteriores, centradas en la limpieza y análisis, esta etapa tiene como propósito trasladar el dataset final a un entorno estructurado, permitiendo su almacenamiento, consulta y reutilización.

El objetivo principal es:

- Cargar los datos limpios generados en la Fase 2  
- Integrarlos en una base de datos relacional  
- Facilitar su explotación posterior  

---

## 2. Enfoque del proceso

El proceso ETL desarrollado en esta fase se centra principalmente en las etapas de **carga (Load)**, partiendo de un dataset ya transformado.

El flujo seguido es:

1. Uso del dataset limpio generado en la Fase 2  
2. Conexión a la base de datos mediante SQLAlchemy  
3. Inserción del DataFrame en una tabla SQL  

Este enfoque permite conectar directamente el análisis realizado con una estructura persistente de datos.

---

## 3. Fuente de datos

Se utiliza el dataset limpio generado en la Fase 2, el cual ya ha sido sometido a:

- Eliminación de duplicados  
- Limpieza de variables  
- Imputación de nulos  
- Estandarización  
- Enriquecimiento de variables como JobRole  

Esto garantiza que los datos cargados en la base de datos son consistentes y aptos para su uso analítico.

---

## 4. Conexión a la base de datos

Se establece la conexión con la base de datos utilizando la librería **SQLAlchemy**.

A través de un engine, se define la conexión con el entorno de base de datos, permitiendo la interacción entre pandas y el sistema relacional.

Esta conexión actúa como punto de entrada para la carga de datos.

---

## 5. Carga de datos

La carga se realiza mediante la conversión del DataFrame a una tabla SQL.

Se utiliza el método:

- `to_sql()` de pandas  

Esto permite insertar directamente los datos del DataFrame en la base de datos.

Como resultado:

- Se crea el esquema **ABC_Corporation**  
- Se genera la tabla **employees_attrition**  
- Se insertan los datos correspondientes  

La tabla contiene el dataset completo tras las transformaciones realizadas en fases anteriores.

---

## 6. Resultado

Tras la ejecución del proceso, los datos quedan almacenados en MySQL Workbench con la siguiente estructura:

- **Schema:** ABC_Corporation  
- **Tabla:** employees_attrition  

Esto permite:

- Consultar los datos mediante SQL  
- Integrarlos en herramientas externas  
- Facilitar su uso en análisis posteriores  

---

## 7. Conclusiones

La implementación de esta fase permite cerrar el ciclo de tratamiento de datos del proyecto.

Se ha conseguido:

- Integrar el dataset limpio en una base de datos relacional  
- Establecer un puente entre análisis en Python y almacenamiento estructurado  
- Facilitar la explotación de los datos en entornos SQL  

---

## 8. Cierre

Esta fase aporta un valor adicional al proyecto, al trasladar los datos a un entorno persistente y escalable.

De este modo, el proyecto no solo realiza análisis, sino que también establece una base sólida para la gestión y reutilización de los datos.