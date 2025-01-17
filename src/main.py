import shutil
import os
from generate_page import generate_page
from generate_pages_recursive import generate_pages_recursive

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
    template_path = "template.html"
    content_dir = "content"
    public_dir = "public"
    generate_pages_recursive(content_dir, template_path, public_dir)

if __name__ == "__main__":
    main()