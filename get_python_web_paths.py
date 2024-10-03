import os
import re

# Patterns to match routes for different frameworks
flask_route_pattern = re.compile(r"@app\.route\((.*?)\)")
django_url_pattern = re.compile(r"(path|re_path)\((.*?)\)")
fastapi_route_pattern = re.compile(r"@app\.(get|post|put|delete)\((.*?)\)")
tornado_route_pattern = re.compile(r"(\(r?\".*?\", .*?Handler\))")

def find_routes(file_content, framework):
    """
    Extracts all routes from a given file content based on the framework.
    :param file_content: String content of a Python file
    :param framework: The web framework being used (Flask, Django, FastAPI, Tornado)
    :return: List of routes found
    """
    if framework == "flask":
        return flask_route_pattern.findall(file_content)
    elif framework == "django":
        return django_url_pattern.findall(file_content)
    elif framework == "fastapi":
        return fastapi_route_pattern.findall(file_content)
    elif framework == "tornado":
        return tornado_route_pattern.findall(file_content)
    return []

def search_routes_in_directory(root_dir):
    """
    Recursively searches for route definitions in Python files in a directory.
    Handles Flask, Django, FastAPI, and Tornado frameworks.
    :param root_dir: The root directory to search
    """
    for dirpath, _, filenames in os.walk(root_dir):
        for filename in filenames:
            if filename.endswith(".py"):  # Only search in Python files
                file_path = os.path.join(dirpath, filename)
                
                try:
                    with open(file_path, "r") as f:
                        content = f.read()
                        
                        # Detect framework based on typical files or content
                        if 'flask' in content:
                            framework = 'flask'
                        elif filename == "urls.py" or 'django' in content:
                            framework = 'django'
                        elif 'fastapi' in content:
                            framework = 'fastapi'
                        elif 'tornado' in content:
                            framework = 'tornado'
                        else:
                            continue  # Skip if the framework can't be detected

                        routes = find_routes(content, framework)
                        
                        if routes:
                            print(f"\nIn file: {file_path} (Framework: {framework})")
                            for route in routes:
                                # Routes can be a tuple, print relevant info
                                if isinstance(route, tuple):
                                    print(f"  Route: {route[1]} (Method: {route[0]})")
                                else:
                                    print(f"  Route: {route}")
                except (UnicodeDecodeError, FileNotFoundError):
                    # Skipping files that can't be read (like binary or restricted files)
                    continue

if __name__ == "__main__":
    # Input directory path from the user
    root_directory = input("Enter the project directory path: ")
    # Search for routes
    search_routes_in_directory(root_directory)
