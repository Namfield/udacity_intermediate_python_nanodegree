"""Strategy object for the pdf file type."""
# from .quote_model import QuoteModel
# from .ingestor_interface import IngestorInterface
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
        # # splits the path by '.' and compares the last element with the allowed extensions.
        # file_extension = path.split('.')[-1]

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
    

# @classmethod
# def parse(cls, path: str) -> list[QuoteModel]:
#     """Extract the quote body and author from the file given.
    
#     Returns:
#         quotes: list of QuoteModel objects
#     """
#     quotes = []

#     try:
#         with open(path, 'rb') as file:
#             pdf_reader = PyPDF2.PdfReader(file)
#             for page in pdf_reader.pages:
#                 text = page.extract_text()
#                 # Parse the text and extract the quote body and author
#                 # Create a QuoteModel object and append it to the quotes list
#     except FileNotFoundError:
#         print(f"File not found: {path}")
#     except Exception as e:
#         print(f"There is an error {str(e)} when parsing the file {path}")

#     return quotes


# @classmethod
#     def parse(cls, path: str) -> List[QuoteModel]:
#         quotes = []
#         try:
#             process = subprocess.Popen(['pdftotext', path, '-'], stdout=subprocess.PIPE)
#             output, error = process.communicate()
#             if error:
#                 raise Exception(f"Error extracting text from PDF: {error}")
            
#             text = output.decode('utf-8')
#             lines = text.split('\n')
            
#             for line in lines:
#                 # Assuming each line in the PDF contains a quote
#                 # Split the line into body and author using a delimiter
#                 body, author = line.strip().split('-')
#                 quote = QuoteModel(body.strip(), author.strip())
#                 quotes.append(quote)
            
#             return quotes
#         except FileNotFoundError:
#             print(f"File not found: {path}")
#         except Exception as e:
#             print(f"An error occurred while parsing the PDF file: {path}")
#             print(f"Error details: {str(e)}")
        
#         return quotes
    

# @classmethod
#     def parse(cls, path: str) -> List[QuoteModel]:
#         quotes = []
#         try:
#             with open(path, 'rb') as file:
#                 reader = PyPDF2.PdfFileReader(file)
#                 num_pages = reader.numPages
                
#                 for page_num in range(num_pages):
#                     page = reader.getPage(page_num)
#                     text = page.extractText()
                    
#                     # Assuming each page contains a quote in the format "body - author"
#                     # Split the text into body and author using the dash as the delimiter
#                     body, author = text.strip().split('-')
#                     quote = QuoteModel(body.strip(), author.strip())
#                     quotes.append(quote)
            
#             return quotes
#         except FileNotFoundError:
#             print(f"File not found: {path}")
#         except PyPDF2.PdfReadError:
#             print(f"Error reading PDF file: {path}")
#         except Exception as e:
#             print(f"An error occurred while parsing the PDF file: {path}")
#             print(f"Error details: {str(e)}")
        
#         return quotes