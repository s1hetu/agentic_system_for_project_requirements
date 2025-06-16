import logging
import os
import watchtower
import boto3
import PyPDF2
import docx
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent
from markdown import markdown
import re
from bs4 import BeautifulSoup
from agents.constants import INSTRUCTIONS_PATH

load_dotenv()
openai_fastest_llm = ChatOpenAI(model="gpt-4.1-nano", api_key=os.environ.get('OPENAI_API_KEY'))

client = boto3.client(
    "logs",
    aws_access_key_id=os.environ.get('ACCESS_KEY'),
    aws_secret_access_key=os.environ.get('SECRET_KEY'),
    region_name=os.environ.get('REGION'),
)


def get_logger(name):
    """
    Logging mechanism for displaying log messages in AWS S3.
    :param name: Name of the logger
    :param use_client: Whether to use boto3 client
    :param log_group_name: Name of log_group
    :param log_stream_name: Stream of log_group
    :return:
    """
    log_formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(name)s - "
                                      "%(filename)s - %(funcName)s - %(lineno)s - %(message)s", )

    handler = logging.StreamHandler()
    handler.setFormatter(log_formatter)

    custom_logger = logging.getLogger(name)
    custom_logger.propagate = False
    custom_logger.setLevel(logging.INFO)
    custom_logger.addHandler(handler)

    # Add watchtower handler to logger
    cloudwatch_handler = watchtower.CloudWatchLogHandler(
        boto3_client=client,
        log_group=os.environ.get('LOG_GROUP'),
        stream_name=os.environ.get('LOG_STREAM'),
        use_queues=False
    )
    cloudwatch_handler.setFormatter(log_formatter)
    custom_logger.addHandler(cloudwatch_handler)
    return custom_logger


logger = get_logger("utils")


def generate_document(uploaded_file, text, question_doc, user_id):
    uploaded_content = ""
    message = None
    if not text and not uploaded_file:
        message = "Please provide either text or document!"
        logger.error(f"Error: {message}")
        return {"message": message, "output": None}
    if text and uploaded_file:
        message = "Please provide either text or document, not both!"
        logger.error(f"Error: {message}")
        return {"message": message, "output": None}

    try:
        if text:
            logger.info("Received input as text.")

        elif uploaded_file:
            logger.info("Received input as file. Converting to text.")
            try:
                filename = uploaded_file.name
                ext = os.path.splitext(filename)[1].lower()
                file_obj = uploaded_file.file
                if ext in ['.txt', '.pdf', '.docx', '.md']:
                    uploaded_content = file_to_text(ext, file_obj)
                else:
                    message = f"Unsupported file: {uploaded_file.filename}"
                    logger.error(message)
                    return {"message": message, "output": None}
            except Exception as error:
                message = f"Error occurred while processing document - {error}."
                logger.error(message)
                return {"message": message, "output": None}
        from agents.individual_agents.main import generate_graph
        data = text or uploaded_content
        if question_doc:
            question_filename = question_doc.name
            question_ext = os.path.splitext(question_filename)[1].lower()
            question_file_obj = question_doc.file
            questions_content = file_to_text(question_ext, question_file_obj)
            data += f"\n\nQuestions and Answers for clarification:\n\n{questions_content}"
        output = generate_graph(data, user_id)
        return {"message": message, "output": output}
    except Exception as error:
        message = f"Error occurred while generating scope document - {error}."
        logger.error(message)
        return {"message": message, "output": None}



def file_to_text(ext, file_obj):
    if ext == '.txt':
        message = "Received input as text file. Converting to text."
        logger.info(message)
        uploaded_content = file_obj.read().decode('utf-8')
    elif ext == '.pdf':
        message = "Received input as pdf file. Converting to text."
        logger.info(message)
        reader = PyPDF2.PdfReader(file_obj)
        uploaded_content = ''.join([page.extract_text() or '' for page in reader.pages])
    elif ext == '.docx':
        message = "Received input as docx file. Converting to text."
        logger.info(message)
        uploaded_content = '\n'.join([para.text for para in docx.Document(file_obj).paragraphs])
    else:
        message = "Received input as md file. Converting to text."
        logger.info(message)

        html = markdown(file_obj.read().decode('utf-8'))
        html = re.sub(r'<pre>(.*?)</pre>', ' ', html)
        html = re.sub(r'<code>(.*?)</code >', ' ', html)
        soup = BeautifulSoup(html, "html.parser")
        uploaded_content = soup.text
    return uploaded_content


def read_user_query(uploaded_file, text):
    uploaded_content = ""
    message = None
    try:
        if text:
            logger.info("Received input as text.")

        elif uploaded_file:
            try:
                filename = uploaded_file.name
                ext = os.path.splitext(filename)[1].lower()
                file_obj = uploaded_file.file
                if ext in ['.txt', '.pdf', '.docx', '.md']:
                    uploaded_content = file_to_text(ext, file_obj)
                else:
                    message = f"Unsupported file: {uploaded_file.filename}"
                    logger.error(message)
                    uploaded_content = None
            except Exception as error:
                message = f"Error occurred while processing document - {error}."
                logger.error(message)
                return {"message": message, "output": None}
        data = text or uploaded_content
        with open("user_query.txt", 'w') as query_file:
            query_file.write(data)
        return {"message": message, "output": data}
    except Exception as error:
        message = f"Error occurred while generating scope document - {error}."
        logger.error(message)
        return {"message": message, "output": None}


def handle_form(form, prompt_path, user_input=None, original_text=None, output_format=None,
                panel_details=None, module_details=None):
    try:
        form_text = form.cleaned_data.get('requirement_text')
        form_file = form.cleaned_data.get('requirement_doc')
        question_file = form.cleaned_data.get('questions_doc', None)
        prompt_path = f"{INSTRUCTIONS_PATH}/{prompt_path}"
        prompt = open(prompt_path).read()
        questions_data = ""
        output = None
        # if a questions_file is provided, append it to the prompt
        if question_file:
            logger.info("Received questions file.")
            filename = question_file.name
            ext = os.path.splitext(filename)[1].lower()
            file_obj = question_file.file
            if ext in ['.txt', '.pdf', '.docx', '.md']:
                questions_data = file_to_text(ext, file_obj)
            else:
                message = f"Unsupported file: {question_file.filename}"
                logger.error(message)
                questions_data = None
            logger.info("Received questions data from file.")
        # If user suggestions are provided, then use the user input
        if user_input:
            response = open("user_query.txt").read()
            logger.info("Received user input for suggestions.")
            output = {
                "role": "user",
                "content": f"Original user query:\n\n{response}. \n\n"
                           f"Previously generated content:\n\n{original_text}. \n\n"
                           f"User Suggestions:\n\n{user_input}. "}
            if questions_data:
                output['content'] += f"\n\nQuestions and Answers for clarification:\n\n{questions_data}"
            if panel_details:
                output['content'] += f"\n\nPanel Details:\n\n{panel_details}"
            if module_details:
                output['content'] += f"\n\nModule Details:\n\n{module_details}"
        else:
            if not form_text and not form_file:
                message = "Please provide either text or document!"
                logger.error(f"Error: {message}")
                response = {"message": message, "output": None}
                return response
            elif form_text and form_file:
                message = "Please provide either text or document, not both!"
                logger.error(f"Error: {message}")
                response = {"message": message, "output": None}
                return response
            else:
                response = read_user_query(form_file, form_text)
                output = response.get("output")
                if output:
                    if questions_data:
                        output += f"\n\nQuestions and Answers for clarification:\n\n{questions_data}"
                    if panel_details:
                        output += f"\n\nPanel Details:\n\n{panel_details}"
                    if module_details:
                        output += f"\n\nModule Details:\n\n{module_details}"
        # If the output format is provided, use it to create the agent
        if output_format:
            agent = create_react_agent(openai_fastest_llm, tools=[], prompt=prompt,
                                       response_format=output_format)
        else:
            agent = create_react_agent(openai_fastest_llm, tools=[], prompt=prompt)
        response = agent.invoke({"messages": output})
        message = "Successfully generated answer"
        logger.info(message)
        return {"message": message, "output": response}
    except Exception as error:
        message = f"Exception occurred while handling form - {error}."
        logger.error(message)
        return {"message": message, "output": None}
