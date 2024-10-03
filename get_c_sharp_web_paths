import os
import re

# Extended patterns to match routes for different C# frameworks
aspnet_route_pattern = re.compile(r"\[(HttpGet|HttpPost|HttpPut|HttpDelete|HttpPatch|Route)\(\"(.*?)\"\)\]")
aspnet_class_route_pattern = re.compile(r"\[Route\(\"(.*?)\"\)\]")  # For class-level routes
minimal_api_pattern = re.compile(r"Map(Get|Post|Put|Delete|Patch)\(\"(.*?)\",")
nancyfx_route_pattern = re.compile(r"(Get|Post|Put|Delete)\[\"(.*?)\"\]")
servicestack_route_pattern = re.compile(r"\[Route\(\"(.*?)\"\)\]")
wcf_route_pattern = re.compile(r"\[(WebGet|WebInvoke)\(.*?UriTemplate=\"(.*?)\"\)\]")
openrasta_route_pattern = re.compile(r"\.AtUri\(\"(.*?)\"\)")
simpleweb_route_pattern = re.compile(r"(Get|Post|Put|Delete)\(\"(.*?)\"\)")  # Simple.Web convention
owin_route_pattern = re.compile(r"app\.Use\((.*?)\)")  # Common for OWIN-based routing

def find_routes(file_content, framework):
    """
    Extracts all routes from a given file content based on the C# framework.
    :param file_content: String content of a C# file
    :param framework: The web framework being used (ASP.NET, NancyFX, ServiceStack, WCF, OpenRasta, etc.)
    :return: List of routes found
    """
    if framework == "aspnet":
        routes = aspnet_route_pattern.findall(file_content)
        class_routes = aspnet_class_route_pattern.findall(file_content)
        # Handle both method-level and class-level routes for ASP.NET
        return routes, class_routes
    elif framework == "minimalapi":
        return minimal_api_pattern.findall(file_content), []
    elif framework == "nancyfx":
        return nancyfx_route_pattern.findall(file_content), []
    elif framework == "servicestack":
        return servicestack_route_pattern.findall(file_content), []
    elif framework == "wcf":
        return wcf_route_pattern.findall(file_content), []
    elif framework == "openrasta":
        return openrasta_route_pattern.findall(file_content), []
    elif framework == "simpleweb":
        return simpleweb_route_pattern.findall(file_content), []
    elif framework == "owin":
        return owin_route_pattern.findall(file_content), []
    return [], []

def search_routes_in_directory(root_dir):
    """
    Recursively searches for route definitions in C# files in a directory.
    Handles ASP.NET, Minimal APIs, NancyFX, ServiceStack, WCF, OpenRasta, Simple.Web, and OWIN frameworks.
    :param root_dir: The root directory to search
    """
    for dirpath, _, filenames in os.walk(root_dir):
        for filename in filenames:
            if filename.endswith(".cs"):  # Only search in C# files
                file_path = os.path.join(dirpath, filename)
                
                try:
                    with open(file_path, "r", encoding="utf-8") as f:
                        content = f.read()

                        # Detect framework based on typical patterns or content
                        if '[HttpGet' in content or '[Route' in content:
                            framework = 'aspnet'
                        elif 'MapGet' in content or 'MapPost' in content:
                            framework = 'minimalapi'
                        elif 'Get["' in content or 'Post["' in content:
                            framework = 'nancyfx'
                        elif '[Route("' in content:
                            framework = 'servicestack'
                        elif '[WebGet' in content or '[WebInvoke' in content:
                            framework = 'wcf'
                        elif '.AtUri(' in content:
                            framework = 'openrasta'
                        elif 'Simple.Web' in content:
                            framework = 'simpleweb'
                        elif 'app.Use(' in content:
                            framework = 'owin'
                        else:
                            continue  # Skip if the framework can't be detected

                        routes, class_routes = find_routes(content, framework)
                        
                        if routes or class_routes:
                            print(f"\nIn file: {file_path} (Framework: {framework})")
                            # Handle class-level routes (like in ASP.NET)
                            if class_routes:
                                for class_route in class_routes:
                                    print(f"  Class-level Route: {class_route}")
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
