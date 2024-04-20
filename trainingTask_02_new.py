import streamlit as st
import pandas as pd
import requests
from PIL import Image
from io import BytesIO, StringIO
from fpdf import FPDF


def fetch_image(url):
    """Fetch and save an image from a URL for PDF embedding."""
    try:
        response = requests.get(url)
        img = Image.open(BytesIO(response.content))
        img_path = '/tmp/temp_image.jpg'  # Temporary file path
        img.save(img_path, format='JPEG')
        return img_path
    except Exception as e:
        st.error(f"Failed to load image from {url}. Error: {e}")
        return None


class PDF(FPDF):
    def add_property(self, property_details):
        """Add a single property to the PDF, ensuring each starts on a new page."""
        self.add_page()
        self.set_font("Arial", 'B', 14)
        self.cell(0, 10, f"Address: {property_details['Address']}", 0, 1)
        self.set_font("Arial", size=12)
        self.cell(0, 10, f"Bedrooms: {property_details['Bedrooms']}, Bathrooms: {property_details['Bathrooms']}", 0, 1)
        self.cell(0, 10,
                  f"Living Area: {property_details['Living Area']} sqft, Lot Size: {property_details['Lot Size']}", 0,
                  1)
        self.cell(0, 10, f"Zestimate: ${property_details['Zestimate']}", 0, 1)

        if property_details['Image']:
            image_path = fetch_image(property_details['Image'])
            if image_path:
                self.image(image_path, x=10, y=self.get_y(), w=180)  # Adjust size and position as needed


def save_pdf(dataframe):
    pdf = PDF()
    for _, row in dataframe.iterrows():
        pdf.add_property(row)
    return pdf.output(dest='S').encode('latin1')  # Return PDF as byte stream


def display_data_with_images(dataframe):
    """Display data and images from the dataframe in Streamlit."""
    for index, row in dataframe.iterrows():
        st.subheader(f"{row['Address']}")
        st.write(f"Bedrooms: {row['Bedrooms']}, Bathrooms: {row['Bathrooms']}")
        st.write(f"Living Area: {row['Living Area']} sqft, Lot Size: {row['Lot Size']}")
        st.write(f"Zestimate: ${row['Zestimate']}")
        image = fetch_image(row['Image'])
        if image:
            st.image(image, width=300)


def main():
    st.title("Real Estate Properties Viewer")
    uploaded_file = st.file_uploader("Choose a CSV file", type="csv")
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        display_data_with_images(df)
        if st.button('Convert to PDF'):
            pdf_bytes = save_pdf(df)
            st.download_button(label="Download PDF", data=pdf_bytes, file_name="real_estate_details.pdf",
                               mime='application/pdf')


if __name__ == "__main__":
    main()
