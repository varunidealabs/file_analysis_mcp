from fastmcp import FastMCP, Context
from typing import Dict, List, Any
import os
from collections import Counter

# Create the MCP server
mcp = FastMCP(
    "File Analysis",
    dependencies=["fastmcp"],
    description="Tools for analyzing text files"
)

@mcp.tool()
def analyze_text(text: str) -> Dict[str, Any]:
    """
    Analyze text content and provide statistics.
    
    Args:
        text: The text content to analyze
        
    Returns:
        Dictionary with text statistics
    """
    # Calculate basic statistics
    char_count = len(text)
    word_count = len(text.split())
    line_count = len(text.splitlines())
    
    # Character frequency analysis
    char_freq = dict(Counter(text.lower()))
    
    # Word frequency analysis (simple)
    import re
    words = re.findall(r'\b\w+\b', text.lower())
    word_freq = dict(Counter(words).most_common(10))
    
    return {
        "statistics": {
            "character_count": char_count,
            "word_count": word_count,
            "line_count": line_count,
        },
        "character_frequency": char_freq,
        "top_words": word_freq
    }

@mcp.tool()
def read_file(file_path: str) -> str:
    """
    Read the contents of a text file.
    
    Args:
        file_path: Path to the file to read
        
    Returns:
        File contents as text
    """
    if not os.path.exists(file_path):
        return f"Error: File not found at {file_path}"
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        return f"Error reading file: {str(e)}"

@mcp.tool()
def list_files(directory: str = ".") -> Dict[str, List[str]]:
    """
    List files in a directory.
    
    Args:
        directory: Directory path to list files from (defaults to current directory)
        
    Returns:
        Dictionary with lists of files and directories
    """
    if not os.path.exists(directory):
        return {"error": f"Directory not found: {directory}"}
    
    try:
        contents = os.listdir(directory)
        files = [item for item in contents if os.path.isfile(os.path.join(directory, item))]
        dirs = [item for item in contents if os.path.isdir(os.path.join(directory, item))]
        
        return {
            "files": files,
            "directories": dirs
        }
    except Exception as e:
        return {"error": f"Error listing directory: {str(e)}"}

@mcp.resource("file://{file_path}")
def get_file_resource(file_path: str) -> str:
    """
    Access a file as a resource.
    
    Args:
        file_path: Path to the file
        
    Returns:
        File contents as text
    """
    return read_file(file_path)

def run():
    """Run the MCP server"""
    mcp.run()

if __name__ == "__main__":
    run()