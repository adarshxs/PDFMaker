import streamlit as st
from fpdf import FPDF
from PIL import Image
import base64
import os
from pygments import highlight
from pygments.lexers import PythonLexer
from pygments.formatters import ImageFormatter

st.set_page_config(page_title='Code Submission', page_icon=':memo:', layout='wide')

with st.sidebar:
    st.sidebar.image("logo.png", use_column_width=True)
    st.write("Simplifies your Moodle ➡️ Vtop process. Use this to simplify generating PDF's for your Moodle assignments.")
    st.warning("This app is still in development. Please report any bugs or issues.")
    st.write("Follow me on Instagram [@adarsh.py](https://www.instagram.com/adarsh.py/)!")
    st.info("[Compress](https://www.ilovepdf.com/compress_pdf) your generated pdf's here!", icon="📄")
    st.write("")

st.title('Code Submission')

name = st.text_input('Enter your name')
reg_num = st.text_input('Enter your registration number')
ass_name = st.text_input('Enter assignment name')
text_in = st.text_area('Enter anything you want to be printed on the first page: ')

number = st.number_input('Insert the number of questions', step=1, min_value=1)

question_images = []
code_inputs = []
output_images = []

st.write("---")
for i in range(int(number)):
    st.write(f'Question {i+1}')
    question_image = st.file_uploader(f'Upload question image for question {i+1}', type=['jpg', 'jpeg', 'png'])
    if question_image is not None:
        img = Image.open(question_image)
        img = img.convert('RGB') # convert image to RGB format
        img.save(f'temp_question_{i}.png', format='png') # save image as a PNG file
        question_images.append(f'temp_question_{i}.png')
    code_input = st.text_area(f'Paste code for question {i+1}')
    if code_input:
        code_inputs.append(code_input)
    output_image = st.file_uploader(f'Upload output image for question {i+1}', type=['jpg', 'jpeg', 'png'])
    if output_image is not None:
        img = Image.open(output_image)
        img = img.convert('RGB') # convert image to RGB format
        img.save(f'temp_output_{i}.png', format='png') # save image as a PNG file
        output_images.append(f'temp_output_{i}.png')
    st.write("---")

pdf = FPDF()

pdf.add_page()

pdf.set_font('Arial', 'B', 16)

# Add the name, registration number, and assignment name as a heading
pdf.cell(0, 20, f"{name} - {reg_num}", 0, 1, 'C')
pdf.cell(0, 10, f"{ass_name}", 0, 1, 'C')

# Add a blank line
pdf.cell(0, 10, '', 0, 1)

# Reset font and size for the body text
pdf.set_font('Arial', '', 12)
pdf.cell(0, 20, f"{text_in}", 0, 1, 'C')

for i in range(int(number)):
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    y_offset = 30

    pdf.cell(200, 10, txt=f"Q{i+1})", ln=1, align='L')
    pdf.cell(200, 10, txt="Code & Output:", ln=1, align='L')

    if i < len(question_images):
        img = Image.open(question_images[i])
        width, height = img.size
        pdf.image(question_images[i], x=10, y=y_offset, w=100)
        y_offset += height * (100 / width) + 10
    if i < len(code_inputs):
        with open(f'temp_code_{i}.png', 'wb') as f:
            f.write(highlight(code_inputs[i], PythonLexer(), ImageFormatter()))
        img = Image.open(f'temp_code_{i}.png')
        width, height = img.size
        pdf.image(f'temp_code_{i}.png', x=10, y=y_offset, w=100)
        y_offset += height * (100 / width) + 10
    if i < len(output_images):
        img = Image.open(output_images[i])
        width, height = img.size
        pdf.image(output_images[i], x=10, y=y_offset, w=100)
        y_offset += height * (100 / width) + 10
        img.close()
pdf.output(f"code_submission.pdf")

def generate_pdf():
    # code to generate the PDF file
    with open(f"code_submission.pdf", "rb") as f:
        bytes = f.read()
        b64 = base64.b64encode(bytes).decode()
        href = f'<a href="data:application/octet-stream;base64,{b64}" download="code_submission.pdf">Download PDF</a>'
        st.markdown(href, unsafe_allow_html=True)

if st.button('Generate PDF'):
    generate_pdf()
    for i in range(int(number)):
        if os.path.exists(f'temp_question_{i}.png'):
            os.remove(f'temp_question_{i}.png')
        if os.path.exists(f'temp_code_{i}.png'):
            os.remove(f'temp_code_{i}.png')
        if os.path.exists(f'temp_output_{i}.png'):
            os.remove(f'temp_output_{i}.png')
        


