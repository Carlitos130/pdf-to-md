# PDF to Markdown Converter

A simple Python tool to convert PDF files to Markdown format.

## Features

- Convert single PDF files to Markdown
- Convert all PDF files in a directory
- Preserves basic formatting (headers, lists)
- Easy to use CLI interface

## Requirements

- Python 3.6+
- Required packages: `pdfplumber` or `pypdf`

## Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/Carlitos130/pdf-to-md.git
   cd pdf-to-md
   ```

2. Install dependencies:
   ```bash
   pip install pdfplumber pypdf
   ```

Or use the built-in installation:
   ```bash
   python pdf_to_md.py --install
   ```

## Usage

### Convert a single PDF file:
```bash
python pdf_to_md.py input.pdf
```

This will create `input.md` in the same directory.

### Specify output file:
```bash
python pdf_to_md.py input.pdf -o output.md
```

### Convert all PDFs in a directory:
```bash
python pdf_to_md.py /path/to/pdf/directory/
```

This will create a `markdown` subdirectory with all converted files.

### Specify output directory:
```bash
python pdf_to_md.py /path/to/pdf/directory/ -o /path/to/output/directory/
```

## Examples

```bash
# Convert single file
python pdf_to_md.py document.pdf

# Convert with custom output name
python pdf_to_md.py report.pdf -o report.md

# Convert all PDFs in a folder
python pdf_to_md.py ./pdfs/

# Convert with custom output directory
python pdf_to_md.py ./pdfs/ -o ./markdown/
```

## How It Works

1. Extracts text from PDF using `pdfplumber` (preferred) or `pypdf`
2. Converts the extracted text to Markdown format:
   - Lines starting with numbers and dots become headers (##)
   - Short ALL-CAPS lines become main headers (#)
   - Lines with bullets (•, -, *) become list items
3. Saves the result as a .md file

## Notes

- PDF text extraction quality depends on the PDF structure
- Complex formatting (tables, images) may not be perfectly preserved
- For best results, use PDFs with selectable text (not scanned images)

## License

MIT License
