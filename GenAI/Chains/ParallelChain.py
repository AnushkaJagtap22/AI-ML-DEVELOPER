
from langchain_groq import ChatGroq
from langchain_mistralai import ChatMistralAI
from dotenv import load_dotenv

from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableParallel

load_dotenv()

# Initialize models
model1 = ChatGroq(
    model="openai/gpt-oss-120b"
)

model2 = ChatMistralAI(
    model="mistral-small-latest"
)

# Prompt templates
prompt1 = PromptTemplate(
    template="""
    Generate short and simple notes from the following text:

    {text}
    """,
    input_variables=["text"]
)

prompt2 = PromptTemplate(
    template="""
    Generate 5 short questions based on the following text:

    {text}
    """,
    input_variables=["text"]
)

prompt3 = PromptTemplate(
    template="""
    Merge the following notes and questions into
    a single well-structured document.

    Notes:
    {notes}

    Questions:
    {questions}
    """,
    input_variables=["notes", "questions"]
)

# Output parser
parser = StrOutputParser()

# Parallel chain
parallel_chain = RunnableParallel({
    "notes": prompt1 | model1 | parser,
    "questions": prompt2 | model2 | parser
})

# Sequential merge chain
merge_chain = prompt3 | model1 | parser

# Complete chain
chain = parallel_chain | merge_chain

text = """
Support Vector Machines (SVMs) are a set of supervised
learning methods used for classification, regression
and outlier detection.

Advantages:
- Effective in high-dimensional spaces.
- Memory efficient.
- Supports different kernel functions.

Disadvantages:
- Kernel selection is important.
- Does not directly provide probability estimates.
"""

result = chain.invoke({"text": text})

print(result)
