"""
Doc

input file:
columns: spi, type, time, frame duration, mosi, miso
type: enable, result, disable

"""

import argparse
from abc import ABC, abstractmethod

def add_arguments(argument_parser: argparse.ArgumentParser) -> None:
    """
    Add arguments to arg parser.
    :param argument_parser:
    :return:
    """
    argument_parser.description = "A python program to parse Saleae Logic Analyzer 2 export files."
    argument_parser.add_argument('-a', dest='reg_addr', metavar='<reg_addr>',
                                 help="Addr of the reg to filter")
    argument_parser.add_argument('-l', action='store_true', dest='print_lines', help='Print lines')
    argument_parser.add_argument('-t', action='store_true', dest='print_time', help='Print time')
    argument_parser.add_argument('-s', action='store_true', dest='print_summary',
                                 help='Print summary')
    argument_parser.add_argument(dest='in_file', metavar='FILE', help="Saleae export data file")

class DataByte():
    """
    Handle result data for one byte
    """
    def __init__(self, data_out='', data_in='', time='', line=0):
        self.data_out = data_out
        self.data_in = data_in
        self.time = time
        self.line = line

    def __str__(self):
        return f"{self.data_in} {self.data_out}"

class Protocol(ABC):
    """
    Protocol abstract class.
    """
    def __init__(self, args):
        self.file = args.in_file
        self.addr_filter = args.reg_addr
        self.arg_print_line = args.print_lines
        self.arg_print_time = args.print_time
        self.frames = []
        self.total_frames = 0

    @abstractmethod
    def read_file(self):
        """
        Read the complete file and store result in frames variable
        :return:
        """
        pass

    @abstractmethod
    def print_frames(self):
        """
        Print the data of the variable frames
        :return:
        """
        pass

    def print_summary(self):
        """
        
        :return:
        """
        print("-------------------------------------")
        print("Frames found = ", len(self.frames))
        print("Frames total = ", self.total_frames)
        print("-------------------------------------")


class SPIProtocol(Protocol):
    """
    SPI specific protocol
    """
    def __init__(self, args):
        super().__init__(args)
        self.current_frame = []
        #self.frames = []

    def read_file(self):
        first_frame = True
        line_number = 0
        addr_detected = False
        with open(self.file, 'r') as infile:
            next(infile)  # Skip the first line
            line_number = line_number + 1
            for line in infile:
                line = line.rstrip()  # remove whitespaces
                line_number = line_number + 1
                splitted_line = line.split(',')  # to array
                if splitted_line[1] == '"enable"':
                    enable_detected = True
                    self.total_frames += 1
                elif splitted_line[1] == '"disable"':
                    if addr_detected :
                        self.frames.append(self.current_frame[:])
                        self.current_frame.clear()
                    enable_detected = False
                    first_frame = True
                    addr_detected = False
                elif splitted_line[1] == '"result"':
                    if enable_detected:
                        if first_frame:
                            if splitted_line[4] == self.addr_filter:
                                self.current_frame.append(DataByte(data_in = splitted_line[4],
                                                                   data_out = splitted_line[5],
                                                                   time = splitted_line[2],
                                                                    line=line_number))
                                addr_detected = True
                            first_frame = False
                        else:
                            if addr_detected:
                                self.current_frame.append(DataByte(data_in = splitted_line[4],
                                                                   data_out = splitted_line[5],
                                                                   time = splitted_line[2],
                                                                    line=line_number))

    def print_frames(self):
        for element in self.frames:
            for data_byte in element:
                output = [data_byte.data_in, data_byte.data_out]
                if self.arg_print_time:
                    output.insert(0, data_byte.time)
                if self.arg_print_line:
                    output.insert(0, data_byte.line)
                print(*output)
            print() # a new line to improve visibility

if __name__ == "__main__":
    parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter)
    add_arguments(parser)
    args = parser.parse_args()

    analyzer = SPIProtocol(args)
    analyzer.read_file()
    analyzer.print_frames()

    if args.print_summary:
        analyzer.print_summary()
