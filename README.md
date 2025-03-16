[![Pylint](https://github.com/devkgs/saleae_frame_analyzer/actions/workflows/pylint.yml/badge.svg?branch=main)](https://github.com/devkgs/saleae_frame_analyzer/actions/workflows/pylint.yml)

# saleae_frame_analyzer
A python script that extract SPI frames from Saleae Logic 2 App SPI export file.  


# Prerequisites
 - Saleae Logic 2 CSV output file
 - Python3

# Usage

## Generating output from Saleae Logic 2
See https://github.com/idaholab/Saleae_Output_Parser 

## Running the script
``python3 -- <path_to_output_file>``  

You may use the ```-h``` flag to see the various options that are available. 

The output will be written to stdout. Use the ```>``` or ```>>``` characters to send the output to a file.

## Options
```commandline
  -h, --help            show this help message and exit
  -a <reg_addr> [<reg_addr> ...] Addr(s) of the reg to filter
  -l                    Print lines
  -t                    Print time
  -s                    Print summary
```

## Example
Locate all frames with address 0x01:<br>
```python3 reg_parser.py data/spi_capture_example.csv -a 0x01```

Locate all frames with addresses 0x01 or 0x16:<br>
```python3 reg_parser.py data/spi_capture_example.csv -a 0x01 0x16```

# data directory
In data directory, there is spi capture examples.

saleae_spi_export.csv: 