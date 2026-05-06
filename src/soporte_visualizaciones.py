import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


class Visualizaciones:
    """
    Clase para generar visualizaciones reutilizables para el análisis de attrition.
    """

    def __init__(
        self,
        dataframe,
        palette_attrition=None,
        palette_seq="viridis",
        style="whitegrid"):
        """
        Inicializa la clase con un DataFrame y una configuración visual básica.

        Parámetros
        ----------
        dataframe : pandas.DataFrame
            DataFrame sobre el que se realizarán las visualizaciones.
        palette_attrition : dict, optional
            Diccionario de colores para Attrition.
            Si no se indica, se usa una paleta por defecto.
        palette_seq : str, default="viridis"
            Paleta secuencial para gráficos con varias categorías.
        style : str, default="whitegrid"
            Estilo general de seaborn.
        """
        self.dataframe = dataframe

        if palette_attrition is None:
            self.palette_attrition = {"No": "seagreen", "Yes": "crimson"}
        else:
            self.palette_attrition = palette_attrition

        self.palette_seq = palette_seq

        sns.set_theme(style=style)
        plt.rcParams["figure.figsize"] = (10, 6)

    # MÉTODOS AUXILIARES

    def configurar_ejes(self, ax, titulo="", xlabel="", ylabel="", rotation=0):
        """
        Aplica un formato común a los ejes del gráfico.
        """
        ax.set_title(str(titulo).replace("_", " "), fontsize=14, fontweight="bold")
        ax.set_xlabel(str(xlabel).replace("_", " "))
        ax.set_ylabel(str(ylabel).replace("_", " "))

        if rotation != 0:
            ax.tick_params(axis="x", rotation=rotation)

        sns.despine(ax=ax)

    def anotar_barras_verticales(self, ax, decimales=1, sufijo="%"):
        """
        Añade etiquetas a barras verticales.
        """
        for barra in ax.patches:
            altura = barra.get_height()

            if pd.notna(altura) and altura > 0:
                ax.annotate(
                    f"{altura:.{decimales}f}{sufijo}",
                    (barra.get_x() + barra.get_width() / 2, altura),
                    ha="center",
                    va="bottom",
                    xytext=(0, 4),
                    textcoords="offset points")

    def anotar_barras_horizontales(self, ax, decimales=1, sufijo="%"):
        """
        Añade etiquetas a barras horizontales.
        """
        for barra in ax.patches:
            ancho = barra.get_width()

            if pd.notna(ancho) and ancho > 0:
                ax.annotate(
                    f"{ancho:.{decimales}f}{sufijo}",
                    (ancho, barra.get_y() + barra.get_height() / 2),
                    ha="left",
                    va="center",
                    xytext=(5, 0),
                    textcoords="offset points")

    def filtrar_valores(self, columna, excluir_valores=None):
        """
        Filtra el DataFrame excluyendo uno o varios valores de una columna.
        """
        df_filtrado = self.dataframe.copy()

        if excluir_valores is not None:
            if isinstance(excluir_valores, list):
                df_filtrado = df_filtrado[~df_filtrado[columna].isin(excluir_valores)]
            else:
                df_filtrado = df_filtrado[df_filtrado[columna] != excluir_valores]

        return df_filtrado

    # 1. ATTRITION GENERAL

    def tasa_attrition_categoria(
        self,
        columna,
        attrition_col="Attrition_num",
        titulo=None,
        xlabel=None,
        ylabel="Attrition Rate (%)",
        figsize=(8, 5),
        excluir_valores=None,
        annot=True):
        """
        Calcula y representa la tasa de attrition media por categoría.
        """
        df_filtrado = self.filtrar_valores(columna, excluir_valores)

        df_plot = df_filtrado.groupby(columna)[attrition_col].mean().reset_index()
        df_plot[attrition_col] = df_plot[attrition_col] * 100

        colores = sns.color_palette(self.palette_seq, len(df_plot))

        plt.figure(figsize=figsize)

        ax = sns.barplot(
            data=df_plot,
            x=columna,
            y=attrition_col,
            hue=columna,
            dodge=False,
            palette=colores)

        if ax.get_legend() is not None:
            ax.get_legend().remove()

        if titulo is None:
            titulo = f"Attrition Rate by {columna.replace('_', ' ')}"

        if xlabel is None:
            xlabel = columna.replace("_", " ")

        self.configurar_ejes(
            ax,
            titulo=titulo,
            xlabel=xlabel,
            ylabel=ylabel)

        if annot:
            self.anotar_barras_verticales(ax)

        plt.tight_layout()
        plt.show()

    def tasa_attrition_years_at_company_group(
        self,
        years_col="Years_At_Company",
        attrition_col="Attrition",
        bins=None,
        labels=None,
        nueva_columna="Years_At_Company_Group",
        titulo="Attrition Rate by Years at Company",
        xlabel="Years at Company",
        ylabel="Attrition Rate (%)",
        figsize=(8, 5),
        annot=True):
        """
        Agrupa Years at Company en rangos y representa la tasa de attrition por grupo.
        """
        df_plot = self.dataframe.copy()

        if bins is None:
            bins = [-1, 2, 5, 10, 20, 40]

        if labels is None:
            labels = ["0-2", "3-5", "6-10", "11-20", "20+"]

        df_plot[nueva_columna] = pd.cut(
            df_plot[years_col],
            bins=bins,
            labels=labels)

        tabla = (
            pd.crosstab(df_plot[nueva_columna], df_plot[attrition_col], normalize="index")
            .mul(100)
            .round(2)
            .reset_index())

        tabla = tabla[[nueva_columna, "Yes"]]
        tabla.columns = [nueva_columna, "Attrition_Rate"]

        colores = sns.color_palette(self.palette_seq, len(tabla))

        plt.figure(figsize=figsize)

        ax = sns.barplot(
            data=tabla,
            x=nueva_columna,
            y="Attrition_Rate",
            hue=nueva_columna,
            dodge=False,
            palette=colores)

        if ax.get_legend() is not None:
            ax.get_legend().remove()

        self.configurar_ejes(
            ax,
            titulo=titulo,
            xlabel=xlabel,
            ylabel=ylabel)

        if annot:
            self.anotar_barras_verticales(ax, decimales=2)

        plt.tight_layout()
        plt.show()

    def tasa_attrition_business_travel(
        self,
        columna="Business_Travel",
        attrition_col="Attrition_num",
        titulo="Attrition Rate by Business Travel",
        xlabel="Business Travel",
        ylabel="Attrition Rate (%)",
        figsize=(8, 5),
        excluir_valores=None,
        annot=True):
        """
        Representa la tasa de attrition según la frecuencia de viajes de trabajo.
        """
        self.tasa_attrition_categoria(
            columna=columna,
            attrition_col=attrition_col,
            titulo=titulo,
            xlabel=xlabel,
            ylabel=ylabel,
            figsize=figsize,
            excluir_valores=excluir_valores,
            annot=annot)

    def tasa_attrition_stock_option_level(
        self,
        columna="Stock_Option_Level",
        attrition_col="Attrition_num",
        titulo="Attrition Rate by Stock Option Level",
        xlabel="Stock Option Level",
        ylabel="Attrition Rate (%)",
        figsize=(8, 5),
        excluir_valores=None,
        annot=True):
        """
        Representa la tasa de attrition según el nivel de stock options.
        """
        self.tasa_attrition_categoria(
            columna=columna,
            attrition_col=attrition_col,
            titulo=titulo,
            xlabel=xlabel,
            ylabel=ylabel,
            figsize=figsize,
            excluir_valores=excluir_valores,
            annot=annot)

    def tasa_attrition_marital_status(
        self,
        columna="Marital_Status",
        attrition_col="Attrition_num",
        titulo="Attrition Rate by Marital Status",
        xlabel="Marital Status",
        ylabel="Attrition Rate (%)",
        figsize=(8, 5),
        excluir_valores=None,
        annot=True):
        """
        Representa la tasa de attrition según el estado civil.
        """
        self.tasa_attrition_categoria(
            columna=columna,
            attrition_col=attrition_col,
            titulo=titulo,
            xlabel=xlabel,
            ylabel=ylabel,
            figsize=figsize,
            excluir_valores=excluir_valores,
            annot=annot)

    def tasa_attrition_hue(
        self,
        columna,
        hue,
        titulo=None,
        xlabel=None,
        ylabel="Percentage (%)",
        figsize=(8, 5),
        palette=None,
        excluir_valores=None,
        hue_order=None):
        """
        Representa el porcentaje interno de una variable hue dentro de cada categoría.
        """
        df_filtrado = self.filtrar_valores(columna, excluir_valores)

        df_plot = (
            df_filtrado.groupby(columna)[hue]
            .value_counts(normalize=True)
            .reset_index(name="percentage"))

        df_plot["percentage"] = df_plot["percentage"] * 100

        if palette is None:
            palette = self.palette_seq

        plt.figure(figsize=figsize)

        ax = sns.barplot(
            data=df_plot,
            x=columna,
            y="percentage",
            hue=hue,
            hue_order=hue_order,
            palette=palette)

        if titulo is None:
            titulo = f"{hue.replace('_', ' ')} Rate by {columna.replace('_', ' ')}"

        if xlabel is None:
            xlabel = columna.replace("_", " ")

        self.configurar_ejes(
            ax,
            titulo=titulo,
            xlabel=xlabel,
            ylabel=ylabel)

        ax.legend(title=hue.replace("_", " "))

        for container in ax.containers:
            ax.bar_label(container, fmt="%.1f%%", padding=2)

        plt.tight_layout()
        plt.show()

    def barras_attrition(
        self,
        x,
        hue,
        attrition_col="Attrition_num",
        excluir_valores_hue=None,
        hue_order=None,
        titulo=None,
        figsize=(9, 5),
        xlabel=None,
        ylabel="Percentage (%)",
        legend_title=None):
        """
        Representa la tasa de attrition por combinación de dos variables mediante barras agrupadas.
        """
        df_filtrado = self.dataframe.copy()

        if excluir_valores_hue is not None:
            if isinstance(excluir_valores_hue, list):
                df_filtrado = df_filtrado[~df_filtrado[hue].isin(excluir_valores_hue)]
            else:
                df_filtrado = df_filtrado[df_filtrado[hue] != excluir_valores_hue]

        df_plot = df_filtrado.groupby([x, hue])[attrition_col].mean().reset_index()
        df_plot[attrition_col] = df_plot[attrition_col] * 100

        plt.figure(figsize=figsize)

        ax = sns.barplot(
            data=df_plot,
            x=x,
            y=attrition_col,
            hue=hue,
            hue_order=hue_order,
            palette=self.palette_seq)

        if titulo is None:
            titulo = f"Attrition Rate by {x.replace('_', ' ')} and {hue.replace('_', ' ')}"

        if xlabel is None:
            xlabel = x.replace("_", " ")

        if legend_title is None:
            legend_title = hue.replace("_", " ")

        self.configurar_ejes(
            ax,
            titulo=titulo,
            xlabel=xlabel,
            ylabel=ylabel)

        ax.legend(title=legend_title)

        for container in ax.containers:
            ax.bar_label(container, fmt="%.1f%%", padding=2)

        plt.tight_layout()
        plt.show()

    def heatmap_attrition(
        self,
        fila,
        columna,
        attrition_col="Attrition_num",
        excluir_valores_columna=None,
        ordenar_columnas=None,
        titulo=None,
        figsize=(8, 5),
        cmap="Reds"):
        """
        Genera un heatmap con la tasa de attrition media para la combinación de dos variables.
        """
        df_filtrado = self.dataframe.copy()

        if excluir_valores_columna is not None:
            if isinstance(excluir_valores_columna, list):
                df_filtrado = df_filtrado[~df_filtrado[columna].isin(excluir_valores_columna)]
            else:
                df_filtrado = df_filtrado[df_filtrado[columna] != excluir_valores_columna]

        tabla = pd.crosstab(
            index=df_filtrado[fila],
            columns=df_filtrado[columna],
            values=df_filtrado[attrition_col],
            aggfunc="mean")

        tabla = tabla * 100
        tabla = tabla.round(2)

        if ordenar_columnas is not None:
            columnas_finales = [col for col in ordenar_columnas if col in tabla.columns]
            tabla = tabla[columnas_finales]

        plt.figure(figsize=figsize)

        ax = sns.heatmap(
            tabla,
            annot=True,
            fmt=".2f",
            cmap=cmap,
            linewidths=0.5,
            cbar_kws={"label": "Attrition Rate (%)"})

        if titulo is None:
            titulo = f"Attrition Rate by {fila.replace('_', ' ')} and {columna.replace('_', ' ')}"

        self.configurar_ejes(
            ax,
            titulo=titulo,
            xlabel=columna.replace("_", " "),
            ylabel=fila.replace("_", " "))

        plt.tight_layout()
        plt.show()

    # 2. DISTRIBUCIÓN DE BAJAS

    def distribucion_bajas_doble(
        self,
        columna_1,
        columna_2,
        attrition_col="Attrition_num",
        titulos=None,
        figsize=(16, 7)):
        """
        Compara la distribución porcentual de dos variables dentro del total de bajas.
        """
        df_bajas = self.dataframe[self.dataframe[attrition_col] == 1]

        serie_1 = df_bajas[columna_1].value_counts(normalize=True) * 100
        serie_1 = serie_1.sort_values(ascending=True)

        serie_2 = df_bajas[columna_2].value_counts(normalize=True) * 100
        serie_2 = serie_2.sort_values(ascending=True)

        fig, axes = plt.subplots(1, 2, figsize=figsize)

        sns.barplot(
            x=serie_1.values,
            y=serie_1.index,
            palette=sns.color_palette(self.palette_seq, len(serie_1)),
            ax=axes[0])

        if titulos is not None:
            titulo_1 = titulos[0]
        else:
            titulo_1 = f"Distribution of Leavers by {columna_1}"

        self.configurar_ejes(
            axes[0],
            titulo=titulo_1,
            xlabel="Percentage of Leavers (%)",
            ylabel=columna_1)
        self.anotar_barras_horizontales(axes[0])

        sns.barplot(
            x=serie_2.values,
            y=serie_2.index,
            palette=sns.color_palette(self.palette_seq, len(serie_2)),
            ax=axes[1])

        if titulos is not None:
            titulo_2 = titulos[1]
        else:
            titulo_2 = f"Distribution of Leavers by {columna_2}"

        self.configurar_ejes(
            axes[1],
            titulo=titulo_2,
            xlabel="Percentage of Leavers (%)",
            ylabel=columna_2)
        self.anotar_barras_horizontales(axes[1])

        plt.tight_layout()
        plt.show()

    def distribucion_bajas_job_role(
        self,
        columna="Job_Role",
        attrition_col="Attrition_num",
        titulo="Distribution of Leavers by Job Role (%)",
        xlabel="Percentage of Leavers (%)",
        ylabel="Job Role",
        figsize=(10, 6)
    ):
        """
        Representa la distribución porcentual de bajas por Job Role.
        """

        # Filtrar solo empleados que se han ido
        df_bajas = self.dataframe[self.dataframe[attrition_col] == 1]

        # Calcular porcentaje
        serie = (
            df_bajas[columna]
            .value_counts(normalize=True)
            .mul(100)
            .sort_values(ascending=True)
        )

        plt.figure(figsize=figsize)

        ax = sns.barplot(
            x=serie.values,
            y=serie.index,
            palette=sns.color_palette(self.palette_seq, len(serie))
        )

        # Formato común
        self.configurar_ejes(
            ax,
            titulo=titulo,
            xlabel=xlabel,
            ylabel=ylabel
        )

        # Anotaciones (ya tienes función reutilizable 👌)
        self.anotar_barras_horizontales(ax)

        plt.tight_layout()
        plt.show()

    def overtime_bajas(
        self,
        overtime_col="Over_Time",
        attrition_col="Attrition_num",
        figsize=(6, 4),
        excluir_valores="Unknown"):
        """
        Analiza la distribución de Over Time entre quienes abandonan la empresa.
        """
        df_bajas = self.dataframe[self.dataframe[attrition_col] == 1].copy()

        if excluir_valores is not None:
            if isinstance(excluir_valores, list):
                df_bajas = df_bajas[~df_bajas[overtime_col].isin(excluir_valores)]
            else:
                df_bajas = df_bajas[df_bajas[overtime_col] != excluir_valores]

        df_plot = df_bajas[overtime_col].value_counts(normalize=True) * 100
        df_plot = df_plot.reset_index()
        df_plot.columns = [overtime_col, "Percentage"]

        plt.figure(figsize=figsize)

        ax = sns.barplot(
            data=df_plot,
            x=overtime_col,
            y="Percentage",
            palette=sns.color_palette(self.palette_seq, len(df_plot)))

        self.configurar_ejes(
            ax,
            titulo="Overtime Distribution among Leavers (%)",
            xlabel="Over Time",
            ylabel="Percentage (%)")

        self.anotar_barras_verticales(ax)

        plt.tight_layout()
        plt.show()

    # 3. INGRESOS Y JOB LEVEL

    def boxplot_income_joblevel(
        self,
        x="Job_Level",
        y="Monthly_Income",
        hue="Attrition",
        figsize=(10, 6),
        palette=None):
        """
        Compara la distribución salarial según Job Level y Attrition.
        """
        if palette is None:
            palette = sns.color_palette(self.palette_seq, 2)

        plt.figure(figsize=figsize)

        ax = sns.boxplot(
            data=self.dataframe,
            x=x,
            y=y,
            hue=hue,
            palette=palette)

        self.configurar_ejes(
            ax,
            titulo="Monthly Income by Job Level and Attrition",
            xlabel="Job Level",
            ylabel="Monthly Income")

        ax.legend(title="Attrition")
        plt.tight_layout()
        plt.show()

    def boxplot_income_department(
        self,
        income_col="Monthly_Income",
        department_col="Department",
        joblevel_col="Job_Level",
        attrition_col="Attrition",
        niveles=None,
        hue_order=None,
        figsize=(12, 25),
        palette=None):
        """
        Crea un subplot por Job Level con la distribución salarial por Department segmentada por Attrition.
        """
        if niveles is None:
            niveles = sorted(self.dataframe[joblevel_col].dropna().unique())

        if hue_order is None:
            hue_order = ["No", "Yes"]

        if palette is None:
            palette = sns.color_palette(self.palette_seq, 2)

        fig, axes = plt.subplots(len(niveles), 1, figsize=figsize)

        if len(niveles) == 1:
            axes = [axes]

        for i, nivel in enumerate(niveles):
            df_nivel = self.dataframe[self.dataframe[joblevel_col] == nivel]

            sns.boxplot(
                data=df_nivel,
                x=income_col,
                y=department_col,
                hue=attrition_col,
                hue_order=hue_order,
                palette=palette,
                ax=axes[i])

            self.configurar_ejes(
                axes[i],
                titulo=f"Monthly Income by Department and Attrition - Job Level {nivel}",
                xlabel="Monthly Income",
                ylabel=""  )

            axes[i].legend(title="Attrition", loc="best")

        plt.tight_layout()
        plt.show()

    # 4. RELACIONES NUMÉRICAS

    def scatter_attrition(
        self,
        x,
        y,
        hue="Attrition",
        titulo=None,
        figsize=(10, 6),
        alpha=0.7,
        palette=None):
        """
        Scatterplot para analizar la relación entre dos variables numéricas segmentadas por Attrition.
        """
        if palette is None:
            palette = sns.color_palette(self.palette_seq, 2)

        plt.figure(figsize=figsize)

        ax = sns.scatterplot(
            data=self.dataframe,
            x=x,
            y=y,
            hue=hue,
            palette=palette,
            alpha=alpha)

        if titulo is None:
            titulo = f"{x.replace('_', ' ')} vs {y.replace('_', ' ')} by {hue.replace('_', ' ')}"

        self.configurar_ejes(
            ax,
            titulo=titulo,
            xlabel=x.replace("_", " "),
            ylabel=y.replace("_", " "))

        ax.legend(title=hue.replace("_", " "))
        plt.tight_layout()
        plt.show()

    # 5. SATISFACCIÓN Y ATTRITION

    def comparativa_satisfaccion(
        self,
        columnas_satisfaccion,
        attrition_col="Attrition",
        figsize=(10, 6),
        palette=None):
        """
        Compara la media global de variables de satisfacción entre quienes abandonan la empresa y quienes permanecen.
        """
        if palette is None:
            palette = sns.color_palette(self.palette_seq, 2)

        df_plot = (
            self.dataframe.groupby(attrition_col)[columnas_satisfaccion]
            .mean()
            .round(2)
            .reset_index())

        df_plot = df_plot.set_index(attrition_col).T.reset_index()
        df_plot.columns = ["Variable", "No", "Yes"]
        df_plot["Variable"] = df_plot["Variable"].str.replace("_", " ", regex=False)

        df_plot_melt = df_plot.melt(
            id_vars="Variable",
            var_name="Attrition",
            value_name="Score")

        plt.figure(figsize=figsize)

        ax = sns.barplot(
            data=df_plot_melt,
            y="Variable",
            x="Score",
            hue="Attrition",
            palette=palette)

        self.configurar_ejes(
            ax,
            titulo="Satisfaction Comparison: Leavers vs Stayers",
            xlabel="Average Score",
            ylabel="")

        ax.legend(title="Attrition")
        plt.tight_layout()
        plt.show()

    def heatmap_satisfaccion_departamento(
        self,
        columnas_satisfaccion,
        attrition_col="Attrition",
        department_col="Department",
        figsize=(10, 6),
        cmap="RdYlGn"):
        """
        Muestra la diferencia de satisfacción media por departamento entre quienes se quedan y quienes se van.
        """
        df_grouped = (
            self.dataframe.groupby([attrition_col, department_col])[columnas_satisfaccion]
            .mean()
            .round(2)
            .reset_index())

        df_no = (
            df_grouped[df_grouped[attrition_col] == "No"]
            .set_index(department_col)[columnas_satisfaccion])

        df_yes = (
            df_grouped[df_grouped[attrition_col] == "Yes"]
            .set_index(department_col)[columnas_satisfaccion])

        diferencia = (df_no - df_yes).round(2)
        diferencia.columns = [col.replace("_", " ") for col in diferencia.columns]

        plt.figure(figsize=figsize)

        ax = sns.heatmap(
            diferencia,
            annot=True,
            fmt=".2f",
            cmap=cmap,
            linewidths=0.5,
            cbar_kws={"label": "Difference in Average Score (No - Yes)"})

        self.configurar_ejes(
            ax,
            titulo="Satisfaction Gap by Department: Stayers vs Leavers",
            xlabel="",
            ylabel="")

        plt.tight_layout()
        plt.show()