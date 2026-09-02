# Offline Signature Matching Using LCS

A **Design and Analysis of Algorithms project** that compares handwritten signature images using the **Longest Common Subsequence (LCS)** algorithm.

The system converts signature images into compact 16-character representations and uses LCS with Dynamic Programming to calculate their similarity.

**Note:** This is an educational prototype and not a production-grade biometric verification system.

## Workflow
Signature Images
       ↓
Grayscale + Resize (64×64)
       ↓
Binary Matrix
       ↓
4×4 Block Compression
       ↓
16×16 Matrix
       ↓
Row & Column Density
       ↓
16-Character Hex String
       ↓
LCS Algorithm
       ↓
Similarity Score


##  Technologies
* **Python**
* **Pillow (PIL)** – image processing
* **Dynamic Programming** – LCS
* **Object-Oriented Programming**

## How It Works
1. The signature image is converted to grayscale and resized to **64×64**.
2. Pixels are converted into a binary matrix (`1 = ink`, `0 = background`).
3. The matrix is compressed from **64×64 → 16×16** using 4×4 blocks.
4. Row and column ink densities are calculated.
5. These values are quantized into a **16-character hexadecimal string**.
6. LCS is applied to the two strings.
7. Similarity is calculated as:
Similarity (%) = (LCS Length / 16) × 100


##  Project Structure

LCS-Signature-Matching/
│
├── main.py
├── signature1.jpeg
├── signature2.jpeg
├── requirements.txt
└── README.md

##  Setup
Install the required library:
python -m pip install Pillow

Run the program:
python main.py
Place your two signature images in the same folder as `main.py` and name them:

signature1.jpeg
signature2.jpeg


##  Example
Signature 1: 015AF87025978753
Signature 2: 025AF87024978753

LCS Length: 15
Similarity Score: 93.75%

Result: Signatures are highly similar
*Actual results depend on the input images.*

##  Future Scope
* Test with multiple genuine and forged signatures
* Improve rotation and scale robustness
* Optimize similarity thresholds
* Compare LCS with Levenshtein distance
* Perform false-acceptance and false-rejection analysis

##  Author
**MARIYUM KHAN BAHADUR**

Design and Analysis of Algorithms  Project
