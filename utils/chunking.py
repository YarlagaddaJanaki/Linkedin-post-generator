from langchain_text_splitters import RecursiveCharacterTextSplitter


class ChunkingService:

    def __init__(self):

        self.splitter = RecursiveCharacterTextSplitter(

            chunk_size=500,

            chunk_overlap=100,

            separators=[
                "\n\n",
                "\n",
                ".",
                " ",
                ""
            ]

        )

    def create_chunks(self, text):

        return self.splitter.split_text(text)