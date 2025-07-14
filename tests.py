from functions.get_files_info import get_files_info, print_file_info

def main():
    print_file_info(get_files_info("calculator", "."))
    print_file_info(get_files_info("calculator", "pkg"))
    print_file_info(get_files_info("calculator", "/bin"))
    print_file_info(get_files_info("calculator", "../"))

if __name__ == "__main__":
    main()