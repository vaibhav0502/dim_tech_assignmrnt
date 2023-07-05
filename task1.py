import fitz
import camelot

import pdfplumber
import nltk
from nltk.tokenize import sent_tokenize
nltk.download('punkt')


def read_table_using_camelot(pdf_path, page_no):
    '''
    Function to read pdf and return tables
    '''
    table_dict = []

    try:
        tables = camelot.read_pdf(pdf_path, pages=f"{page_no+1}")

        if tables:
            for table in tables:
                table_dict.append(
                    {
                        'data':table.df.to_dict('records'),
                        # "data": table.df,
                        "bbox": table._bbox,
                    }
                )

            return table_dict
        else:
            return []

    except Exception as e:
        print("Exception in read_table_using_camelot", e)
        return table_dict

def change_y_of_table(tables, height):
    """
    Function to change y coordinate of camelot table
    Allign that with fitz coordinate
    """
    for table in tables:
        x1, y1, x2, y2 = table["bbox"]
        y11 = height - y2
        y22 = height - y1
        table["bbox"] = (x1, y11, x2, y22)
    return tables


def add__d(data, bbox, type_):
    data = {"data": data, "bbox": bbox, "type": type_}
    return data


def add_tables_to_output(pdf_path, h, pp, text_data):
    try:
        # get tables using camelot
        tables = read_table_using_camelot(pdf_path, 0)
        tables = change_y_of_table(tables, h)

        if tables:
            for table in tables:
                data = add__d(table["data"], table["bbox"], "table")
                text_data[pp]["data"].append(data)
            return text_data, tables
        else:
            return text_data, []
    except Exception as e:
        print("Exception in add_tables_to_output", e)
        return text_data, []

def check_overlap(t1, t2):
    y1, y2 = int(t1[0]), int(t1[1])
    r1 = set(list(range(y1, y2)))

    y1, y2 = int(t2[0]), int(t2[1])
    r2 = set(list(range(y1, y2)))

    overlap = r1.intersection(r2)
    return len(overlap) > 0


def check_if_table_overlap(tables, bbox, overlap_flag):
    """
    Function to check if line coordinate overlaps with table coordinate
    """
    tables_bbox_list = [t["bbox"] for t in tables]
    for t in tables_bbox_list:
        if check_overlap((bbox[1], bbox[3]), (t[1], t[3])):
            overlap_flag = True
        else:
            overlap_flag = False
    return overlap_flag


def get_doc_data(pdf_path):
    """
    Function to return text block from given doc.

    Args:
        pdf_path (str): pdf file path
    Returns:
        text_data: Dict containing list of text and bbox
    """

    text_data = {}

    try:
        doc = fitz.open(pdf_path)
        for page_no in range(doc.page_count):            

            page = doc[page_no]
            w, h = page.mediabox.width, page.mediabox.height
            
            texts, bbox_list = [], []

            pp = f"page_{page_no}"
            text_data[pp] = {}
            text_data[pp]['width'] = w
            text_data[pp]['height'] = h
            text_data[pp]['data'] = []

            # get table data using camelot and add it to output json (text_data)
            text_data, tables = add_tables_to_output(pdf_path, h, pp, text_data)
            tables = []

            for block in page.get_text("dict")["blocks"]:
                if "image" in block.keys():
                    continue

                for line in block["lines"]:
                    line_text = ""
                    for span in line["spans"]:
                        line_text += f'{span["text"]} '

                    if line_text.strip():
                      bbox = [round(coord, 2) for coord in line["bbox"]]
                      data = add__d(line_text.strip(), bbox, 'line')

                      ## check overlap of line with table data, if line overlap with table bbox then do not add line
                      if not tables:
                        text_data[pp]['data'].append(data)
                      else:
                        overlap_flag = False
                        overlap_flag = check_if_table_overlap(tables, bbox, overlap_flag)
                        if not overlap_flag:
                          data = add__d(line_text.strip(), bbox, 'line')
                          text_data[pp]['data'].append(data)

            # sort data as per top
            d = text_data['page_0']['data']
            text_data['page_0']['data'] = sorted(d, key=lambda d: (d['bbox'][1], d['bbox'][3]))
    except Exception as e:
        print("Exception in get_doc_data", e)
    return text_data


pdf_path = "pdfs/chapter.pdf"
output_json = get_doc_data(pdf_path)


### Get text data
no = 0
lines = [d['data'] for d in output_json[f'page_{no}']['data'] if d['type'] == 'line']
print(lines)


### Get table data
# Table is converted to json
no = 0
tables = [d['data'] for d in output_json[f'page_{no}']['data'] if d['type'] == 'table']
if tables:
    print(tables[0])
else:
    print("no tables")


## Get sentence data
def get_page_data(pdf, page_no):
    page = pdf.pages[page_no]
    text = page.extract_text()
    sentences = sent_tokenize(text)
    return sentences


pdf = pdfplumber.open(pdf_path)

page_no = 4
sentences = get_page_data(pdf, page_no)
for each in sentences:
  print(each)
  print("---"*20)

