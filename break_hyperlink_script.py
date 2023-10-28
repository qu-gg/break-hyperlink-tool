import re
import fitz

# Change these to your PDF file paths
PDF_PATH = "BREAK_RPG_BETA_v0.9.1_BACKERKIT_TOC.pdf"
PDF_SAVE_FILE = "BREAK_RPG_BETA_v0.9.1_BACKERKIT_TOC_HYPERLINKED.pdf"


if __name__ == '__main__':
    # Open up the PDF file
    doc = fitz.open(PDF_PATH)

    # Regex pattern matcher for pXXX in text
    pattern = re.compile(r"p[0-9]+", re.IGNORECASE)

    # Iterate over all pages
    for page_idx, page in enumerate(doc):
        # Extract the page text
        text = page.get_text()

        # Iterate over each found match in string, adding the link
        r = pattern.search(text)
        while r:
            # Get all instances of said text match
            text_instance = page.search_for(r.string[r.start():r.end()])

            # For each instance, add a hyperlink box to it
            for inst in text_instance:
                link = page.insert_link({
                    "kind": fitz.LINK_GOTO,
                    "page": int(r.string[r.start():r.end()].replace("p", "")) - 1,
                    "from": inst,
                    "to": fitz.Point(0.0, 0.0)
                })

                # Optional blue color highlighting of the text, just uncomment # the next three lines
                # highlight = page.add_highlight_annot(inst)
                # highlight.set_colors(stroke=[0.5, 1, 1])
                # highlight.update()

            # Update the search for the next
            r = pattern.search(text, r.start() + 1)

    # Save the PDF. Make sure it isn't open somewhere else!
    doc.save(PDF_SAVE_FILE)
