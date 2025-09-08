from langchain_core.documents import Document
import csv

def csv_to_documents(path: str) -> list[Document]:
    docs: list[Document] = []
    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            # Normalize row into content; also keep full row as metadata for filtering
            content = "\n".join([f"{k}: {v}" for k, v in row.items()])
            docs.append(Document(page_content=content, metadata=row))
    return docs