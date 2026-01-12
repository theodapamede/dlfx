import os
import datetime
from IPython.display import display, Markdown

def stamp_notebook(created_date, author="", notebook_path=None):
    """
    Displays a formatted info block to track notebook creation and modification.
    Distinct from DICOM/Image metadata.
    
    Args:
        created_date (str): The date the notebook was created (e.g., "2025-08-15").
        author (str): Researcher name.
        notebook_path (str): The filename of the .ipynb file to pull 'Last Modified' stats.
    """
    info_lines = [
        "**Notebook Session Info:**",
        f"* **Created:** {created_date}",
    ]
    
    # Check if we can pull filesystem modification time
    if notebook_path and os.path.exists(notebook_path):
        mtime = os.path.getmtime(notebook_path)
        last_mod = datetime.datetime.fromtimestamp(mtime).strftime('%Y-%m-%d %H:%M:%S')
        info_lines.append(f"* **Last Modified:** {last_mod}")
    else:
        info_lines.append("* **Last Modified:** (Run save to update / path not found)")
        
    info_lines.append(f"* **Researcher:** {author}")

    # Render as a clean Markdown block
    display(Markdown("---"))
    display(Markdown("\n".join(info_lines)))
    display(Markdown("---"))