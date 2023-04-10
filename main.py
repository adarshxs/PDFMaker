import streamlit as st
from fpdf import FPDF
from PIL import Image
import base64
import os
from pygments import highlight
from pygments.lexers import PythonLexer
from pygments.formatters import ImageFormatter

st.set_page_config(page_title='PDFMaker', page_icon=':memo:', layout='wide')

with st.sidebar:
    st.sidebar.image("logo.png", use_column_width=True)
    st.write("Simplifies your Moodle ➡️ Vtop process. Use this to simplify generating PDF's for your Moodle assignments.")
    st.warning("This app is still in development. Please report any bugs or issues.")
    st.write("Follow me on Instagram [@adarsh.py](https://www.instagram.com/adarsh.py/)!")
    st.info("Contribute here! [GitHub](https://github.com/adarshxs/PDFMaker)")
    st.info("[Compress](https://www.ilovepdf.com/compress_pdf) your generated pdf's here!", icon="📄")
    
    st.write("")


st.title('PDF Maker')

name = st.text_input('Enter your name')
reg_num = st.text_input('Enter your registration number')
ass_name = st.text_input('Enter assignment name')
text_in = st.text_area('Enter anything you want to be printed on the first page: ')
number = st.number_input('Insert the number of questions', step=1, min_value=1)

col1, col2= st.columns(2)
with col1:
    theme = st.selectbox(
    'Choose a theme!',
    ('default', 'github-dark', 'sas', 'rrt', 'rainbow_dash', 'stata-light', 'gruvbox-light', 'gruvbox-light', 'monokai', 'vim', 'inkpot'))
   

with col2:
    image_url = f'data:image/jpeg;base64,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'
    st.image(image_url)
   

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

# set minimum line length for code inputs else shit blows up
min_line_length = 40 
for i in range(len(code_inputs)):
    code_lines = code_inputs[i].split('\n')
    max_line_length = max(len(line) for line in code_lines)
    if max_line_length < min_line_length:
        padding = ' ' * (min_line_length - max_line_length)
        code_inputs[i] = '\n'.join(line + padding for line in code_lines)

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

page_width = pdf.w
max_image_width = page_width * 0.8 # set maximum image width to 80% of page width


for i in range(int(number)):
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    y_offset = 30

    pdf.cell(200, 10, txt=f"Q{i+1})", ln=1, align='L')
    pdf.cell(200, 10, txt="Code & Output:", ln=1, align='L')

    if i < len(question_images):
        img = Image.open(question_images[i])
        width, height = img.size
        image_width = min(max_image_width, width) # set image width to the smaller of max_image_width and original image width
        X = (page_width - image_width) / 2
        pdf.image(question_images[i], x=X, y=y_offset, w=image_width)
        page_height = pdf.h
        padding = page_height * 0.15
        y_offset += height * (100 / width) + padding
        img.close()
    if i < len(code_inputs):
        formatter = ImageFormatter(style=theme)
        with open(f'temp_code_{i}.png', 'wb') as f:
            f.write(highlight(code_inputs[i], PythonLexer(), formatter))
        img = Image.open(f'temp_code_{i}.png')
        width, height = img.size
        image_width = min(max_image_width, width) # set image width to the smaller of max_image_width and original image width
        X = (page_width - image_width) / 2
        pdf.image(f'temp_code_{i}.png', x=X, y=y_offset, w=image_width)
        y_offset += height * (100 / width) + padding
        img.close()
        os.remove(f'temp_code_{i}.png')
    if  y_offset > pdf.w - 20: # check if y_offset exceeds page height
        pdf.add_page() # add a new page
        y_offset = 30 # reset y_offset
    if i < len(output_images):
        img = Image.open(output_images[i])
        width, height = img.size
        image_width = min(max_image_width, width) # set image width to the smaller of max_image_width and original image width
        X = (page_width - image_width) / 2
        pdf.image(output_images[i], x=X, y=y_offset, w=image_width)
        y_offset += height * (100 / width) + 10
        img.close()

pdf.output(f"code_submission.pdf")

#changes

def generate_pdf():
    # code to generate the PDF file
    with open(f"code_submission.pdf", "rb") as f:
        base64_pdf = base64.b64encode(f.read()).decode('utf-8')
        pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="800" height="800" type="application/pdf"></iframe>'
        st.markdown(pdf_display, unsafe_allow_html=True)

if st.button('Generate PDF'):
    generate_pdf()
    for i in range(int(number)):
        if os.path.exists(f'temp_question_{i}.png'):
            os.remove(f'temp_question_{i}.png')
        if os.path.exists(f'temp_code_{i}.png'):
            os.remove(f'temp_code_{i}.png')
        if os.path.exists(f'temp_output_{i}.png'):
            os.remove(f'temp_output_{i}.png')
        
