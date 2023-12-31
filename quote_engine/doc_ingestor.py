"""Strategy object for the docx file type."""
# from .quote_model import QuoteModel
# from .ingestor_interface import IngestorInterface
from quote_engine import QuoteModel, IngestorInterface
from docx import Document

class DOCXIngestor(IngestorInterface):
    """This class is responsible for parsing txt files"""
    
    #The file extension supported is '.docx'
    #allowed_extensions = ['docx']
    
    @classmethod
    def can_ingest(cls, path: str) -> bool:
        """Check if the given path is a docx file.
        
        Returns:
            True if the path is a docx file
        """
        # return file_extension in cls.allowed_extensions
        return path.endswith('.docx')

    @classmethod
    def parse(cls, path: str) -> list[QuoteModel]:
        """Extract the quote body and author from the file given.
        
        Returns:
            quotes: list of QuoteModel objects
        """
        # list of QuoteModel objects extracted from the given docx file
        quotes = []

        try:
            # read the docx file
            doc_file = Document(path)
            # parse each paragraph
            for paragraph in doc_file.paragraphs:
                # get the content of the paragraph
                text = paragraph.text.strip()
                # parse each line of the paragraph
                for line in text.split('\n'):
                    # check if the line is empty
                    if line.strip() == '':
                        # stop parsing when encountering an empty line
                        break
                    """extract body and author
                    strip(): remove any leading or trailing whitespace characters
                    split(' - '): split the line into a list of values based on the comma (,) delimiter
                    """
                    body, author = line.strip().split(' - ')
                    # create a corresponding QuoteModel object
                    quote = QuoteModel(body, author)
                    # store in the quotes list
                    quotes.append(quote)
        except FileNotFoundError:
            print(f"File not found: {path}")
        except Exception as e:
            print(f"There is error \"{str(e)}\" when parsing the file {path}")

        return quotes