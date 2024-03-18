

from langchain import OpenAI
from langchain.utilities import SQLDatabase
from langchain_experimental.sql import SQLDatabaseChain
from langchain.prompts import SemanticSimilarityExampleSelector
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import Chroma
from langchain.prompts import FewShotPromptTemplate
from langchain.chains.sql_database.prompt import PROMPT_SUFFIX, _mysql_prompt
from langchain.prompts.prompt import PromptTemplate


import getpass
import os
# from dotenv import load_dotenv
# load_dotenv()  


import json


with open("resource_templates.json", "r") as f:
    resource_templates = json.load(f)

def db_chain():
    db_user = "root"
    db_password = "root"
    db_host = "localhost"
    db_name = "Fhir"

    db = SQLDatabase.from_uri(f"mysql+pymysql://{db_user}:{db_password}@{db_host}/{db_name}",
                              sample_rows_in_table_info=3)
    llm = OpenAI(openai_api_key=os.environ["API_KEY"], temperature=0.7)

    embeddings = HuggingFaceEmbeddings(model_name='sentence-transformers/all-MiniLM-L6-v2')
    to_vectorize = [" ".join(example.values()) for example in database]
    vectorstore = Chroma.from_texts(to_vectorize, embeddings, metadatas=database) # need to create a database file to share the format of sql database
    example_selector = SemanticSimilarityExampleSelector(
        vectorstore=vectorstore,
        k=2,
    )
    fhir_prompt = """You are a FHIR Resource generating expert. Given a converstion between doctor and patient, first create a syntactically correct FHIR resource in JSON Format as specified by the user then look at the results  and return the FHIR resource to the input conversation.
    Never create random values for values that are not present in the conversation. You must only the columns that are needed to answer the question. Wrap each column name in backticks (`) to denote them as delimited identifiers.
    Generate the following FHIR resources based on the conversation and exam:
    Patient: Capture the patient's demographics and medical history details.
    Practitioner: Identify the doctor involved in the encounter.
    Encounter: Describe the patient-doctor interaction, including the reason for the visit.
    Observation: Record the patient's reported symptoms and the physical exam findings.

    Use clear and concise language for each resource. Maintain patient confidentiality and adhere to HIPAA regulations. Strive for accuracy and consistency in your FHIR structures.
    resource_template = resource_templates["resource"]
    No pre-amble.
    """

   example_prompt = PromptTemplate(
    input_variables=["Conversation"],
    template="\nConversation: {Conversation}\nFhir: {Resource}\nResource Template: {ResourceTemplate}",
)

    
    chain = SQLDatabaseChain.from_llm(llm, db, verbose=True, prompt=few_shot_prompt)
    return chain
