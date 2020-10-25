"""Class to extract composure cite parameters from function src code."""

from mdutils.mdutils import MdUtils


class CiteParameters:
    def __init__(self, cite_about, func_text_dict):

        self.func_text_dict = func_text_dict
        self.cite_about = cite_about

        self.cite_parameters = [
            "about '",
            "group '",
            "param '",
            "example '",
        ]  # , "about '", "about '"]

        self.main_write_md()

    def get_cite_values(self, func_name, func_str):

        self.mdFile.new_header(
            level=4,
            title="f() - " + func_name + ":",
            style="atx",
            add_table_of_contents="n",
        )

        cite_li = []
        for line in func_str.split("\n"):
            for cparam in self.cite_parameters:

                if cparam in line:
                    stripped_line = line.strip()
                    print("*", cparam, stripped_line)
                    cite_li.append(
                        stripped_line.strip("'")
                        .strip()
                        .replace(cparam, ">***" + cparam.strip("'").strip() + "***: ")
                    )
                    break

        self.mdFile.new_paragraph("\n".join(cite_li))

    def main_write_md(self):

        self.mdFile = MdUtils(file_name="example_markdown.md", title=self.cite_about)
        # self.mdFile.new_table_of_contents(table_title="Contents", depth=3)

        # all_funcs = list(self.func_text_dict.keys())

        all_funcs_li = [
            str(idx + 1).rjust(2, "0") + " - " + key
            for idx, key in enumerate(self.func_text_dict.keys())
        ]
        cat_all_funcs = "\n".join(all_funcs_li)
        print("cat_all_funcs", cat_all_funcs)

        self.mdFile.new_header(
            level=4, title="All functions", style="atx", add_table_of_contents="n"
        )
        self.mdFile.insert_code(
            cat_all_funcs,
            language="shell",
        )
        for key, value in self.func_text_dict.items():
            print("\n*~~~~~\n", key)  # , "\n", value)
            citey = self.get_cite_values(func_name=key, func_str=value)

            # formatted_func_md =

        self.mdFile.create_md_file()
