import streamlit as st
import plotly.express as px

def show_visualization(df, numeric_columns, categorical_columns):

    st.subheader("📊 Data Visualizations")

    chart_type = st.selectbox(
        "Select Chart Type",
        [
            "Histogram",
            "Box Plot",
            "Scatter Plot",
            "Line Chart",
            "Area Chart",
            "Bar Chart",
            "Pie Chart",
            "Heatmap",
            "Violin Plot",
            "Bubble Chart"
        ]
    )

    # ---------------- HISTOGRAM ----------------
    if chart_type == "Histogram":

        if len(numeric_columns) == 0:
            st.warning("No numeric columns available")
            return

        col = st.selectbox("Select Column", numeric_columns)

        fig = px.histogram(df, x=col, nbins=30, title=f"{col} Distribution")
        st.plotly_chart(fig, use_container_width=True)

    # ---------------- BOX PLOT ----------------
    elif chart_type == "Box Plot":

        if len(numeric_columns) == 0:
            st.warning("No numeric columns available")
            return

        col = st.selectbox("Select Column", numeric_columns)

        fig = px.box(df, y=col, title=f"{col} Box Plot")
        st.plotly_chart(fig, use_container_width=True)

    # ---------------- SCATTER ----------------
    elif chart_type == "Scatter Plot":

        if len(numeric_columns) < 2:
            st.warning("Need at least 2 numeric columns")
            return

        x_col = st.selectbox("X Axis", numeric_columns)
        y_col = st.selectbox("Y Axis", numeric_columns)

        fig = px.scatter(df, x=x_col, y=y_col, title="Scatter Plot")
        st.plotly_chart(fig, use_container_width=True)

    # ---------------- LINE CHART ----------------
    elif chart_type == "Line Chart":

        if len(numeric_columns) == 0:
            st.warning("No numeric columns available")
            return

        col = st.selectbox("Select Column", numeric_columns)

        fig = px.line(df, y=col, title=f"{col} Trend")
        st.plotly_chart(fig, use_container_width=True)

    # ---------------- AREA CHART ----------------
    elif chart_type == "Area Chart":

        if len(numeric_columns) == 0:
            st.warning("No numeric columns available")
            return

        col = st.selectbox("Select Column", numeric_columns)

        fig = px.area(df, y=col, title=f"{col} Area Chart")
        st.plotly_chart(fig, use_container_width=True)

    # ---------------- BAR CHART ----------------
    elif chart_type == "Bar Chart":

        if len(categorical_columns) == 0:
            st.warning("No categorical columns available")
            return

        col = st.selectbox("Select Column", categorical_columns)

        bar_data = df[col].value_counts().reset_index()
        bar_data.columns = [col, "Count"]

        fig = px.bar(bar_data, x=col, y="Count", title=f"{col} Distribution")
        st.plotly_chart(fig, use_container_width=True)

    # ---------------- PIE CHART ----------------
    elif chart_type == "Pie Chart":

        if len(categorical_columns) == 0:
            st.warning("No categorical columns available")
            return

        col = st.selectbox("Select Column", categorical_columns)

        pie_data = df[col].value_counts().reset_index()
        pie_data.columns = [col, "Count"]

        fig = px.pie(pie_data, names=col, values="Count", title=f"{col} Distribution")
        st.plotly_chart(fig, use_container_width=True)

    # ---------------- HEATMAP ----------------
    elif chart_type == "Heatmap":

        if len(numeric_columns) < 2:
            st.warning("Need at least 2 numeric columns")
            return

        corr = df[numeric_columns].corr()

        fig = px.imshow(
            corr,
            text_auto=True,
            color_continuous_scale="RdBu_r",
            title="Correlation Heatmap"
        )

        st.plotly_chart(fig, use_container_width=True)

    # ---------------- VIOLIN PLOT ----------------
    elif chart_type == "Violin Plot":

        if len(numeric_columns) == 0:
            st.warning("No numeric columns available")
            return

        num_col = st.selectbox("Numeric Column", numeric_columns)

        if len(categorical_columns) > 0:
            cat_col = st.selectbox("Category Column", categorical_columns)
            fig = px.violin(df, x=cat_col, y=num_col, box=True, points="all")
        else:
            fig = px.violin(df, y=num_col, box=True, points="all")

        st.plotly_chart(fig, use_container_width=True)

    # ---------------- BUBBLE CHART ----------------
    elif chart_type == "Bubble Chart":

        if len(numeric_columns) < 3:
            st.warning("Need at least 3 numeric columns")
            return

        x_col = st.selectbox("X Axis", numeric_columns)
        y_col = st.selectbox("Y Axis", numeric_columns)
        size_col = st.selectbox("Size", numeric_columns)

        fig = px.scatter(
            df,
            x=x_col,
            y=y_col,
            size=size_col,
            title="Bubble Chart"
        )

        st.plotly_chart(fig, use_container_width=True)