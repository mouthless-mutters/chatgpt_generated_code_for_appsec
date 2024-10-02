import os
import re
import subprocess
import git
import shutil

# Clone the repository
def clone_repo(repo_url, repo_dir='cloned_repo'):
    # Clean up the previous repo if exists
    if os.path.exists(repo_dir):
        shutil.rmtree(repo_dir)

    try:
        print(f"Cloning the repository from {repo_url}...")
        git.Repo.clone_from(repo_url, repo_dir)
        print("Repository cloned successfully.")
    except Exception as e:
        print(f"Error cloning repository: {e}")
        return None
    return repo_dir

# Language-specific deserialization patterns
def get_insecure_deserialization_patterns():
    return {
        # Python
        '.py': [
            r'pickle\.load', r'pickle\.loads',
            r'cPickle\.load', r'cPickle\.loads',
            r'yaml\.load', r'eval\(', r'json\.load',
            r'json\.loads', r'marshal\.load', r'marshal\.loads',
            r'shelve\.open'
        ],
        # Java
        '.java': [
            r'ObjectInputStream\.readObject',
            r'XMLDecoder\.readObject'
        ],
        # JavaScript (Node.js)
        '.js': [
            r'JSON\.parse',  # Can be insecure if used with unsanitized data
            r'eval\(',       # Dangerous if used improperly
            r'vm\.runInContext', r'vm\.runInNewContext',  # Node.js VM eval-like
        ],
        # PHP
        '.php': [
            r'unserialize\(',   # PHP's unserialize function
            r'json_decode',     # If not sanitized properly
            r'eval\(',          # Risky in any language
        ],
        # Ruby
        '.rb': [
            r'Marshal\.load', r'Marshal\.restore',  # Ruby deserialization
            r'YAML\.load', r'YAML\.parse',          # Unsafe YAML deserialization
            r'eval\('                                # Risky eval
        ],
        # C#
        '.cs': [
            r'BinaryFormatter\.Deserialize',
            r'JavaScriptSerializer\.Deserialize',
            r'XmlSerializer\.Deserialize'
        ],
        # C++
        '.cpp': [
            r'boost::archive::text_iarchive',  # Boost serialization
            r'boost::archive::binary_iarchive'
        ]
    }

# Scan files for insecure deserialization patterns
def scan_for_insecure_deserialization(repo_dir):
    patterns = get_insecure_deserialization_patterns()
    results = []

    # Scan each file for deserialization patterns
    for subdir, dirs, files in os.walk(repo_dir):
        for file in files:
            filepath = os.path.join(subdir, file)
            file_ext = os.path.splitext(file)[1]
            
            # Get patterns based on file extension
            if file_ext in patterns:
                with open(filepath, 'r', encoding='utf-8') as f:
                    try:
                        content = f.read()
                        for pattern in patterns[file_ext]:
                            if re.search(pattern, content):
                                results.append((filepath, pattern))
                    except Exception as e:
                        print(f"Error reading file {filepath}: {e}")
    
    return results

# Main function
def main():
    repo_url = input("Enter the Git repository URL: ")
    repo_dir = clone_repo(repo_url)
    
    if repo_dir:
        print("Scanning repository for insecure deserialization vulnerabilities...")
        results = scan_for_insecure_deserialization(repo_dir)
        
        if results:
            print("Potential insecure deserialization flaws found:")
            for filepath, pattern in results:
                print(f"File: {filepath}, Pattern: {pattern}")
        else:
            print("No insecure deserialization flaws found.")
        
        # Clean up cloned repo after scanning
        shutil.rmtree(repo_dir)
    else:
        print("Failed to clone the repository. Exiting.")

if __name__ == "__main__":
    main()
