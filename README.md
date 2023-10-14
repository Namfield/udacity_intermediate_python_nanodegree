# Meme Generator

## Overview
This is a meme generator program. It takes a random image from a folder and a random quote from a file and combines them to create a meme.

## Usage
### Quote Engine
Using base class `IngestorInterface` to ingest different types of files.
With:
- @classmethod `can_ingest` method to check if the file can be ingested.
- @classmethod `parse` method to parse the file.

Example:
```
from QuoteEngine.ingestor import Ingestor

ingestor = Ingestor.parse(path='./_data/DogQuotes/DogQuotesCSV.csv')
for quote in ingestor.quotes:
    print(quote)
```

### Meme Engine
Manipulate any given images to generate a meme
.

Example:
```
from MemeEngine.generator import MemeGenerator
meme = MemeGenerator(output_dir='./output')

meme.make_meme('./_data/photos/dog/xander_1.jpg', 'Work hard', 'Play hard')
```