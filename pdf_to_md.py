#!/usr/bin/env python3
"""
PDF to Markdown Converter
Converts PDF files to Markdown format
"""

import os
import sys
import argparse
from pathlib import Path

try:
    import pdfplumber
    HAS_PDFPLUMBER = True
except ImportError:
    HAS_PDFPLUMBER = False

try:
    from pypdf import PdfReader
    HAS_PYPDF = True
except ImportError:
    HAS_PYPDF = False


def install_dependencies():
    """Install required dependencies"""
    print("Installing required packages...")
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "pdfplumber", "pypdf"])
    print("Dependencies installed!")


def extract_text_with_pdfplumber(pdf_path):
    """Extract text from PDF using pdfplumber"""
    text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n\n"
    return text


def extract_text_with_pypdf(pdf_path):
    """Extract text from PDF using pypdf"""
    text = ""
    reader = PdfReader(pdf_path)
    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text + "\n\n"
    return text


def text_to_markdown(text):
    """Convert plain text to Markdown format"""
    lines = text.split('\n')
    markdown_lines = []
    
    for line in lines:
        stripped = line.strip()
        if not stripped:
            markdown_lines.append('')
            continue
        
        # Headers (lines starting with numbers followed by dot or just bold text)
        if stripped[0].isdigit() and '.' in stripped[:5]:
            # Convert "1. Title" to "## Title"
            parts = stripped.split('.', 1)
            if len(parts) == 2:
                markdown_lines.append(f"## {parts[1].strip()}")
            else:
                markdown_lines.append(stripped)
        elif len(stripped) <= 50 and stripped.isupper():
            # Short all-caps lines as headers
            markdown_lines.append(f"# {stripped}")
        elif len(stripped) <= 80 and stripped.isupper():
            markdown_lines.append(f"## {stripped}")
        elif stripped.startswith('•') or stripped.startswith('-') or stripped.startswith('*'):
            # List items
            markdown_lines.append(f"- {stripped[1:].strip()}")
        else:
            markdown_lines.append(stripped)
    
    return '\n'.join(markdown_lines)


def convert_pdf_to_md(pdf_path, output_path=None):
    """Convert PDF file to Markdown"""
    if not os.path.exists(pdf_path):
        print(f"Error: File not found: {pdf_path}")
        return False
    
    # Extract text
    if HAS_PDFPLUMBER:
        text = extract_text_with_pdfplumber(pdf_path)
    elif HAS_PYPDF:
        text = extract_text_with_pypdf(pdf_path)
    else:
        print("Error: No PDF extraction library available. Install pdfplumber or pypdf")
        return False
    
    # Convert to markdown
    markdown_content = text_to_markdown(text)
    
    # Save to file
    if output_path is None:
        output_path = os.path.splitext(pdf_path)[0] + ".md"
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(markdown_content)
    
    print(f"Successfully converted {pdf_path} to {output_path}")
    return True


def convert_directory(pdf_dir, output_dir=None):
    """Convert all PDF files in a directory to Markdown"""
    pdf_dir = Path(pdf_dir)
    if output_dir is None:
        output_dir = pdf_dir / "markdown"
    else:
        output_dir = Path(output_dir)
    
    output_dir.mkdir(parents=True, exist_ok=True)
    
    converted = 0
    for pdf_file in pdf_dir.glob("*.pdf"):
        md_file = output_dir / (pdf_file.stem + ".md")
        if convert_pdf_to_md(str(pdf_file), str(md_file)):
            converted += 1
    
    print(f"Converted {converted} PDF files to Markdown in {output_dir}")
    return converted


def main():
    parser = argparse.ArgumentParser(description='Convert PDF files to Markdown')
    parser.add_argument('input', nargs='?', help='PDF file or directory containing PDF files')
    parser.add_argument('-o', '--output', help='Output file or directory')
    parser.add_argument('--install', action='store_true', help='Install required dependencies')
    
    args = parser.parse_args()
    
    if args.install:
        install_dependencies()
        return
    
    if not args.input:
        parser.print_help()
        return
    
    input_path = Path(args.input)
    
    if input_path.is_file() and input_path.suffix.lower() == '.pdf':
        convert_pdf_to_md(str(input_path), args.output)
    elif input_path.is_dir():
        convert_directory(str(input_path), args.output)
    else:
        print(f"Error: {args.input} is not a valid PDF file or directory")


if __name__ == '__main__':
    # Check for dependencies
    if not HAS_PDFPLUMBER and not HAS_PYPDF:
        print("Warning: No PDF extraction library found.")
        print("Run with --install to install dependencies, or install manually:")
        print("  pip install pdfplumber pypdf")
        sys.exit(1)
    
    main()
