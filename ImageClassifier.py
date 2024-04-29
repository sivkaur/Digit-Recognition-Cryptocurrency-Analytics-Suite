import streamlit as st
from PIL import Image, ImageOps, ImageEnhance
from tensorflow.keras.models import load_model
import numpy as np
import os

# Set page configuration
st.set_page_config(page_title='NumeralNet - Digit Recognition Suite', layout='wide')

# Get the path of the directory where the script is located
current_script_dir = os.path.dirname(os.path.abspath(__file__))

# Function to load and return the trained model
def load_your_model():
    # Change the current working directory to the script directory
    os.chdir(current_script_dir)

    # Replace the path with your actual model path
    model_path = 'mnist_digit_model.h5'

    # Check if the model file exists in the script directory
    if os.path.isfile(model_path):
        model = load_model(model_path)
    else:
        st.error('Model file not found. Please ensure it is located in the script directory.')
        model = None

    return model

# Load your model
model = load_your_model()

st.title("NumeralNet - Digit Recognition Suite")

st.write("Upload a digit image, and NumeralNet will identify the digit.")

# File uploader allows user to add their own image
uploaded_file = st.file_uploader("Choose an image...", type=["png", "jpg", "jpeg"])


def preprocess_image(image):
    # If image is RGBA, convert to RGB first to remove alpha channel
    if image.mode == 'RGBA':
        # Create a white rgba background
        new_image = Image.new("RGBA", image.size, "WHITE")
        new_image.paste(image, (0, 0), image)
        image = new_image.convert('RGB')

    # Convert to grayscale
    image = ImageOps.grayscale(image)

    # Resize the image to 28x28
    image = image.resize((28, 28), Image.Resampling.LANCZOS)

    # Invert image colors so digit is white and background is black
    image = ImageOps.invert(image)

    # Normalize the image
    image_array = np.array(image).astype(np.float32) / 255.0

    # Add a channel dimension
    image_array = np.expand_dims(image_array, axis=-1)

    # Make sure we have a 4D batch tensor
    image_array = np.expand_dims(image_array, axis=0)

    return image_array


if uploaded_file is not None:
    # Load and display the uploaded image
    image = Image.open(uploaded_file)
    st.image(image, caption='Uploaded Image', use_column_width=True)

    # Preprocess the image
    processed_image = preprocess_image(image)

    st.write("Classifying...")

    # Make a prediction
    prediction = model.predict(processed_image)
    predicted_class = np.argmax(prediction, axis=1)
    confidence = np.max(prediction, axis=1)

    # Display the prediction and the confidence
    st.subheader(f'Predicted digit: {predicted_class[0]} with confidence: {confidence[0]:.2f}')
else:
    st.write("Please upload an image.")
