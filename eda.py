import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.title("📊 Simple EDA App")

# =========================
# a.) File Upload (CSV + Excel)
# =========================
uploaded_file = st.file_uploader(
    "Upload CSV or Excel file",
    type=["csv", "xlsx"]
)

if uploaded_file is not None:
    try:
        file_name = uploaded_file.name

        if file_name.endswith(".csv"):
            data = pd.read_csv(uploaded_file)
            st.success("✅ CSV file uploaded")

        elif file_name.endswith(".xlsx"):
            data = pd.read_excel(uploaded_file)
            st.success("✅ Excel file uploaded")

        else:
            st.error("❌ Unsupported file type")
            st.stop()

        # =========================
        # Preview Data
        # =========================
        st.subheader("👀 Data Preview")
        st.dataframe(data)

        # =========================
        # Basic Info
        # =========================
        st.subheader("📌 Dataset Info")
        st.write(f"Rows: {data.shape[0]}")
        st.write(f"Columns: {data.shape[1]}")

        # =========================
        # Numerical Summary
        # =========================
        st.subheader("🔢 Numerical Summary")
        st.dataframe(data.describe())

        # =========================
        # b.) Non-Numerical Summary (SAFE CHECK)
        # =========================
        non_numeric = data.select_dtypes(include=['object', 'bool'])

        if not non_numeric.empty:
            st.subheader("🔤 Non-Numerical Summary")
            st.dataframe(non_numeric.describe())
        else:
            st.info("ℹ️ No non-numerical features found in this dataset")

        # =========================
        # c.) More Graphs
        # =========================
        st.subheader("📈 Visualizations")

        numeric_cols = data.select_dtypes(include='number').columns

        if len(numeric_cols) > 0:
            selected_col = st.selectbox(
                "Choose a column for visualization",
                numeric_cols
            )

            # Histogram
            st.write("### Histogram 📊")
            fig, ax = plt.subplots()
            data[selected_col].hist(ax=ax)
            st.pyplot(fig)

            # Boxplot
            st.write("### Boxplot 📦")
            fig, ax = plt.subplots()
            data.boxplot(column=selected_col, ax=ax)
            st.pyplot(fig)

        # Scatter Plot (if more than 1 numeric column)
        if len(numeric_cols) > 1:
            st.write("### Scatter Plot 🔵")
            col1 = st.selectbox("X-axis", numeric_cols, key="x")
            col2 = st.selectbox("Y-axis", numeric_cols, key="y")

            fig, ax = plt.subplots()
            ax.scatter(data[col1], data[col2])
            ax.set_xlabel(col1)
            ax.set_ylabel(col2)
            st.pyplot(fig)

    except Exception as e:
        st.error(f"⚠️ Error: {e}")