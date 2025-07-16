from .pdf_loader import My_PDFReader_sorted


def parse_document(path_pdf_file):
    reader = My_PDFReader_sorted()
    data = reader.load_data(file_path=path_pdf_file)

    return data