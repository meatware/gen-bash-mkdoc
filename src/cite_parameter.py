"""Class to extract composure cite parameters from function src code."""

from mdutils.mdutils import MdUtils


class CiteParameters:
    def __init__(
        self, cite_about, func_text_dict, full_alias_str_list, src_file_path, out_dir
    ):

        self.cite_about = cite_about
        self.func_text_dict = func_text_dict
        self.full_alias_str_list = full_alias_str_list
        self.src_file_path = src_file_path
        self.out_dir = out_dir

        self.cite_parameters = [
            "about '",
            "group '",
            "param '",
            "example '",
        ]  # , "about '", "about '"]

        self.main_write_md()

    def write_func_section(
        self,
    ):

        self.mdFile.new_header(
            level=4, title="All functions", style="atx", add_table_of_contents="n"
        )

        all_funcs_li = [
            str(idx + 1).rjust(2, "0") + " - " + key
            for idx, key in enumerate(self.func_text_dict.keys())
        ]
        cat_all_funcs = "\n".join(all_funcs_li)
        self.mdFile.insert_code(
            cat_all_funcs,
            language="shell",
        )

        for func_name, func_str in self.func_text_dict.items():
            print("\n*~~~~~\n", func_name)  # , "\n", func_str)

            self.mdFile.new_paragraph("******")
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
                            .replace(
                                cparam, ">***" + cparam.strip("'").strip() + "***: "
                            )
                        )
                        break
            self.mdFile.new_paragraph("\n".join(cite_li))

    def write_aliases_section(self):
        self.mdFile.new_header(
            level=3, title="Aliases", style="atx", add_table_of_contents="n"
        )

        mytable = ""
        mytable += "| **Alias Name** | **Code** | **Descripion** |\n"
        mytable += "| :------------- |:-------------:| -----:|\n"
        for myalias in self.full_alias_str_list:
            mytable += myalias  # "| **" + ppass + "** | " + pp_dict[stack] + " |\n"
        # for fmtted_alias in self.full_alias_str_list:
        #     self.mdFile.new_paragraph(fmtted_alias)

        self.mdFile.new_paragraph(mytable)

    def main_write_md(self):

        infile_path_name = self.src_file_path.split("/")
        outfile_path = self.out_dir + "/" + infile_path_name[-1].replace("*.sh", "md")

        self.mdFile = MdUtils(file_name=outfile_path, title=self.cite_about)
        self.mdFile.new_paragraph(f"***(in {self.src_file_path})***")

        ### Process functions
        if len(self.func_text_dict) > 0:
            self.write_func_section()

        ### Process aliases
        self.write_aliases_section()

        ### Write out .md file
        self.mdFile.create_md_file()
