# Import necessary modules for environment variable loading, OpenAI API interaction, PDF reading, and Gradio UI
from dotenv import load_dotenv
from openai import OpenAI
from pypdf import PdfReader
import gradio as gr


# Load environment variables, overwriting any existing ones
load_dotenv(override=True)
# Initialize OpenAI client
openai = OpenAI()

# Read and extract all text from LinkedIn PDF profile
reader = PdfReader("me/Linkedin_Devesh.pdf")
linkedin = ""
for page in reader.pages:
    text = page.extract_text()  # Extract text from each PDF page
    if text:
        linkedin += text  # Concatenate extracted text

#print(linkedin)  # Output the extracted LinkedIn text to the console

# Read and extract all text from Resume PDF
resume_reader = PdfReader("me/Resume_Devesh.pdf")
resume = ""
for page in resume_reader.pages:
    text = page.extract_text()  # Extract text from each resume page
    if text:
        resume += text  # Concatenate extracted text

# Load summary from a local file
with open("me/summary_Devesh.txt", "r", encoding="utf-8") as summary_file:
    summary = summary_file.read()


name = "Devesh Sonpure"

system_prompt = f"You are acting as {name}. You are answering questions on {name}'s website, \
particularly questions related to {name}'s career, background, skills and experience. \
Your responsibility is to represent {name} for interactions on the website as faithfully as possible. \
You are given a summary of {name}'s background and LinkedIn profile and {name}'s resume which you can use to answer questions. \
Be professional and engaging, as if talking to a potential client or future employer who came across the website. \
If you don't know the answer, say so. Make sure all your answers are strictly within the scope of professional details only. \
All the answers related to experience should be strictly from the job experience mentioned in these resources only. \
if you do not get the required information within the provided resources, politely inform that you are not sure about it."

system_prompt += f"\n\n## Summary:\n{summary}\n\n## LinkedIn Profile:\n{linkedin}\n\n## Resume:\n{resume}\n\n"
system_prompt += f"With this context, please chat with the user, always staying in character as {name}."

def chat(message, history):
    messages = [{"role": "system", "content": system_prompt}] + history + [{"role": "user", "content": message}]
    response = openai.chat.completions.create(model="gpt-4o-mini", messages=messages)
    return response.choices[0].message.content

gr.ChatInterface(chat, type="messages").launch()

