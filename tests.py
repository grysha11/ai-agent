# from functions.get_files_info import get_files_info

# def print_files_info(infos):
#     for str in infos:
#         print(str)

# def main():
#     print_files_info(get_files_info("calculator", "."))
#     print_files_info(get_files_info("calculator", "pkg"))
#     print_files_info(get_files_info("calculator", "/bin"))
#     print_files_info(get_files_info("calculator", "../"))

# if __name__ == "__main__":
#     main()


from functions.get_file_content import get_file_content

def main():
    # print(get_file_content("calculator", "lorem.txt"))
    # print(f"Len is : {len(get_file_content("calculator", "lorem.txt"))}")
    print(get_file_content("calculator", "main.py"))
    print(get_file_content("calculator", "pkg/calculator.py"))
    print(get_file_content("calculator", "/bin/cat"))
    print(get_file_content("calculator", "pkg/does_not_exist.py"))

if __name__ == "__main__":
    main()