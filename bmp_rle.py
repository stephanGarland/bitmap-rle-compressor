import argparse
import os
import pprint
import re

def make_args():
    args_parser = argparse.ArgumentParser(
        prog="bmp_rle.py",
        description="Create a bitmap index from a list")
    args_parser.add_argument("data",
                            metavar="data",
                            nargs="*",
                            type=float,
                            help="Input to convert in space-separated values")
    args_parser.add_argument("-p",
                            "--pprint",
                            action="store_true",
                            help="Output with pretty-printer")
    args_parser.add_argument("-c",
                            "--comp",
                            action="store_true",
                            help="Output only the compressed bitmap index")
    args_parser.add_argument("-u",
                            "--uncomp",
                            action="store_true",
                            help="Output only the uncompressed bitmap index")
    args_parser.add_argument("-t",
                             "--test",
                             action="store_true",
                             help="Run a test with known data (no further args are accepted)")
    args = args_parser.parse_args()
    return args


def make_bmp(column):
    column_bmp = []
    column_str = ""
    for i in range(len(column)):
        for j in range(len(column)):
            if column[j] == column[i]:
                column_str = column_str + "1"
            else:
                column_str = column_str + "0"
        column_bmp.append(column_str)
        column_str = ""
    return column_bmp


def dec_to_bin(n):
    return bin(n).replace("0b", "")


def zero_regexer(uncompressed_input):
    regex = r"1|(0+1)"
    matches = re.finditer(regex, uncompressed_input, re.MULTILINE)
    return matches


def make_comp_bmp(col_lst):
    buf_list = []
    for x in col_lst:
        buf = ""
        matches = zero_regexer(x)
        group_list = []

        for match in matches:
            group_list.append(match.group())

        for group in group_list:
            if group == "1":
                tmp = "00"
            else:
                num_zeros = group.count("0")
                num_zeros_bin = dec_to_bin(num_zeros)
                len_num_zeros_bin = len(num_zeros_bin) - 1
                tmp = (len_num_zeros_bin * "1") + "0" + num_zeros_bin
            buf = buf + tmp
            if not buf == "00":
                buf = buf.rstrip("0")
        buf_list.append(buf)
    return buf_list


def run_test():
    raw = [2.66, 2.10, 1.42, 2.80, 3.20, 3.20,
           2.20, 2.20, 2.00, 2.80, 1.86, 2.80]
    ref_uncomp = ["100000000000",
                  "010000000000",
                  "001000000000",
                  "000100000101",
                  "000011000000",
                  "000011000000",
                  "000000110000",
                  "000000110000",
                  "000000001000",
                  "000100000101",
                  "000000000010",
                  "000100000101"]
    ref_comp = ["00",
                "01",
                "101",
                "101111010101",
                "1101",
                "1101",
                "11011",
                "11011",
                "11101",
                "101111010101",
                "1110101",
                "101111010101"]
    test_uncomp = make_bmp(raw)
    test_comp = make_comp_bmp(test_uncomp)

    def results(test_inp, ref_inp):
        for x, y in list(zip(test_inp, ref_inp)):
            print("Expected:  " + y)
            print("Actual  :  " + x)
            print("\n")
        try:
            assert test_inp == ref_inp
            print("INFO: Test passed!\n")
        except AssertionError:
            print("ERROR: Test failed!\n")
    
    results(test_uncomp, ref_uncomp)
    results(test_comp, ref_comp)


def return_raw(raw):
    return "".join("\n{}".format(x) for x in raw)


if __name__ == "__main__":
    args = make_args()
    if args.test:
        run_test()
        raise SystemExit
    if not args.data:
        raise SystemExit
    pp = pprint.PrettyPrinter(indent=4)
    uncomp = make_bmp(args.data)
    comp = make_comp_bmp(uncomp)
    if args.comp:
        print("\nCompressed:\n")
        if args.pprint:
            pp.pprint(comp)
        else:
            print(return_raw(comp))
        raise SystemExit
    if args.uncomp:
        print("\nUncompressed:\n")
        if args.pprint:
            pp.pprint(uncomp)
        else:
            print(return_raw(uncomp))
        raise SystemExit
    else:
        if args.pprint:
            print("\nUncompressed:\n")
            pp.pprint(uncomp)
            print("\nCompressed:\n")
            pp.pprint(comp)
        else:
            print("\nUncompressed:\n")
            print(return_raw(uncomp))
            print("\nCompressed:\n")
            print(return_raw(comp))
