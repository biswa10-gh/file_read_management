# CHANGES MADE:
# 1️⃣ Changed import from `from crewai.tools import Tool` → `from crewai.tools import BaseTool`
#     → CrewAI v1.1.0 uses BaseTool, not Tool.
#
# 2️⃣ Renamed the main method from `run()` → `_run()`
#     → In v1.1.0, tool logic must be inside `_run()`, not `run()`.
#
# 3️⃣ No other logic changes — file reading logic remains the same.
 
from crewai.tools import BaseTool  # ✅ Updated import
import csv
import json
import PyPDF2
from docx import Document
 
class ReadFileTool(BaseTool):  # ✅ Inherit from BaseTool
    name = "read_file_tool"
    description = "Read CSV, PDF, TXT, DOCX, and JSON files"
 
    def _run(self, file_path: str):  # ✅ Renamed from run() to _run()
        """Reads a file and returns its contents depending on file type."""
        file_type = file_path.split(".")[-1].lower()
 
        try:
            if file_type == "csv":
                with open(file_path, "r", encoding="utf-8") as f:
                    reader = csv.DictReader(f)
                    data = [row for row in reader]
                return data
 
            elif file_type == "pdf":
                with open(file_path, "rb") as f:
                    reader = PyPDF2.PdfReader(f)
                    text = ""
                    for page in reader.pages:
                        text += page.extract_text() + "\n"
                return text
 
            elif file_type == "txt":
                with open(file_path, "r", encoding="utf-8") as f:
                    return f.read()
 
            elif file_type == "docx":
                doc = Document(file_path)
                full_text = "\n".join([p.text for p in doc.paragraphs])
                return full_text
 
            elif file_type == "json":
                with open(file_path, "r", encoding="utf-8") as f:
                    return json.load(f)
 
            else:
                return f"File type .{file_type} is not supported in CrewAI v1.1.0"
 
        except Exception as e:
            return f"Error reading file: {str(e)}"