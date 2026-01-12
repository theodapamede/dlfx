import os
import datetime
import ipynbname
from IPython.display import display, Markdown

def stamp_notebook(created_date, author=""):
    """
    Displays a formatted session info block. 
    Automatically detects the notebook name and last modification time.
    """
    try:
        # Get the full path and the filename of the current notebook
        nb_path = ipynbname.path()
        nb_name = ipynbname.name() + ".ipynb"
        
        # Get last modified time from the filesystem
        mtime = os.path.getmtime(nb_path)
        last_mod = datetime.datetime.fromtimestamp(mtime).strftime('%Y-%m-%d %H:%M:%S')
    except Exception:
        # Fallback if ipynbname cannot detect the notebook (e.g. running as a script)
        nb_name = "Detection failed (run in Jupyter)"
        last_mod = "Unknown"

    info_lines = [
        "**Notebook Session Info:**",
        f"* **File:** `{nb_name}`",
        f"* **Created:** {created_date}",
        f"* **Last Modified:** {last_mod}",
        f"* **Researcher:** {author}"
    ]

    display(Markdown("---"))
    display(Markdown("\n".join(info_lines)))
    display(Markdown("---"))