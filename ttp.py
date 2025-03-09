import os
import sys
import nbconvert
import nbformat
from nbconvert.preprocessors import ExecutePreprocessor
from traitlets.config import Config

def convert_ipynb_to_pdf(input_file, output_file=None, execute=False, timeout=600):
    """
    Convert a Jupyter Notebook to PDF.
    
    Args:
    input_file (str): Path to the input .ipynb file
    output_file (str, optional): Path to the output PDF file
    execute (bool, optional): Whether to execute the notebook before converting
    timeout (int, optional): Execution timeout in seconds (default 10 minutes)
    
    Returns:
    bool: True if conversion successful, False otherwise
    """
    # Validate input file
    if not os.path.exists(input_file):
        print(f"Error: File {input_file} does not exist.")
        return False
    
    # Determine output file path
    if output_file is None:
        output_file = os.path.splitext(input_file)[0] + '.pdf'
    
    try:
        # Read the notebook
        with open(input_file, 'r', encoding='utf-8') as f:
            nb = nbformat.read(f, as_version=4)
        
        # Execute the notebook if requested
        if execute:
            print("Executing notebook...")
            ep = ExecutePreprocessor(timeout=timeout)
            ep.preprocess(nb, {})
        
        # Configure PDF export
        c = Config()
        c.PDFExporter.latex_engine = 'xelatex'
        c.PDFExporter.config = c
        
        # Convert to PDF
        pdf_exporter = nbconvert.exporters.PDFExporter(config=c)
        body, resources = pdf_exporter.from_notebook_node(nb)
        
        # Write PDF
        with open(output_file, 'wb') as f:
            f.write(body)
        
        print(f"Converted {input_file} to {output_file} successfully!")
        return True
    
    except Exception as e:
        print(f"Error occurred while converting {input_file}: {e}")
        return False

def convert_multiple_ipynb_files(file_list, output_dir=None, execute=False, timeout=600):
    """
    Convert multiple Jupyter Notebooks to PDF.
    
    Args:
    file_list (list): List of Jupyter Notebook file paths
    output_dir (str, optional): Directory to save converted PDF files
    execute (bool, optional): Whether to execute notebooks before converting
    timeout (int, optional): Execution timeout in seconds
    
    Returns:
    tuple: (successful conversions, total files)
    """
    # Create output directory if not exists
    if output_dir:
        os.makedirs(output_dir, exist_ok=True)
    
    successful_conversions = 0
    total_files = len(file_list)
    
    for notebook_file in file_list:
        # Prepare output file path
        if output_dir:
            # Use original filename in the specified output directory
            output_file = os.path.join(output_dir, os.path.basename(notebook_file).replace('.ipynb', '.pdf'))
        else:
            output_file = None
        
        # Convert the file
        if convert_ipynb_to_pdf(notebook_file, output_file, execute, timeout):
            successful_conversions += 1
    
    print(f"\nConversion Summary:")
    print(f"Total files processed: {total_files}")
    print(f"Successful conversions: {successful_conversions}")
    print(f"Failed conversions: {total_files - successful_conversions}")
    
    return successful_conversions, total_files

def main():
    # In another Python script
    file_list = [
         "level4_prodriver.ipynb"
    ]


    successful, total = convert_multiple_ipynb_files(
        file_list, 
        output_dir='pdfs', 
        execute=True
    )

    print(f"\nTotal successful conversions: {successful} out of {total}")
    # Convert multiple files

if __name__ == "__main__":
    main()