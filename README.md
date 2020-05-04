# DigitalImageCompressor
Final Project for Digital Image Class

Language: Python3
Operating System(s): Debian Buster (linux bash shell on Windows), & Ubuntu 20.04 LTS (and maybe MX Linux 19.1)
Editors: Emacs, Vim, & Nano

## Instruction

**Due May 12th 11 AM**

**Objective: _develop a DCT-based image compression system._**

The system will have the following modules:

**Encoder:**

1. 8*8 DCT transform of the image (to be implemented by yourself);
2. Uniform quantization;
3. Zig-zag scan (use a table) and run-level coding;
4. Size + amplitude representation of the non-zero coefficients;
5. Use Huffman coder (to be provided by MATLAB) to encode run-size sequence; Do binary representation of the amplitude.
6. Calculate the bit rate of the compressed image.

**Decoder:**

1. Inverse quantization;
2. Inverse run-level coding and zig-zag scan.
3. Inverse DCT;
4. Compute the PSNR of the reconstructed image;
