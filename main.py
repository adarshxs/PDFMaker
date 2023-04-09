import streamlit as st
from fpdf import FPDF
from PIL import Image
import base64
import os
from pygments import highlight
from pygments.lexers import PythonLexer
from pygments.formatters import ImageFormatter

formatter = ImageFormatter()

st.set_page_config(page_title='PDFMaker', page_icon=':memo:', layout='wide')

with st.sidebar:
    st.sidebar.image("logo.png", use_column_width=True)
    st.write("Simplifies your Moodle ➡️ Vtop process. Use this to simplify generating PDF's for your Moodle assignments.")
    st.warning("This app is still in development. Please report any bugs or issues.")
    st.write("Follow me on Instagram [@adarsh.py](https://www.instagram.com/adarsh.py/)!")
    st.info("Contribute here! [GitHub](https://github.com/adarshxs/PDFMaker)")
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
question_images = []
output_images = []
for i, _ in enumerate(range(int(number))):
    st.write(f'Question {i+1}')
    question_code_output = st.beta_columns([2, 3, 2])
    with question_code_output[0]:
        question_image = st.file_uploader(f'Upload question image for question {i+1}', type=['jpg', 'jpeg', 'png'])
        if question_image is not None:
            with Image.open(question_image) as img:
                img = img.convert('RGB')
                question_images.append(img)
    with question_code_output[1]:
        code_input = st.text_area(f'Paste code for question {i+1}')
        if code_input:
            code_inputs.append(code_input)
    with question_code_output[2]:
        output_image = st.file_uploader(f'Upload output image for question {i+1}', type=['jpg', 'jpeg', 'png'])
        if output_image is not None:
            with Image.open(output_image) as img:
                img = img.convert('RGB')
                output_images.append(img)
        st.write("---")

# Save the question and output images to disk
import os
from contextlib import contextmanager
from fpdf import FPDF
from pygments import highlight
from pygments.formatters import ImageFormatter
from pygments.lexers import PythonLexer
from PIL import Image

@contextmanager
def open_image(filename):
    with Image.open(filename) as img:
        yield img

def save_image_to_file(image, prefix):
    with open(f"{prefix}.png", "wb") as f:
        image.save(f, format="png")

def generate_temp_filenames(prefix, count):
    return [f"{prefix}_{i}.png" for i in range(count)]

question_temp_filenames = generate_temp_filenames("temp_question", len(question_images))
output_temp_filenames = generate_temp_filenames("temp_output", len(output_images))
code_temp_filenames = generate_temp_filenames("temp_code", len(code_inputs))

for i, img in enumerate(question_images):
    img.save(question_temp_filenames[i], format="png")
for i, img in enumerate(output_images):
    img.save(output_temp_filenames[i], format="png")
for i, code in enumerate(code_inputs):
    with open_image(code) as img:
        formatter = ImageFormatter(font_name="DejaVu Sans Mono", line_numbers=True)
        highlighted_img = highlight(code, PythonLexer(), formatter).get_image()
        save_image_to_file(highlighted_img, code_temp_filenames[i])

# Create a formatter for the code highlighting
formatter = ImageFormatter(font_name='DejaVu Sans Mono', fontsize=12, line_numbers=True)

# Define the PDF document
pdf = FPDF()

# Add a new page for the document
pdf.add_page()

# Set the font for the document
pdf.set_font('Arial', '', 12)

# Add the name, registration number, and assignment name as a heading
pdf.cell(0, 20, f"{name} - {reg_num}", 0, 1, 'C')
pdf.cell(0, 10, f"{ass_name}", 0, 1, 'C')

# Add a blank line
pdf.cell(0, 10, '', 0, 1)

# Add the body text
pdf.cell(0, 20, f"{text_in}", 0, 1, 'C')

# Iterate over the questions
for i in range(int(number)):
    # Add a new page for the question
    pdf.add_page()
    
    # Set the font for the question
    pdf.set_font("Arial", size=12)
    
    # Set the y offset for the images
    y_offset = 30

    # Add the question number and the label for the code and output
    pdf.cell(200, 10, txt=f"Q{i+1})", ln=1, align='L')
    pdf.cell(200, 10, txt="Code & Output:", ln=1, align='L')

    # Add the question image if it exists
    if i < len(question_images):
        img = Image.open(question_images[i])
        append_temp_image(img, code_inputs)
        width, height = img.size
        pdf.image(code_inputs[-1], x=10, y=y_offset, w=100)
        y_offset += height * (100 / width) + 10

    # Add the code and output images if they exist
    if i < len(code_inputs):
        img = Image.open(code_inputs[i])
        width, height = img.size
        pdf.image(code_inputs[i], x=10, y=y_offset, w=100)
        y_offset += height * (100 / width) + 10

    if i < len(output_images):
        img = Image.open(output_images[i])
        append_temp_image(img, code_inputs)
        width, height = img.size
        pdf.image(code_inputs[-1], x=10, y=y_offset, w=100)
        y_offset += height * (100 / width) + 10

    # Check if the y offset exceeds the page height
    if y_offset > pdf.w - 20:
        pdf.add_page()  # add a new page
        y_offset = 30  # reset y_offset

    # Close the images and delete the temporary files
    if i < len(question_images):
        os.remove(code_inputs[-1])
    if i < len(output_images):
        os.remove(code_inputs[-1])

pdf.output(f"code_submission.pdf")

#changes

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
        
