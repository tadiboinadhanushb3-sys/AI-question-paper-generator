import streamlit as st
import PyPDF2
import random
import re
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

# ---------------------------------------------------------
# Page Configuration
# ---------------------------------------------------------

st.set_page_config(
    page_title="AI Question Paper Generator",
    page_icon="🧠",
    layout="wide"
)

st.title("🧠 AI Question Paper Generator")

# ---------------------------------------------------------
# Exam Details
# ---------------------------------------------------------

st.sidebar.header("Exam Information")

college = st.sidebar.text_input("College / University Name", "RAMACHANDRA COLLEGE OF ENGINEERING")
subject = st.sidebar.text_input("Subject Name", "Artificial Intelligence")
time = st.sidebar.text_input("Exam Duration", "3 Hours")
marks = st.sidebar.text_input("Maximum Marks", "70")

# ---------------------------------------------------------
# Question Configuration
# ---------------------------------------------------------

st.sidebar.header("Question Settings")

mcq_count = st.sidebar.number_input("Number of MCQs", 1, 15, 10)
short_count = st.sidebar.number_input("Short Answer Questions", 1, 6, 5)
difficulty_count = st.sidebar.number_input("Long Questions", 1, 6, 5)

# ---------------------------------------------------------
# Topic Input
# ---------------------------------------------------------

st.subheader("Provide Syllabus Topics")

method = st.radio(
    "Select Input Method",
    ["Manual Input", "Upload PDF"]
)

topics = []

if method == "Manual Input":

    text = st.text_area("Enter topics separated by comma")

    if text:
        topics = re.split(",|\n", text)

elif method == "Upload PDF":

    pdf_file = st.file_uploader("Upload PDF", type=["pdf"])

    if pdf_file:

        reader = PyPDF2.PdfReader(pdf_file)

        text = ""

        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text

        topics = re.split(",|\n", text)

        st.success("PDF Loaded Successfully")

topics = [t.strip() for t in topics if t.strip()]

# ---------------------------------------------------------
# Question Generation (Different Structures)
# ---------------------------------------------------------

def generate_mcq(topic):

    templates = [
        f"What is the main purpose of {topic}?",
        f"Which statement best describes {topic}?",
        f"What is a key feature of {topic}?",
        f"In AI systems, what role does {topic} play?",
        f"Which of the following is related to {topic}?"
    ]

    question = random.choice(templates)

    correct = f"{topic} improves system intelligence"

    distractors = [
        f"{topic} removes the need for algorithms",
        f"{topic} is unrelated to artificial intelligence",
        f"{topic} is only used in hardware design"
    ]

    options = distractors + [correct]
    random.shuffle(options)

    return question, options


def generate_short(topic):

    templates = [
        f"Define {topic}.",
        f"Explain the concept of {topic}.",
        f"Write a short note on {topic}.",
        f"What are the applications of {topic}?",
        f"State the importance of {topic} in Artificial Intelligence."
    ]

    return random.choice(templates)


def generate_long(topic):

    templates = [
        f"Explain the working principle of {topic} with suitable examples.",
        f"Discuss the advantages and limitations of {topic}.",
        f"Describe the architecture and applications of {topic}.",
        f"Analyze how {topic} contributes to intelligent systems.",
        f"Explain the role of {topic} in modern AI technologies."
    ]

    return random.choice(templates)

# ---------------------------------------------------------
# PDF Generator
# ---------------------------------------------------------

def create_pdf(text):

    buffer = BytesIO()

    pdf = canvas.Canvas(buffer, pagesize=letter)

    width, height = letter
    y = height - 40

    for line in text.split("\n"):

        pdf.drawString(40, y, line)

        y -= 18

        if y < 40:
            pdf.showPage()
            y = height - 40

    pdf.save()
    buffer.seek(0)

    return buffer

# ---------------------------------------------------------
# Generate Question Paper
# ---------------------------------------------------------

if st.button("Generate Question Paper"):

    if not topics:
        st.error("Please provide syllabus topics")

    else:

        output = ""

        header = f"""
{college}
Subject: {subject}

Time: {time}        Max Marks: {marks}

------------------------------------------------------------
"""

        st.text(header)
        output += header

        # SECTION A
        st.subheader("SECTION A – MCQs (1 Mark Each)")
        output += "\nSECTION A – MCQs (1 Mark Each)\n"

        for i in range(mcq_count):

            topic = random.choice(topics)
            q, options = generate_mcq(topic)

            st.write(f"Q{i+1}. {q}")
            output += f"\nQ{i+1}. {q}\n"

            for j, op in enumerate(options):

                st.write(f"{chr(65+j)}. {op}")
                output += f"{chr(65+j)}. {op}\n"

        # SECTION B
        st.subheader("SECTION B – Short Answer (2 Marks Each)")
        output += "\nSECTION B – Short Answer (2 Marks Each)\n"

        for i in range(short_count):

            topic = random.choice(topics)
            q = generate_short(topic)

            st.write(f"Q{i+1}. {q}")
            output += f"\nQ{i+1}. {q}\n"

        # SECTION C
        st.subheader("SECTION C – Long Answer (10 Marks Each)")
        output += "\nSECTION C – Long Answer. (10 Marks Each)\n"

        for i in range(difficulty_count):

            topic = random.choice(topics)
            q = generate_long(topic)

            st.write(f"Q{i+1}. {q}")
            output += f"\nQ{i+1}. {q}\n"

        # Download Options
        st.subheader("Download Question Paper")

        st.download_button(
            "Download as TXT",
            output.encode("utf-8"),
            "question_paper.txt"
        )

        st.download_button(
            "Download as PDF",
            create_pdf(output),
            "question_paper.pdf"
        )
        st.balloons()
        st.success("Question Paper Generated Successfully!")