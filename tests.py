from functions.get_files_info import get_files_info

def print_files_info(infos):
    for str in infos:
        print(str)

# def main():
#     print_files_info(get_files_info("calculator", "."))
#     print_files_info(get_files_info("calculator", "pkg"))
#     print_files_info(get_files_info("calculator", "/bin"))
#     print_files_info(get_files_info("calculator", "../"))

# if __name__ == "__main__":
#     main()


from functions.get_file_content import get_file_content
from functions.write_file import write_file
from functions.run_python import run_python_file

def main():
    print(get_files_info("calculator", "."))

if __name__ == "__main__":
    main()