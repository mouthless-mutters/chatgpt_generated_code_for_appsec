import os
import re

# Patterns to match routes for different Java frameworks
spring_route_pattern = re.compile(r"@(GetMapping|PostMapping|PutMapping|DeleteMapping|RequestMapping)\((.*?)\)")
jaxrs_route_pattern = re.compile(r"@Path\(\"(.*?)\"\)")
jaxrs_method_pattern = re.compile(r"@(GET|POST|PUT|DELETE)")
play_routes_pattern = re.compile(r"(GET|POST|PUT|DELETE)\s+(\/[^\s]*)")
spark_route_pattern = re.compile(r"(get|post|put|delete)\(\"(.*?)\"")
vaadin_route_pattern = re.compile(r"@Route\(\"(.*?)\"\)")
struts_action_pattern = re.compile(r"<action\s+name=\"(.*?)\"\s+class=\"(.*?)\"\s+method=\"(.*?)\"")
struts_annotation_pattern = re.compile(r"@Action\(\"(.*?)\"\)")
blade_route_pattern = re.compile(r"@(GetRoute|PostRoute|PutRoute|DeleteRoute)\(\"(.*?)\"\)")
micronaut_route_pattern = re.compile(r"@(Get|Post|Put|Delete)\(\"(.*?)\"\)")

def find_routes(file_content, framework):
    """
    Extracts all routes from a given file content based on the Java framework.
    :param file_content: String content of a Java file
    :param framework: The web framework being used (Spring, JAX-RS, Vaadin, Struts, etc.)
    :return: List of routes found
    """
    if framework == "spring":
        return spring_route_pattern.findall(file_content)
    elif framework == "jaxrs" or framework == "dropwizard":
        paths = jaxrs_route_pattern.findall(file_content)
        methods = jaxrs_method_pattern.findall(file_content)
        return zip(methods, paths)
    elif framework == "play":
        return play_routes_pattern.findall(file_content)
    elif framework == "spark":
        return spark_route_pattern.findall(file_content)
    elif framework == "vaadin":
        return vaadin_route_pattern.findall(file_content)
    elif framework == "struts":
        return struts_action_pattern.findall(file_content)
    elif framework == "struts-annotation":
        return struts_annotation_pattern.findall(file_content)
    elif framework == "blade":
        return blade_route_pattern.findall(file_content)
    elif framework == "micronaut":
        return micronaut_route_pattern.findall(file_content)
    return []

def search_routes_in_directory(root_dir):
    """
    Recursively searches for route definitions in Java files in a directory.
    Handles Spring, JAX-RS, Dropwizard, Vaadin, Struts, Play Framework, and Spark Java frameworks.
    :param root_dir: The root directory to search
    """
    for dirpath, _, filenames in os.walk(root_dir):
        for filename in filenames:
            if filename.endswith(".java") or filename.endswith("routes") or filename.endswith(".xml"):  # Search Java and XML files
                file_path = os.path.join(dirpath, filename)
                
                try:
                    with open(file_path, "r", encoding="utf-8") as f:
                        content = f.read()

                        # Detect framework based on typical patterns or content
                        if '@GetMapping' in content or '@RequestMapping' in content:
                            framework = 'spring'
                        elif '@Path' in content and ('@GET' in content or '@POST' in content):
                            framework = 'jaxrs'  # Also applies to Dropwizard
                        elif filename == 'routes':  # Play Framework routes file
                            framework = 'play'
                        elif 'get(' in content or 'post(' in content:
                            framework = 'spark'
                        elif '@Route' in content:
                            framework = 'vaadin'
                        elif 'struts.xml' in filename:
                            framework = 'struts'  # XML-based Struts config
                        elif '@Action' in content:
                            framework = 'struts-annotation'
                        elif '@GetRoute' in content or '@PostRoute' in content:
                            framework = 'blade'
                        elif '@Get' in content or '@Post' in content:
                            framework = 'micronaut'
                        else:
                            continue  # Skip if the framework can't be detected

                        routes = find_routes(content, framework)
                        
                        if routes:
                            print(f"\nIn file: {file_path} (Framework: {framework})")
                            for route in routes:
                                if isinstance(route, tuple):
                                    # Handle the route tuple (method, path)
                                    print(f"  Method: {route[0]}, Route: {route[1]}")
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
