import subprocess
from docx import Document

# # Create and start the processes
# proc1 = subprocess.Popen(['python', './SLC/ticket.py'])
# proc2 = subprocess.Popen(['python', './NginX/nginx.py'])
# proc3 = subprocess.Popen(['python', './Audittrail/audittrail.py'])

# # Wait for the processes to finish
# proc1.wait()
# proc2.wait()
# proc3.wait()

def merge_docx(docx1_path, docx2_path, output_path):
    # Load the first document
    doc1 = Document(docx1_path)

    # Load the second document
    doc2 = Document(docx2_path)

    # Add content from the second document to the first document
    for element in doc2.element.body:
        doc1.element.body.append(element)

    # Save the merged document to the output file
    doc1.save(output_path)

# Example usage
merge_docx('./Allpart/Nginx_edit.docx', './Allpart/Audittrail_edit.docx', 'merged_document.docx')
