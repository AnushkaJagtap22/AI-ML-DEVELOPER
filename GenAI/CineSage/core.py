from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langchain_core.prompts import ChatPromptTemplate

# Load environment variables
load_dotenv()

# Initialize the model
model = init_chat_model(
    "mistral-small-latest",
    temperature=0.9
)

# Prompt Template
prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
You are CineSage, an expert AI movie information extractor.

Your task is to analyze the given movie paragraph and extract only the most useful information.

Instructions:
- Use only the information present in the paragraph.
- Do not invent or assume facts.
- If a piece of information is not available, write "Not Mentioned".
- Keep the output neat and easy to read.
- Keep the quick summary between 2 and 3 sentences.
- Use bullet points wherever appropriate.
- Do not include unnecessary explanations.

Extract the following information:

🎬 Movie Name
📅 Release Year
🎭 Genre(s)
🎬 Director
✍️ Writer(s)
🎥 Producer(s)
⭐ Cast
🎼 Music Composer
📖 Plot
📝 Quick Summary (2–3 sentences)
🎯 Main Themes
🔑 Keywords
🌍 Setting / Location
👤 Main Characters
🏆 Awards / Recognition
⭐ Ratings (IMDb/Rotten Tomatoes/etc. if mentioned)
💰 Box Office (if mentioned)
🎞️ Notable Features
😊 Overall Mood / Tone
👥 Target Audience
💡 Interesting Fact (if mentioned)

End with one line:

Recommended For:
(A single sentence describing who would enjoy this movie.)
            """
        ),
        (
            "human",
            """
Analyze the following movie paragraph and extract all useful information.

Movie Paragraph:
{movie_paragraph}
            """
        )
    ]
)

# Take input from the user
print("=========== CineSage ===========")
print("Paste the movie description below.")
print("Press Enter twice (or Ctrl+Z then Enter on Windows / Ctrl+D on Linux/Mac) when finished.\n")

lines = []
while True:
    try:
        line = input()
        if line == "":
            break
        lines.append(line)
    except EOFError:
        break

movie_paragraph = "\n".join(lines)

# Create the chain
chain = prompt | model

# Invoke the model
response = chain.invoke(
    {
        "movie_paragraph": movie_paragraph
    }
)

# Print the output
print("\n========== Extracted Information ==========\n")
print(response.content)