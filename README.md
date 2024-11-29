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
``python3 <path_to_output_file>``  

You may use the ```-h``` flag to see the various options that are available. 

The output will be written to stdout. Use the ```>``` or ```>>``` characters to send the output to a file.

### Options
```commandline
  -h, --help     show this help message and exit
  -a <reg_addr>  Addr of the reg to filter
  -l             Print lines
  -t             Print time
  -s             Print summary
```

### Example
Locate all frames with address 0xFC. Print line number, time and summary.  
```python3 data/spi_export -a 0xFC -l -t -s```

Output
```commandline
318 0.0032885 0xFC 0xFD
319 0.0032985 0xFD 0xFE
320 0.0033085 0xFE 0xFF

638 0.0066165 0xFC 0xFD
639 0.0066265 0xFD 0xFE
640 0.0066365 0xFE 0xFF

...

8318 0.0864885 0xFC 0xFD
8319 0.0864985 0xFD 0xFE
8320 0.0865085 0xFE 0xFF

-------------------------------------
Frames found =  26
Frames total =  1666
-------------------------------------
```