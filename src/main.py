"""Gen-Bash-MkDoc main entrypoint"""

import os
import sys
import logging
from cite_parameter import CiteParameters


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

    for infile in sys.argv[1:]:
        print(infile)

        # 1. get names of all functions in file
        func_name_list = []
        func_name = None

        with open(infile, "r") as FHI:
            print("infile", infile)

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
                    # elif (func_name is not None):
                    #     # terminate last function
                else:
                    if func_name is not None:
                        func_text_dict[func_name] = (
                            func_text_dict[func_name] + "\n" + line
                        )
        print("\n\n ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        # for key, value in func_text_dict.items():
        #     print("\n*~~~~~\n", key)  # , "\n", value)
        citey = CiteParameters(
            cite_about="History functions", func_text_dict=func_text_dict
        )

        # print("\n\n ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        # func_dep_dict = {}
        # for key, value in func_text_dict.items():
        #     print("\n*~~~~~\n", key, "\n", value)
        #     for func_name in func_name_list:
        #         if func_name != key:  # exclude fuctions own name
        #             if (func_name + " ") in value:
        #                 if key not in func_dep_dict:
        #                     # create new entry
        #                     func_dep_dict[key] = [func_name]
        #                 else:
        #                     # append to exiting list
        #                     if func_name not in func_dep_dict[key]:  # unique values
        #                         func_dep_dict[key].append(func_name)

        #         # print(line)

        # print("\n\n ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        # for key, value in func_dep_dict.items():
        #     print(key, len(value), value)