from PIL import Image


# ============================================================
# CLASS 1: IMAGE TO MATRIX CONVERTER
# Converts signature image into a 64x64 binary matrix
# ============================================================

class ImageToMatrixConverter:

    def __init__(self, image_path, size=64, threshold=128):
        self.image_path = image_path
        self.size = size
        self.threshold = threshold

    def convert(self):

        # Open image
        image = Image.open(self.image_path)

        # Convert to grayscale
        image = image.convert("L")

        # Resize image to 64x64
        image = image.resize((self.size, self.size))

        # Create binary matrix
        matrix = []

        for y in range(self.size):

            row = []

            for x in range(self.size):

                pixel = image.getpixel((x, y))

                # Dark pixel = ink = 1
                # Light pixel = background = 0
                if pixel < self.threshold:
                    row.append("1")
                else:
                    row.append("0")

            matrix.append(row)

        return matrix


# ============================================================
# CLASS 2: MATRIX COMPRESSOR
# Converts 64x64 matrix into 16x16 matrix
# Each 4x4 block becomes one value
# ============================================================

class MatrixCompressor:

    def __init__(self, block_size=4, ink_ratio_threshold=0.10):
        self.block_size = block_size
        self.ink_ratio_threshold = ink_ratio_threshold

    def compress(self, matrix):

        original_size = len(matrix)

        compressed_matrix = []

        for row_start in range(0, original_size, self.block_size):

            compressed_row = []

            for col_start in range(0, original_size, self.block_size):

                ink_count = 0
                total_pixels = self.block_size * self.block_size

                # Count ink pixels inside the block
                for i in range(row_start, row_start + self.block_size):

                    for j in range(col_start, col_start + self.block_size):

                        if matrix[i][j] == "1":
                            ink_count += 1

                # Calculate ink ratio
                ink_ratio = ink_count / total_pixels

                # If at least 10% pixels contain ink,
                # mark compressed block as ink
                if ink_ratio >= self.ink_ratio_threshold:
                    compressed_row.append("1")
                else:
                    compressed_row.append("0")

            compressed_matrix.append(compressed_row)

        return compressed_matrix


# ============================================================
# CLASS 3: MATRIX TO ROW/COLUMN CONVERTER
# Calculates row density and column density
# ============================================================

class MatrixToRowColConverter:

    def convert(self, matrix):

        size = len(matrix)

        row_density = []
        column_density = []

        # Calculate row density
        for i in range(size):

            count = sum(1 for value in matrix[i] if value == "1")

            row_density.append(count)

        # Calculate column density
        for j in range(size):

            count = 0

            for i in range(size):

                if matrix[i][j] == "1":
                    count += 1

            column_density.append(count)

        return row_density, column_density


# ============================================================
# CLASS 4: ROW/COLUMN COMPRESSOR
# Converts density arrays into 16-character hexadecimal string
# ============================================================

class RowColCompressor:

    HEX_CHARACTERS = "0123456789ABCDEF"

    def compress(self, row_density, column_density):

        # Combine into 8 row buckets + 8 column buckets
        final_values = []

        # ----------------------------------------------------
        # ROW DENSITY -> 8 BUCKETS
        # Each bucket contains 2 values
        # ----------------------------------------------------

        for i in range(0, 16, 2):

            average = (
                row_density[i] +
                row_density[i + 1]
            ) / 2

            final_values.append(average)

        # ----------------------------------------------------
        # COLUMN DENSITY -> 8 BUCKETS
        # ----------------------------------------------------

        for i in range(0, 16, 2):

            average = (
                column_density[i] +
                column_density[i + 1]
            ) / 2

            final_values.append(average)

        # Find maximum value for normalization
        max_value = max(final_values)

        # Handle completely blank image
        if max_value == 0:
            return "0000000000000000"

        result = ""

        # Quantize each value to hexadecimal level 0-15
        for value in final_values:

            normalized = value / max_value

            quantized = round(normalized * 15)

            result += self.HEX_CHARACTERS[quantized]

        return result


# ============================================================
# CLASS 5: LCS COMPARATOR
# Implements Longest Common Subsequence using Dynamic Programming
# ============================================================

class LCSComparator:

    def find_lcs(self, string1, string2):

        m = len(string1)
        n = len(string2)

        # Create DP table
        dp = []

        for i in range(m + 1):
            dp.append([0] * (n + 1))

        # Fill DP table
        for i in range(1, m + 1):

            for j in range(1, n + 1):

                if string1[i - 1] == string2[j - 1]:

                    dp[i][j] = dp[i - 1][j - 1] + 1

                else:

                    dp[i][j] = max(
                        dp[i - 1][j],
                        dp[i][j - 1]
                    )

        # Reconstruct LCS string
        i = m
        j = n

        lcs = ""

        while i > 0 and j > 0:

            if string1[i - 1] == string2[j - 1]:

                lcs = string1[i - 1] + lcs

                i -= 1
                j -= 1

            elif dp[i - 1][j] > dp[i][j - 1]:

                i -= 1

            else:

                j -= 1

        return lcs, dp[m][n]

    def similarity_score(self, string1, string2):

        lcs, lcs_length = self.find_lcs(
            string1,
            string2
        )

        shorter_length = min(
            len(string1),
            len(string2)
        )

        if shorter_length == 0:
            return lcs, 0, 0

        similarity = (
            lcs_length / shorter_length
        ) * 100

        return lcs, lcs_length, similarity


# ============================================================
# MAIN PIPELINE
# ============================================================

def process_signature(image_path):

    print("\n======================================")
    print("Processing:", image_path)
    print("======================================")

    # Stage 1 + 2
    image_converter = ImageToMatrixConverter(image_path)

    binary_matrix = image_converter.convert()

    print("\nStage 2: 64x64 Binary Matrix Created")

    # Stage 3
    matrix_compressor = MatrixCompressor()

    compressed_matrix = matrix_compressor.compress(
        binary_matrix
    )

    print("\nStage 3: 16x16 Compressed Matrix:")

    for row in compressed_matrix:
        print("".join(row))

    # Stage 4
    row_col_converter = MatrixToRowColConverter()

    row_density, column_density = row_col_converter.convert(
        compressed_matrix
    )

    print("\nStage 4: Row Density:")
    print(row_density)

    print("\nStage 4: Column Density:")
    print(column_density)

    # Stage 5
    row_col_compressor = RowColCompressor()

    signature_string = row_col_compressor.compress(
        row_density,
        column_density
    )

    print("\nStage 5: Final 16 Character Signature String:")
    print(signature_string)

    return signature_string


# ============================================================
# PROGRAM START
# ============================================================

if __name__ == "__main__":

    print("\n======================================")
    print("LCS BASED SIGNATURE MATCHING SYSTEM - case1")
    print("======================================")

    # Change filenames according to your images
    signature1_path = "signature1.jpeg"
    signature2_path = "signature2.jpeg"

    try:

        # Process first signature
        signature_string1 = process_signature(
            signature1_path
        )

        # Process second signature
        signature_string2 = process_signature(
            signature2_path
        )

        # Stage 6: LCS Comparison
        comparator = LCSComparator()

        lcs, lcs_length, similarity = comparator.similarity_score(
            signature_string1,
            signature_string2
        )

        print("\n======================================")
        print("FINAL COMPARISON RESULT")
        print("======================================")

        print("\nSignature 1 String:")
        print(signature_string1)

        print("\nSignature 2 String:")
        print(signature_string2)

        print("\nLongest Common Subsequence:")
        print(lcs)

        print("\nLCS Length:")
        print(lcs_length)

        print("\nSimilarity Score:")
        print(f"{similarity:.2f}%")

        print("\n======================================")

        # Simple interpretation
        if similarity >= 75:
            print("RESULT: Signatures are highly similar")

        elif similarity >= 50:
            print("RESULT: Signatures are moderately similar")

        else:
            print("RESULT: Signatures are different")

        print("======================================\n")

    except FileNotFoundError:

        print("\nERROR:")
        print("One or both signature image files were not found.")
        print("Make sure signature1.png and signature2.png")
        print("are inside the same folder as main.py")

    except Exception as e:

        print("\nAn error occurred:")
        print(e)




if __name__ == "__main__":

    print("\n======================================")
    print("LCS BASED SIGNATURE MATCHING SYSTEM - case2")
    print("======================================")

    # Change filenames according to your images
    signature1_path = "signature1.jpeg"
    signature2_path = "signature1.jpeg"

    try:

        # Process first signature
        signature_string1 = process_signature(
            signature1_path
        )

        # Process second signature
        signature_string2 = process_signature(
            signature2_path
        )

        # Stage 6: LCS Comparison
        comparator = LCSComparator()

        lcs, lcs_length, similarity = comparator.similarity_score(
            signature_string1,
            signature_string2
        )

        print("\n======================================")
        print("FINAL COMPARISON RESULT")
        print("======================================")

        print("\nSignature 1 String:")
        print(signature_string1)

        print("\nSignature 2 String:")
        print(signature_string2)

        print("\nLongest Common Subsequence:")
        print(lcs)

        print("\nLCS Length:")
        print(lcs_length)

        print("\nSimilarity Score:")
        print(f"{similarity:.2f}%")

        print("\n======================================")

        # Simple interpretation
        if similarity >= 75:
            print("RESULT: Signatures are highly similar")

        elif similarity >= 50:
            print("RESULT: Signatures are moderately similar")

        else:
            print("RESULT: Signatures are different")

        print("======================================\n")

    except FileNotFoundError:

        print("\nERROR:")
        print("One or both signature image files were not found.")
        print("Make sure signature1.png and signature2.png")
        print("are inside the same folder as main.py")

    except Exception as e:

        print("\nAn error occurred:")
        print(e)
