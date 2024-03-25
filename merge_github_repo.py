import os
import sys
from dotenv import load_dotenv

# 加载.env文件
dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(dotenv_path)


def find_files(root_dir, extensions, exclude):
    js_ts_md_files = []
    exclude_paths = [os.path.normpath(os.path.join(root_dir, ex)) for ex in exclude]
    
    for root, dirs, files in os.walk(root_dir):
        dirs[:] = [d for d in dirs if os.path.join(root, d) not in exclude_paths]  # 修改目录列表，排除不需要遍历的目录
        for file in files:
            if os.path.join(root, file) in exclude_paths:
                continue  # 排除在exclude列表中的文件
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
    prefix = 'MERGE_CODE_TOOL_'
    root_dir = os.getenv(f'{prefix}ROOT_DIR')
    repo_url = os.getenv(f'{prefix}REPO_URL')
    output_file = os.getenv(f'{prefix}OUTPUT_FILE')
    extensions = os.getenv(f'{prefix}EXTENSIONS', '').split(',')
    exclude = os.getenv(f'{prefix}EXCLUDE', '').split(',')
    
    if not all([root_dir, repo_url, output_file, extensions]):
        print("Some environment variables are missing. Please make sure all required environment variables are set.")
        sys.exit(1)
    
    files = find_files(root_dir, extensions, exclude)
    read_and_write_files(files, output_file, repo_url, root_dir)


if __name__ == "__main__":
    main()
