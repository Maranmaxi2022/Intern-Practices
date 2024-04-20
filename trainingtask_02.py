import streamlit as st
import pandas as pd
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import io


def convert_df_to_pdf(df):
    """ Convert DataFrame to a PDF file. """
    pdf_buffer = io.BytesIO()
    c = canvas.Canvas(pdf_buffer, pagesize=letter)
    text = c.beginText(40, 750)
    text.setFont("Helvetica", 12)

    # Add CSV contents to PDF
    for index, row in df.iterrows():
        line = ', '.join(str(value) for value in row)
        text.textLine(line)

    c.drawText(text)
    c.showPage()
    c.save()
    pdf_buffer.seek(0)
    return pdf_buffer


def main():
    st.title('CSV to PDF Converter')

    # File uploader allows user to add their own CSV
    uploaded_file = st.file_uploader("Choose a CSV file", type="csv")
    if uploaded_file is not None:
        # Read CSV file with Pandas
        df = pd.read_csv(uploaded_file)
        st.write("Data Preview:", df.head())

        # Convert DataFrame to PDF
        result_pdf = convert_df_to_pdf(df)

        # Create download button for the PDF
        st.download_button(
            label="Download PDF",
            data=result_pdf,
            file_name="converted.pdf",
            mime="application/pdf"
        )


if __name__ == "__main__":
    main()
