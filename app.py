import streamlit as st
import pandas as pd
import pickle
from io import BytesIO

st.set_page_config(
    page_title="Full Size Streamlit App",
    layout="wide",  # Mengaktifkan mode lebar
    initial_sidebar_state="expanded",  # Sidebar tetap terbuka (opsional)
)

# Fungsi untuk melakukan prediksi
def predict(model, data):
    return model.predict(data)

# Tampilan di aplikasi Streamlit
st.title("Model Prediksi Kelayakan Promosi Karyawan")
st.write("Upload model (.pkl) dan file test.csv untuk melihat hasil prediksi.")

# Upload file model
uploaded_model = st.file_uploader("Upload Pickle Model", type="pkl")
if uploaded_model:
    model = pickle.load(uploaded_model)
    st.success("Model berhasil dimuat!")

# Upload file test.csv
uploaded_file = st.file_uploader("Upload Test CSV", type="csv")
if uploaded_file:
    test_data = pd.read_csv(uploaded_file)
    st.write("Data berhasil dimuat!")
    st.dataframe(test_data)

    # Jika model sudah diupload, lakukan prediksi
    if uploaded_model:
        with st.spinner("Sedang melakukan prediksi..."):
            predictions = predict(model, test_data)
            st.success("Prediksi selesai!")

            # Menambahkan hasil prediksi ke data
            test_data["Prediction"] = predictions
            st.write("Hasil Prediksi:")
            st.dataframe(test_data)

            # Tombol untuk mengunduh hasil prediksi
            output = BytesIO()
            with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
                test_data.to_excel(writer, index=False, sheet_name="Predictions")

            # Move the pointer to the beginning of the stream before downloading
            output.seek(0)

            st.download_button(
                label="Download Hasil Prediksi ke Excel",
                data=output.getvalue(),
                file_name="predictions.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )