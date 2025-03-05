import unittest
import argparse
import io
import sys
from unittest.mock import patch
from reg_parser import (
    add_arguments,
    DataByte,
    Protocol,
    SPIProtocol,
)

class TestRegParser(unittest.TestCase):

    def setUp(self):
        self.parser = argparse.ArgumentParser()
        add_arguments(self.parser)

    def test_add_arguments(self):
        args = self.parser.parse_args(['test.csv', '-a', '0x01', '0x02', '-l', '-t', '-s'])
        self.assertEqual(args.reg_addr, ['0x01', '0x02'])
        self.assertTrue(args.print_lines)
        self.assertTrue(args.print_time)
        self.assertTrue(args.print_summary)
        self.assertEqual(args.in_file, 'test.csv')

    def test_data_byte_str(self):
        data_byte = DataByte(data_out='0x02', data_in='0x01', time='0.123', line=42)
        self.assertEqual(str(data_byte), '0x01 0x02')

    def test_spi_protocol_parse_file(self):
        test_csv_content = """SPI,type,time,frame duration,mosi,miso
SPI,"enable",0.0001,8e-09,,
SPI,"result",0.0002,3.36e-06,0x01,0x03
SPI,"result",0.0003,3.352e-06,0x02,0x07
SPI,"disable",0.0004,8e-09,,
SPI,"enable",0.0005,8e-09,,
SPI,"result",0.0006,3.36e-06,0x02,0x06
SPI,"result",0.0007,3.352e-06,0x03,0x0E
SPI,"disable",0.0008,8e-09,,
SPI,"enable",0.0009,8e-09,,
SPI,"result",0.0010,3.36e-06,0x04,0x0C
SPI,"result",0.0011,3.352e-06,0x05,0x1C
SPI,"disable",0.0012,8e-09,,
"""
        with patch('argparse.ArgumentParser.parse_args', return_value=self.parser.parse_args(['test.csv', '-a', '0x01', '0x02'])):
            with patch('builtins.open', unittest.mock.mock_open(read_data=test_csv_content)) as mock_file:
                spi_protocol = SPIProtocol(self.parser.parse_args())
                spi_protocol.parse_file()
                self.assertEqual(len(spi_protocol.frames), 2)
                self.assertEqual(len(spi_protocol.frames[0]), 2)
                self.assertEqual(len(spi_protocol.frames[1]), 2)
                self.assertEqual(spi_protocol.frames[0][0].data_in, '0x01')
                self.assertEqual(spi_protocol.frames[0][0].data_out, '0x03')
                self.assertEqual(spi_protocol.frames[0][1].data_in, '0x02')
                self.assertEqual(spi_protocol.frames[0][1].data_out, '0x07')
                self.assertEqual(spi_protocol.frames[1][0].data_in, '0x02')
                self.assertEqual(spi_protocol.frames[1][0].data_out, '0x06')
                self.assertEqual(spi_protocol.frames[1][1].data_in, '0x03')
                self.assertEqual(spi_protocol.frames[1][1].data_out, '0x0E')
                self.assertEqual(spi_protocol.total_frames, 3)

    def test_spi_protocol_print_frames(self):
        test_csv_content = """SPI,type,time,frame duration,mosi,miso
SPI,"enable",0.0001,8e-09,,
SPI,"result",0.0002,3.36e-06,0x01,0x03
SPI,"result",0.0003,3.352e-06,0x02,0x07
SPI,"disable",0.0004,8e-09,,
"""
        with patch('argparse.ArgumentParser.parse_args', return_value=self.parser.parse_args(['test.csv', '-a', '0x01'])):
            with patch('builtins.open', unittest.mock.mock_open(read_data=test_csv_content)):
                spi_protocol = SPIProtocol(self.parser.parse_args(['test.csv', '-a', '0x01', '-l', '-t']))
                spi_protocol.parse_file()
                captured_output = io.StringIO()
                sys.stdout = captured_output
                spi_protocol.print_frames()
                sys.stdout = sys.__stdout__
                expected_output = "2 0.0002 0x01 0x03\n3 0.0003 0x02 0x07\n\n"
                self.assertEqual(captured_output.getvalue(), expected_output)

    def test_spi_protocol_print_summary(self):
        test_csv_content = """SPI,type,time,frame duration,mosi,miso
SPI,"enable",0.0001,8e-09,,
SPI,"result",0.0002,3.36e-06,0x01,0x03
SPI,"result",0.0003,3.352e-06,0x02,0x07
SPI,"disable",0.0004,8e-09,,
"""
        with patch('argparse.ArgumentParser.parse_args', return_value=self.parser.parse_args(['test.csv', '-a', '0x01'])):
            with patch('builtins.open', unittest.mock.mock_open(read_data=test_csv_content)):
                spi_protocol = SPIProtocol(self.parser.parse_args(['test.csv', '-a', '0x01']))
                spi_protocol.parse_file()
                captured_output = io.StringIO()
                sys.stdout = captured_output
                spi_protocol.print_summary()
                sys.stdout = sys.__stdout__
                expected_output = "-------------------------------------\nFrames found =  1\nFrames total =  1\n-------------------------------------\n"
                self.assertEqual(captured_output.getvalue(), expected_output)

if __name__ == '__main__':
    unittest.main()