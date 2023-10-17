"""Strategy object for the pdf file type."""
from quote_engine import ( 
                         QuoteModel
                        ,IngestorInterface
)
import PyPDF2

class PDFIngestor(IngestorInterface):
    """This class is responsible for parsing pdf files"""
    
    #The file extension supported is '.txt'
    #allowed_extensions = ['txt']
    
    @classmethod
    def can_ingest(cls, path: str) -> bool:
        """Check if the given path is a txt file.
        
        Returns:
            True if the path is a txt file
        """
        # return file_extension in cls.allowed_extensions
        return path.endswith('.pdf')

    @classmethod
    def parse(cls, path: str) -> list[QuoteModel]:
        """Extract the quote body and author from the file given.
        
        Returns:
            quotes: list of QuoteModel objects
        """
        # list of QuoteModel objects extracted from the given pdf file
        quotes = []

        try:
            with open(path, 'rb') as file:
                # read the pdf file
                pdf_file = PyPDF2.PdfReader(file)
                # parse each pdf file page
                for page in pdf_file.pages:
                    # get the content of the page
                    text = page.extract_text()
                    # parse each line of the pdf page
                    for line in text.split('\n'):
                        """extract body and author
                        strip(): remove any leading or trailing whitespace characters
                        split(' - '): split the line into a list of values based on the comma (,) delimiter
                        """
                        line_values = line.strip().split(' - ')
                        if len(line_values) == 2:
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