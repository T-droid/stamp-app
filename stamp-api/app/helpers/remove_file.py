
def remove_file(file_path):
    import os
    if os.path.exists(file_path):
        os.remove(file_path)