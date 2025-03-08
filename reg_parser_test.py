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


#@unittest.skip("...")
class TestRegParser(unittest.TestCase):

    def setUp(self):
        self.parser = argparse.ArgumentParser()
        add_arguments(self.parser)

    def test_spi_protocol_single_address_count(self):
        test_csv_content = """SPI,type,time,frame duration,mosi,miso
SPI,"enable",0.0001,8e-09,,
SPI,"result",0.0002,3.36e-06,0x01,0x03
SPI,"result",0.0003,3.352e-06,0x02,0x07
SPI,"disable",0.0004,8e-09,,
SPI,"enable",0.0005,8e-09,,
SPI,"result",0.0006,3.36e-06,0x01,0x06
SPI,"result",0.0007,3.352e-06,0x03,0x0E
SPI,"disable",0.0008,8e-09,,
SPI,"enable",0.0009,8e-09,,
SPI,"result",0.0010,3.36e-06,0x01,0x0C
SPI,"result",0.0011,3.352e-06,0x05,0x1C
SPI,"disable",0.0012,8e-09,,
SPI,"enable",0.0013,8e-09,,
SPI,"result",0.0014,3.36e-06,0x01,0x0F
SPI,"result",0.0015,3.352e-06,0x06,0x23
SPI,"disable",0.0016,8e-09,,
"""
        with patch('argparse.ArgumentParser.parse_args', return_value=self.parser.parse_args(['spi_capture_test.csv', '-a', '0x01'])):
            with patch('builtins.open', unittest.mock.mock_open(read_data=test_csv_content)):
                spi_protocol = SPIProtocol(self.parser.parse_args())
                spi_protocol.parse_file()
                count = 0
                for frame in spi_protocol.frames:
                    #for data_byte in frame:     # TODO fix it is wrong
                    #    if data_byte.data_in == '0x01':
                    if (frame[0].data_in == '0x01'):
                            count += 1
                self.assertEqual(4, count)

    def test_spi_protocol_single_address_not_found(self):
        test_csv_content = """SPI,type,time,frame duration,mosi,miso
SPI,"enable",0.0001,8e-09,,
SPI,"result",0.0002,3.36e-06,0x02,0x03
SPI,"result",0.0003,3.352e-06,0x03,0x07
SPI,"disable",0.0004,8e-09,,
"""
        with patch('argparse.ArgumentParser.parse_args', return_value=self.parser.parse_args(['spi_capture_test.csv', '-a', '0x01'])):
            with patch('builtins.open', unittest.mock.mock_open(read_data=test_csv_content)):
                spi_protocol = SPIProtocol(self.parser.parse_args())
                spi_protocol.parse_file()
                self.assertEqual(len(spi_protocol.frames), 0)

    def test_spi_protocol_multiple_address_count(self):
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
SPI,"result",0.0010,3.36e-06,0x03,0x0C
SPI,"result",0.0011,3.352e-06,0x05,0x1C
SPI,"disable",0.0012,8e-09,,
SPI,"enable",0.0013,8e-09,,
SPI,"result",0.0014,3.36e-06,0x04,0x0F
SPI,"result",0.0015,3.352e-06,0x06,0x23
SPI,"disable",0.0016,8e-09,,
"""
        with patch('argparse.ArgumentParser.parse_args', return_value=self.parser.parse_args(['spi_capture_test.csv', '-a', '0x01', '0x02'])):
            with patch('builtins.open', unittest.mock.mock_open(read_data=test_csv_content)):
                spi_protocol = SPIProtocol(self.parser.parse_args())
                spi_protocol.parse_file()
                count = 0
                for frame in spi_protocol.frames:
                    if (frame[0].data_in == '0x01') | (frame[0].data_in == '0x02'):
                            count += 1
                self.assertEqual(2, count)



if __name__ == '__main__':
    unittest.main()