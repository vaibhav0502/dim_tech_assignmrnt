# NLP Assignment

- INSTALL Python 3.8

```
sudo apt update
sudo apt install software-properties-common
sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt install python3.8
sudo apt-get install python3.8-venv
```

- Create a Virtual Environment outside the Project folder

```python3.8 -m venv tasks```

- Activate the Virtual Environment.

```source tasks/bin/activate(Linux)```


- Install required Python libraries.

```
pip install -r requirements.txt

apt-get install build-essential
apt install ghostscript python3-tk
```


## Task 1

- Download the publicly available reports and extract the contents out of it.  
- I have used `Fitz` to get text data and `Camelot` to get tabular data
- Final output will be a dictionary containing text and table data for each page
- Run `task1.py` or you can see the output in `task1.ipynb`
- Pass pdf_file path to function `get_doc_data` it will return output_json


