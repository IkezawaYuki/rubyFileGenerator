import logging

h = logging.FileHandler("log.txt")
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger.addHandler(h)


def ruby_source_write(target_path_rb, string_list):
    logger.info("ruby_source_write start: " + str(target_path_rb))
    target_path_rb += ".rb"
    with open(target_path_rb, "w+") as f:
        with open("template/header.txt", "r") as r:
            header = r.read()
            f.write(header)
            
        f.write("\n".join(string_list))

        with open("template/footer.txt", "r") as r:
            footer = r.read()
            f.write(footer)
    logger.info("ruby_source_write end.")


def write_batch_file(target_path_bat, string_list):
    logger.info("write_batch_file start: " + str(target_path_bat))
    target_path_bat += ".bat"
    with open(target_path_bat, "w") as f:
        pass
    logger.info("write_batch_file end.")


def execute_output(output_taget_path, page, string_list):
    taget_path = output_taget_path + "_" + str(page)
    ruby_source_write(taget_path, string_list)
    write_batch_file(taget_path, string_list)