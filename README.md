# Digital Image Compressor
Final Project for Digital Image Class

Language: Python3

Operating System(s): Debian Buster (linux bash shell on Windows), &
Ubuntu 20.04 LTS (and maybe MX Linux 19.1)

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
5. Use Huffman coder (to be provided by MATLAB) to encode run-size
sequence; Do binary representation of the amplitude.
6. Calculate the bit rate of the compressed image.

**Decoder:**

1. Inverse quantization;
2. Inverse run-level coding and zig-zag scan.
3. Inverse DCT;
4. Compute the PSNR of the reconstructed image;

## Images

Images used in this project came from Unsplash, Creative Commons,
Wikicommons, and Reddit.

```
directories with "640" tag contain images of 640x640 size.

images/
├── 640-jpeg
│   ├── butterfly.jpeg
│   ├── empress.jpeg
│   ├── lithograph.jpeg
│   ├── purpleFlower.jpeg
│   └── sunflower.jpeg
├── 640-png
│   ├── giant.png
│   ├── lithograph.png
│   ├── robinWilliams.png
│   ├── rose.png
│   └── woman.png
├── analog_1.jpg
├── analog_2.jpg
├── analog_3.jpg
├── fanart_1.jpeg
├── fanart_2.jpeg
├── fanart_3.jpeg
├── jpeg
│   ├── comic.jpeg
│   ├── dog_cat.jpeg
│   ├── robot.jpeg
│   ├── twoDogsAndWoman.jpeg
│   └── twoWomen.jpeg
└── png
    ├── couchCat.png
    ├── holo.png
    ├── owlHat.png
    ├── SansUndertale.png
    └── scifi_cover.png

```
