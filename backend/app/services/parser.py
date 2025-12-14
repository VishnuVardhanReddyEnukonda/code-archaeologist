from tree_sitter import Language, Parser
import tree_sitter_python

# 1. Initialize the Parser (The "Scalpel")
PY_LANGUAGE = Language(tree_sitter_python.language())
parser = Parser(PY_LANGUAGE)

def extract_functions(code_bytes):
    """
    Scans the code and returns a list of every function found,
    including its name, the code content, and line numbers.
    """
    tree = parser.parse(code_bytes)
    root_node = tree.root_node
    
    functions = []
    
    # We walk through the AST (Abstract Syntax Tree) to find 'function_definition' nodes
    # This is much more robust than Regex
    for node in root_node.children:
        if node.type == 'function_definition':
            # Extract function name
            name_node = node.child_by_field_name('name')
            func_name = code_bytes[name_node.start_byte:name_node.end_byte].decode('utf8')
            
            # Extract the full code of the function
            func_code = code_bytes[node.start_byte:node.end_byte].decode('utf8')
            
            functions.append({
                "name": func_name,
                "code": func_code,
                "start_line": node.start_point[0],
                "end_line": node.end_point[0]
            })
            
    return functions