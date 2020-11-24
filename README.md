# tariff-json-scraper

## Implementation steps

- Create and activate a virtual environment, e.g.

  `python3 -m venv venv/`
  `source venv/bin/activate`

- Install necessary Python modules 

  - autopep8==1.5.4
  - certifi==2020.11.8
  - chardet==3.0.4
  - idna==2.10
  - pycodestyle==2.6.0
  - python-dotenv==0.15.0
  - requests==2.25.0
  - toml==0.10.2
  - urllib3==1.26.2

  via `pip3 install -r requirements.txt`


## Usage

Two modes of usage: run usage 1 first, as it is a pre-requisite of usage 2

### Usage 1 - Download structural elements

`python3 main.py structure`

Downloads the following structures:

- sections
- chapters
- search_references
- geographical_areas
- footnote_types
- certificate_types
- additional_code_types
- additional_codes (page 1 of x, for comparison only)

Takes 5 minutes

### Usage 1 - Download structural elements

`python3 main.py commodities`

Downloads commodities - takes hours

You are able to start the download at a specific part, by specifying as the second argument the commodity code on which to start, e.g.

`python3 main.py commodities 0302118019`