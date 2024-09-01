import os 

# 로컬 파일 삭제


def delete_local_files(directory):
    for root, dirs, files in os.walk(directory, topdown=False):
        for file in files:
            file_path = os.path.join(root, file)
            os.remove(file_path)
            print(f"Deleted local file: {file_path}")

        # 빈 디렉토리 삭제
        for dir in dirs:
            dir_path = os.path.join(root, dir)
            os.rmdir(dir_path)
            print(f"Deleted local directory: {dir_path}")
