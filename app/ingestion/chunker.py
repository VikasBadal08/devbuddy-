from dataclasses import dataclass
from tree_sitter import Language,Parser
import tree_sitter_python

@dataclass
class Chunk:
    file_path: str
    chunk_type: str
    name: str
    start_line: int
    end_line: int
    content: str

python_language=Language(tree_sitter_python.language())

def create_parser():
    return Parser(python_language)

def extract_chunks(code: bytes) -> list[dict]:
    parser = create_parser()
    tree = parser.parse(code)

    chunks = []

    def traverse(node, inside_class=False):

        if node.type == "class_definition":

            name_node = node.child_by_field_name("name")

            name = (
                name_node.text.decode("utf-8")
                if name_node
                else "unknown"
            )

            chunks.append(
                {
                    "type": node.type,
                    "name": name,
                    "start_line": node.start_point.row + 1,
                    "end_line": node.end_point.row + 1,
                    "content": node.text.decode("utf-8"),
                }
            )

            for child in node.children:
                traverse(child, inside_class=True)

            return

        if node.type == "function_definition":

            name_node = node.child_by_field_name("name")

            name = (
                name_node.text.decode("utf-8")
                if name_node
                else "unknown"
            )

            chunks.append(
                {
                    "type": node.type,
                    "name": name,
                    "start_line": node.start_point.row + 1,
                    "end_line": node.end_point.row + 1,
                    "content": node.text.decode("utf-8"),
                }
            )

            # Don't extract nested functions separately
            return

        for child in node.children:
            traverse(child, inside_class)

    traverse(tree.root_node)

    return chunks

def extract_chunks_from_file(file_path:str)-> list[dict]:
    with open(file_path,"rb") as file:
        code =file.read()

    chunks=extract_chunks(code)

    for chunk in chunks:
        chunk["file_path"]=file_path

    return chunks


from pathlib import Path

EXCLUDED_DIRS = {
    ".git",
    ".venv",
    "venv",
    "__pycache__",
    "node_modules",
}

def process_repository(repo_path:str) -> list[dict]:
    repo=Path(repo_path)
    all_chunks=[]

    for file_path in repo.rglob("*.py"):
         # Check whether any parent directory should be excluded
        if any(part in EXCLUDED_DIRS for part in file_path.parts):
            continue


        try:
            chunks = extract_chunks_from_file(str(file_path))
            all_chunks.extend(chunks)
        except Exception as e:
            print(f"skipping {file_path}: {e}")
    return all_chunks