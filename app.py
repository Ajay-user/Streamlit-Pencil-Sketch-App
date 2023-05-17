# attr: Michael Beyeler
import cv2
from PIL import Image
import requests
import numpy as np
import matplotlib.pyplot as plt
import streamlit as st

def compare_image(img, final_img):
        image, final_image = Image.fromarray(img), Image.fromarray(final_img)
        compare_img =  Image.new('RGB', (image.width + final_image.width, image.height))
        compare_img.paste(image, (0,0))
        compare_img.paste(final_image, (image.width,0))
        return np.array(compare_img)


st.title('✏ Pencil Sketch 🖌')
st.caption('Do you want to create pencil sketch of your portrait ?')


with st.sidebar:
    tab1, tab2 = st.tabs(['URL', 'Upload'])
    with tab1:
        image_url = st.text_input(label="Enter the image url", value="https://images.unsplash.com/photo-1494790108377-be9c29b29330?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=387&q=80")
    with tab2:
        image_upload = st.file_uploader(label="Upload your image", type=['png', 'jpg', 'jpeg'])
    compare = st.checkbox(label="Compare image and result", value=True)


image = None
if image_upload:
    image = Image.open(image_upload)
elif image_url:
    image = Image.open(requests.get(url=image_url, stream=True).raw)

if image:
    image = np.array(image)
    img_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    img_invert = cv2.bitwise_not(img_gray)
    img_smoothing = cv2.GaussianBlur(img_invert, (21, 21), sigmaX=0, sigmaY=0)
    final_image = cv2.divide(img_gray, 255 - img_smoothing, scale=256)

    if compare:
         final_image = compare_image(image, final_image)

    fig, ax = plt.subplots(nrows=1, ncols=1)
    ax.imshow(final_image, cmap='gray')
    ax.axis(False)
    st.pyplot(fig=fig, use_container_width=True)




# @book{OpenCVWithPythonBlueprints,
# 	title = {{OpenCV with Python Blueprints}},
# 	subtitle = {Design and develop advanced computer vision projects using {OpenCV} with {Python}},
# 	author = {Michael Beyeler},
# 	year = {2015},
# 	pages = {230},
# 	publisher = {Packt Publishing Ltd.},
# 	isbn = {978-178528269-0}
# }