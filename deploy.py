import streamlit as st
from PIL import Image
import tensorflow as tf
import numpy as np

model = tf.keras.models.load_model('Model.h5')

def preprocess_image(image):
    image = image.resize((32,32))  
    img_array = np.array(image)
    img_array = img_array/255
    return img_array

def predict(image):
    processed_image = preprocess_image(image)
    test = []
    test.append(processed_image)
    test = np.array(test)
    pred = model.predict(test)
    ind = np.argmax(pred[0])
    if(ind==0):
        return ("AI generated Image")
    elif(ind==1):
        return("REAL Image")

def main():
    st.title('AI vs REAL Image Classifier')
    pages = ['Home', 'Predictor']
    selected_page = st.sidebar.radio('Select a page', pages)

    if selected_page == 'Home':
        st.header('Welcome to the AI Image Classifier!')
        st.write('This app allows you to classify images as real or AI generated.')

    elif selected_page == 'Predictor':
        st.header('Image Predictor')
        uploaded_file = st.file_uploader('Upload an image', type=['jpg', 'jpeg', 'png'])

        if uploaded_file is not None:
            image = Image.open(uploaded_file)
            st.image(image, caption='Uploaded Image', use_column_width=True)
            st.write('')

            if st.button('Predict'):
                label = predict(image)
                st.write(f'Prediction: {label}')

if __name__ == '__main__':
    main()
