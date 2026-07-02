"""
=========================================================
AI_NEET

Text Extraction Engine
Version : 2.0

Author : Praveen Mark

Supports

✓ Embedded PDF Text
✓ OCR Fallback
✓ Cache Generation

=========================================================
"""

from pathlib import Path
import json

import fitz
import cv2
import numpy as np
import pytesseract

from PIL import Image


class TextExtractor:

    def __init__(self):

        self.minimum_text_length = 50

        self.zoom = 4

    # --------------------------------------------------

    def extract_document(self, pdf_path):

        document = fitz.open(pdf_path)

        pages = []

        for page_index in range(len(document)):

            page = document.load_page(page_index)

            text = self.extract_page_text(page)

            pages.append(

                {

                    "page_number": page_index + 1,

                    "text": text

                }

            )

            print(

                f"Page {page_index+1}/{len(document)}"

            )

        return {

            "file_name": Path(pdf_path).name,

            "page_count": len(document),

            "pages": pages

        }

    # --------------------------------------------------

    def extract_page_text(self, page):

        text = page.get_text("text")

        if len(text.strip()) >= self.minimum_text_length:

            return self.clean_text(text)

        print("    OCR Fallback...")

        return self.ocr_page(page)

    # --------------------------------------------------

    def render_page(self, page):

        matrix = fitz.Matrix(

            self.zoom,

            self.zoom

        )

        pix = page.get_pixmap(

            matrix=matrix

        )

        image = Image.frombytes(

            "RGB",

            [

                pix.width,

                pix.height

            ],

            pix.samples

        )

        return image

    # --------------------------------------------------

    def preprocess_image(self, image):

        image = np.array(image)

        image = cv2.cvtColor(

            image,

            cv2.COLOR_RGB2GRAY

        )

        image = cv2.threshold(

            image,

            0,

            255,

            cv2.THRESH_BINARY +

            cv2.THRESH_OTSU

        )[1]

        return image
    
        # --------------------------------------------------

    def ocr_page(self, page):

        image = self.render_page(page)

        image = self.preprocess_image(image)

        text = pytesseract.image_to_string(

            image,

            lang="eng",

            config="--oem 3 --psm 6"

        )

        return self.clean_text(text)

    # --------------------------------------------------

    def clean_text(self, text):

        if not text:

            return ""

        text = text.replace("\x0c", "")

        text = text.replace("\t", " ")

        text = text.replace("\r", " ")

        lines = []

        for line in text.split("\n"):

            line = " ".join(

                line.split()

            )

            if line:

                lines.append(line)

        return "\n".join(lines)

    # --------------------------------------------------

    def save_json(

        self,

        data,

        output_file

    ):

        output_file = Path(output_file)

        output_file.parent.mkdir(

            parents=True,

            exist_ok=True

        )

        with open(

            output_file,

            "w",

            encoding="utf-8"

        ) as file:

            json.dump(

                data,

                file,

                indent=4,

                ensure_ascii=False

            )

    # --------------------------------------------------

    def process_pdf(

        self,

        pdf_path,

        output_folder

    ):

        pdf_path = Path(pdf_path)

        output_folder = Path(output_folder)

        output_file = (

            output_folder /

            f"{pdf_path.stem}.json"

        )

        print()

        print("=" * 70)

        print(

            f"Processing : {pdf_path.name}"

        )

        print("=" * 70)

        document = self.extract_document(

            str(pdf_path)

        )

        self.save_json(

            document,

            output_file

        )

        print()

        print(

            f"Saved : {output_file}"

        )

        print()

        return document
    
        # --------------------------------------------------

    def process_folder(

        self,

        input_folder,

        output_folder

    ):

        input_folder = Path(input_folder)

        output_folder = Path(output_folder)

        pdf_files = sorted(

            input_folder.rglob("*.pdf")

        )

        processed = 0

        total_pages = 0

        print()

        print("=" * 70)
        print("TEXT EXTRACTION")
        print("=" * 70)

        for pdf in pdf_files:

            document = self.process_pdf(

                pdf,

                output_folder

            )

            processed += 1

            total_pages += document["page_count"]

        print()

        print("=" * 70)
        print("EXTRACTION SUMMARY")
        print("=" * 70)

        print(

            f"PDF Files : {processed}"

        )

        print(

            f"Pages     : {total_pages}"

        )

        print("=" * 70)

        return {

            "pdfs": processed,

            "pages": total_pages

        }

    # --------------------------------------------------

    def verify_json(

        self,

        json_file

    ):

        json_file = Path(json_file)

        with open(

            json_file,

            "r",

            encoding="utf-8"

        ) as file:

            data = json.load(file)

        page_count = len(

            data["pages"]

        )

        text_pages = 0

        empty_pages = 0

        total_words = 0

        for page in data["pages"]:

            text = page["text"]

            if text.strip():

                text_pages += 1

                total_words += len(

                    text.split()

                )

            else:

                empty_pages += 1

        print()

        print("=" * 70)
        print(json_file.name)
        print("=" * 70)

        print(

            f"Pages With Text : {text_pages}"

        )

        print(

            f"Empty Pages     : {empty_pages}"

        )

        print(

            f"Words           : {total_words}"

        )

        print("=" * 70)

        return {

            "pages": page_count,

            "text_pages": text_pages,

            "empty_pages": empty_pages,

            "words": total_words

        }
    
        # --------------------------------------------------

    def verify_folder(

        self,

        folder

    ):

        folder = Path(folder)

        json_files = sorted(

            folder.glob("*.json")

        )

        total_pages = 0
        total_text_pages = 0
        total_empty_pages = 0
        total_words = 0

        print()
        print("=" * 70)
        print("VERIFYING CACHE")
        print("=" * 70)

        for json_file in json_files:

            stats = self.verify_json(
                json_file
            )

            total_pages += stats["pages"]
            total_text_pages += stats["text_pages"]
            total_empty_pages += stats["empty_pages"]
            total_words += stats["words"]

        print()
        print("=" * 70)
        print("CACHE SUMMARY")
        print("=" * 70)

        print(f"JSON Files       : {len(json_files)}")
        print(f"Pages            : {total_pages}")
        print(f"Pages With Text  : {total_text_pages}")
        print(f"Empty Pages      : {total_empty_pages}")
        print(f"Total Words      : {total_words}")

        print("=" * 70)

    # --------------------------------------------------

    def process(

        self,

        input_folder,

        output_folder

    ):

        stats = self.process_folder(

            input_folder,

            output_folder

        )

        print()

        print("=" * 70)
        print("TEXT EXTRACTION COMPLETE")
        print("=" * 70)

        print(

            f"Processed PDFs : {stats['pdfs']}"

        )

        print(

            f"Processed Pages : {stats['pages']}"

        )

        print("=" * 70)

        return stats


# =========================================================
# End of File
# =========================================================