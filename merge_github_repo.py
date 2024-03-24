import os
import sys

def find_files(root_dir, extensions):
    js_ts_md_files = []
    for root, dirs, files in os.walk(root_dir):
        for file in files:
            for ext in extensions:
                if file.endswith(ext):
                    file_path = os.path.join(root, file)
                    js_ts_md_files.append(file_path)
                    break
    return js_ts_md_files

def get_relative_path(file_path, root_dir):
    return os.path.relpath(file_path, root_dir)

def read_and_write_files(files, output_file, repo_url, root_dir):
    with open(output_file, 'w') as output:
        for file_path in files:
            with open(file_path, 'r') as file:
                content = file.read()
                file_name = os.path.basename(file_path)
                relative_path = get_relative_path(file_path, root_dir)
                github_link = os.path.join(repo_url, 'blob/main/', relative_path)
                output.write(f"## {file_name}\n\nLink: [{github_link}]({github_link})\n\n```\n{content}\n```\n\n")

def main():
    if len(sys.argv) < 4:
        print("Usage: python script.py /path/to/your/github/repo https://github.com/username/repo output.md .js .ts")
        sys.exit(1)
        
    root_dir = sys.argv[1]
    repo_url = sys.argv[2]
    output_file = sys.argv[3]
    extensions = sys.argv[4:]
    
    files = find_files(root_dir, extensions)
    read_and_write_files(files, output_file, repo_url, root_dir)

if __name__ == "__main__":
    main()
