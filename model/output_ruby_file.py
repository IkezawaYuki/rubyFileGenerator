import logging

h = logging.FileHandler("log.txt")
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger.addHandler(h)


def ruby_source_write(string_list):
    with open("test.txt", "w+") as f:
        with open("model/template/header.txt", "r") as r:
            header = r.read()
            f.write(header)

        f.write("\n".join(string_list))

        with open("model/template/footer.txt", "r") as r:
            footer = r.read()
            f.write(footer)


def write_batch_file(string_list):
    pass


def execute_output(string_list):
    ruby_source_write(string_list)
    write_batch_file(string_list)