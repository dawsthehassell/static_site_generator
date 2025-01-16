import shutil
import os
from generate_page import generate_page

def file_copier(source="./static", destination="./public"):
    source = os.path.abspath(source)
    destination = os.path.abspath(destination)
    file_list = os.listdir(source)
    if os.path.exists(destination):
        if os.path.commonpath([os.getcwd(), os.path.abspath(destination)]) == os.getcwd():
            shutil.rmtree(destination, ignore_errors=True)
        else:
            raise ValueError("Refusing to delete destination outside of project scope.")
    shutil.rmtree(destination, ignore_errors=True)
    if not os.path.exists(destination):
        os.mkdir(destination)
    
    for item in file_list:
        is_directory = os.path.exists(os.path.join(source, item)) and not os.path.isfile(os.path.join(source, item))
        if is_directory:
            subdirectory_path = os.path.join(destination, item)
            if not os.path.exists(subdirectory_path):
                os.mkdir(subdirectory_path)
            file_copier(os.path.join(source, item), subdirectory_path)
        else:
            shutil.copy(os.path.join(source, item), os.path.join(destination, item))

def main():
    source = "./static"
    destination = "./public"
    file_copier(source, destination)
    print(f"Static files successfully copied from '{source}' to '{destination}'.")
    generate_page(
        from_path="content/index.md",
        template_path="template.html",
        dest_path="public/index.html"
    )

if __name__ == "__main__":
    main()