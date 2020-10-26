"""Gen-Bash-MkDoc main entrypoint"""

import os
import sys
import logging
import argparse
import errno
from cite_parameter import CiteParameters


def mkdir_if_none(dir_name):
    """Create specified directory if it does not exist."""

    try:
        os.makedirs(dir_name)
    except OSError as err:
        if err.errno != errno.EEXIST:
            raise


LOG = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, stream=sys.stdout)


def get_function_name(line_str):
    func_name = None
    if line.strip().endswith(("{", "}")):
        # print("line:", line)

        function_header = line.split()
        func_name = function_header[1]
        print("func_name:", func_name)
    return func_name


# function_list = []

if __name__ == "__main__":

    help_banner = "????????????????????"

    parser = argparse.ArgumentParser(
        description="Gen-Bash-MkDoc",
        usage="??????????????????????",
    )

    parser.add_argument(
        "-i",
        "--infiles",
        dest="infiles",
        help="Space seperated strings of Bash src code files",
        type=str,
        nargs="*",
        default=None,
        required=True,
    )

    parser.add_argument(
        "-o",
        "--out-dir",
        dest="out_dir",
        help="Folder to write processed documenatation to",
        type=str,
        default=None,
        required=True,
    )

    args = parser.parse_args()

    out_dir = args.out_dir
    mkdir_if_none(dir_name=out_dir)
    for infile_path in args.infiles:
        print(infile_path)

        # 1. get names of all functions in file
        func_name_list = []
        full_alias_str_list = []
        func_name = None
        cite_about = "Undefined. Add composure cite-about to shell script file"
        with open(infile_path, "r") as FHI:
            print("infile_path", infile_path)

            func_text_dict = {}
            src_text = text = FHI.read()
            # print(src_text)
            for line in src_text.split("\n"):
                # print("ulu", line)

                if line.startswith("function"):
                    func_name = get_function_name(line_str=line)
                    if func_name is not None:  # and (len(func_text_dict) == 0):
                        # first function
                        func_name_list.append(func_name)
                        func_text_dict[func_name] = line
                elif line.startswith(("about-plugin", "about-alias")):
                    cite_about = (
                        line.replace("about-plugin", "")
                        .replace("about-alias", "")
                        .replace("'", "")
                        .strip()
                    )
                elif line.startswith("alias"):
                    # pass alias into a container - write out full definition
                    alias_list = line.replace("alias ", "").strip().split("=")

                    alias_name = alias_list[0]
                    alias_cmd = alias_list[1]
                    alias_comment = ""
                    # Further split alias line using "#" because final column is a description
                    if "#" in alias_list[1]:
                        alias_list_lvl2 = alias_list[1].split("#")
                        alias_cmd = alias_list_lvl2[0]
                        alias_comment = alias_list_lvl2[1]

                    alias_fmtstr = (
                        f"| **{alias_name}** | {alias_cmd} | {alias_comment}\n"
                    )

                    full_alias_str_list.append(alias_fmtstr)

                else:
                    if func_name is not None:
                        func_text_dict[func_name] = (
                            func_text_dict[func_name] + "\n" + line
                        )
        print("\n\n ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        # for key, value in func_text_dict.items():
        #     print("\n*~~~~~\n", key)  # , "\n", value)
        citey = CiteParameters(
            cite_about=cite_about,
            func_text_dict=func_text_dict,
            full_alias_str_list=full_alias_str_list,
            src_file_path=infile_path,
            out_dir=out_dir,
        )

        print("\n\n ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        func_dep_dict = {}
        for key, value in func_text_dict.items():
            print("\n*~~~~~\n", key, "\n", value)
            for func_name in func_name_list:
                if func_name != key:  # exclude fuctions own name
                    if (func_name + " ") in value:
                        if key not in func_dep_dict:
                            # create new entry
                            func_dep_dict[key] = [func_name]
                        else:
                            # append to exiting list
                            if func_name not in func_dep_dict[key]:  # unique values
                                func_dep_dict[key].append(func_name)

                # print(line)

        print("\n\n ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")

        # ghf
        # |-- grep_history
        # |-- hist_nlines
        # `-- _unique_history
        #     |-- _add_line_numbers
        #     |-- _chop_first_column
        #     `-- _top_ten

        # def fmt_hier_string(idx, cf_len, cf_label, indent):
        #     if idx == cf_len - 1:
        #         return f"""{(indent+2) * " "}`-- {cf_label}\n"""

        #     return f"""{(indent+2) * " "}|-- {cf_label}\n"""

        # def bufferthis(fdep_list, hier_str, cf_len, indent):

        #     # level = 0
        #     for idx, cf_label in enumerate(fdep_list):
        #         hier_str += fmt_hier_string(
        #             idx=idx, cf_len=cf_len, cf_label=cf_label, indent=indent
        #         )
        #         if cf_label in func_dep_dict:
        #             # level += 4
        #             # for called_funcs in func_dep_dict[cf_label]:
        #             print("yabba - found", cf_label, func_dep_dict[cf_label])
        #             nest_hier_str = bufferthis(
        #                 fdep_list=func_dep_dict[cf_label],
        #                 hier_str=f"",
        #                 cf_len=len(cf_label),
        #                 indent=4,
        #             )
        #             hier_str += nest_hier_str
        #         # else:
        #         #     level -= 4
        #         # print("level", level)
        #     return hier_str

        # hier_frag_ascii_dict = {}
        # for key, called_funcs in func_dep_dict.items():
        #     print("xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx")
        #     print(key, len(called_funcs), called_funcs)
        #     hier_str = f"""* {key}\n"""

        #     ##############################
        #     cf_len = len(called_funcs)
        #     indent = 1

        #     hier_str += bufferthis(
        #         fdep_list=called_funcs, hier_str=hier_str, cf_len=cf_len, indent=indent
        #     )

        #     # for idx, cf_label in enumerate(called_funcs):
        #     #     hier_str += fmt_hier_string(
        #     #         idx=idx, cf_len=cf_len, cf_label=cf_label, indent=indent
        #     #     )
        #     #     if cf_label in func_dep_dict:
        #     #         for called_funcs in func_dep_dict[cf_label]:
        #     #         #bufferthis()

        #     print("\n\n\n", hier_str)
        #     hier_frag_ascii_dict[key] = hier_str
        #     hier_str = ""

        # print("\n\n\n\n ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        # for key, called_funcs in func_dep_dict.items():
        #     print("x", key)
        #     root_ascii = hier_frag_ascii_dict[key]
        #     for idx, cf_label in enumerate(called_funcs):
        #         if cf_label in hier_frag_ascii_dict:
        #             # insert sub-ascii into root_ascii
        #             print("boo", cf_label)
        #             # print(hier_frag_ascii_dic+t[cf_label])
        #             root_ascii = root_ascii.replace(
        #                 cf_label,
        #                 hier_frag_ascii_dict[cf_label].replace("\n", "\n" + (4 * " ")),
        #             )

        #             print(root_ascii)
        #             sys.exit(0)

        # for key, called_funcs in func_dep_dict.items():
        #     print()
        #     mystr = f"* {key}\n"
        #     mystr += "\n   *".join(called_funcs)

        #     print(mystr)