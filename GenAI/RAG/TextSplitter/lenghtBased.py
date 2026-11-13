from langchain.text_splitter import CharacterTextSplitter

text = "This is a sample text that we will split into smaller chunks based on character length. The text splitter will help us manage large documents by breaking them down into more manageable pieces."

splitter = CharacterTextSplitter(
    chunk_size=50,  # Maximum number of characters in each chunk
    chunk_overlap=10,  # Number of characters to overlap between chunks
    separator="\n"  # Separator to use when splitting the text
)

split_text = splitter.split_text(text)

print(split_text)