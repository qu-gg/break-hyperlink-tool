import re
import fitz

from tqdm import tqdm


class RectList:
    def __init__(self):
        self.rect_list = []

    def rect_already_exists(self, rect):
        exists = False
        for ref_rect in self.rect_list:
            if rect.intersects(ref_rect):
                exists = True

        self.rect_list.append(rect)
        return exists


def apply_index():
    pages = (1, 3)
    regex = re.compile(r"\b[0-9]+\b", re.IGNORECASE)

    for page_idx, page in tqdm(enumerate(doc)):
        if page_idx < pages[0]:
            continue

        if page_idx > pages[1]:
            break

        # Extract the page text
        text = page.get_text()
        rect_list = RectList()

        fall = [int(i) for i in regex.findall(text)]
        fall = [i for i in reversed(sorted(set(fall)))]

        for pn in fall:
            text_instance = page.search_for(str(pn))

            # For each instance, add a hyperlink box to it
            for inst in text_instance:
                if rect_list.rect_already_exists(inst):
                    continue

                link = page.insert_link({
                    "kind": fitz.LINK_GOTO,
                    "page": pn - 1,
                    "from": inst,
                    "to": fitz.Point(0.0, 0.0)
                })

                # Optional blue color highlighting of the text, just uncomment # the next three lines
                if BLUE_HIGHLIGHT is True:
                    highlight = page.add_highlight_annot(inst)
                    highlight.set_colors(stroke=[0.5, 1, 1])
                    highlight.update()


def apply_appendix():
    pages = (459, 471)
    regex = re.compile(r"p[0-9]+", re.IGNORECASE)
    for page_idx, page in tqdm(enumerate(doc)):
        if page_idx < pages[0]:
            continue

        if page_idx > pages[1]:
            break

        # Extract the page text
        text = page.get_text()
        rect_list = RectList()

        fall = regex.findall(text)
        fall = [i for i in reversed(sorted(set(fall), key=lambda x: int(x.replace('p', ''))))]

        for pn in fall:
            text_instance = page.search_for(str(pn))

            # For each instance, add a hyperlink box to it
            for inst in text_instance:
                if rect_list.rect_already_exists(inst):
                    continue

                link = page.insert_link({
                    "kind": fitz.LINK_GOTO,
                    "page": int(pn.replace('p', '')) - 1,
                    "from": inst,
                    "to": fitz.Point(0.0, 0.0)
                })

                # Optional blue color highlighting of the text, just uncomment # the next three lines
                if BLUE_HIGHLIGHT is True:
                    highlight = page.add_highlight_annot(inst)
                    highlight.set_colors(stroke=[0.5, 1, 1])
                    highlight.update()


def apply_pattern(regex, pages):
    for page_idx, page in tqdm(enumerate(doc)):
        if page_idx < pages[0]:
            continue

        if page_idx > pages[1]:
            break

        # Extract the page text
        text = page.get_text().replace("\n", " ")

        # Iterate over each found match in string, adding the link
        r = regex.search(text)
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
                if BLUE_HIGHLIGHT is True:
                    highlight = page.add_highlight_annot(inst)
                    highlight.set_colors(stroke=[0.5, 1, 1])
                    highlight.update()

            # Update the search for the next
            r = regex.search(text, r.start() + 1)


def apply_margin(regex, pages, ref_page):
    for page_idx, page in tqdm(enumerate(doc)):
        if page_idx < pages[0]:
            continue

        if page_idx > pages[1]:
            break

        # Extract the page text
        text = page.get_text().replace("\n", " ")

        # Iterate over each found match in string, adding the link
        r = regex.search(text)
        while r:
            # Get all instances of said text match
            text_instance = page.search_for(r.string[r.start():r.end()])

            # For each instance, add a hyperlink box to it
            for inst in text_instance:
                link = page.insert_link({
                    "kind": fitz.LINK_GOTO,
                    "page": ref_page,
                    "from": inst,
                    "to": fitz.Point(0.0, 0.0)
                })

                # Optional blue color highlighting of the text, just uncomment # the next three lines
                if BLUE_HIGHLIGHT is True:
                    highlight = page.add_highlight_annot(inst)
                    highlight.set_colors(stroke=[0.5, 1, 1])
                    highlight.update()

            # Update the search for the next
            r = regex.search(text, r.start() + 1)


def get_triangle_bounds(regex, tripage, pages):
    for page_idx, page in tqdm(enumerate(doc)):
        if page_idx < tripage:
            continue

        if page_idx > tripage:
            break

        # Extract the page text
        text = page.get_text().replace("\n", " ")

        # Iterate over each found match in string, adding the link
        r = regex.search(text)

        # Get all instances of said text match
        text_instance = page.search_for(r.string[r.start():r.end()])
        TRIANGLE_BOUNDS = text_instance[0]

    for page_idx, page in tqdm(enumerate(doc)):
        if page_idx < pages[0]:
            continue

        if page_idx > pages[1]:
            break

        # Extract the page text
        text = page.get_text().replace("\n", " ")

        # Iterate over each found match in string, adding the link
        r = regex.search(text)
        if r is None:
            continue

        # Get all instances of said text match
        text_instance = page.search_for(r.string[r.start():r.end()], clip=TRIANGLE_BOUNDS)

        # For each instance, add a hyperlink box to it
        for inst in text_instance:
            link = page.insert_link({
                "kind": fitz.LINK_GOTO,
                "page": tripage,
                "from": inst,
                "to": fitz.Point(0.0, 0.0)
            })

            # Optional blue color highlighting of the text, just uncomment # the next three lines
            if BLUE_HIGHLIGHT is True:
                highlight = page.add_highlight_annot(inst)
                highlight.set_colors(stroke=[0.5, 1, 1])
                highlight.update()


def isExactMatch(page, term, clip, fullMatch=False, caseSensitive=False):
    # clip is an item from page.search_for(term, quads=True)
    termLen = len(term)
    termBboxLen = max(clip.height, clip.width)
    termfontSize = termBboxLen / termLen
    f = termfontSize * 2

    validate = page.get_text("blocks", clip=clip + (-f, -f, f, f), flags=0)[0][4]
    flag = 0
    if not caseSensitive:
        flag = re.IGNORECASE

    matches = len(re.findall(f'{term}', validate, flags=flag)) > 0
    if fullMatch:
        matches = len(re.findall(f'\\b{term}\\b', validate)) > 0
    return matches


if __name__ == '__main__':
    # Change these to your PDF file paths
    PDF_PATH = "BREAK_BOOK_PDF_newfont2.pdf"
    PDF_SAVE_FILE = "BREAK_BOOK_PDF_newfont2_HYPERLINKED"

    BLUE_HIGHLIGHT = False
    if BLUE_HIGHLIGHT is True:
        PDF_SAVE_FILE += "_BLUEHIGHLIGHT"

    PDF_SAVE_FILE += ".pdf"

    # Open up the PDF file
    doc = fitz.open(PDF_PATH)

    """ Index/Appendix """
    apply_index()
    apply_appendix()

    """ Regex pattern matcher for pXXX in text """
    pattern = re.compile(r"p[0-9]+", re.IGNORECASE)
    apply_pattern(pattern, (6, 459))

    """ Triangles """
    global TRIANGLE_BOUNDS
    pattern = re.compile(r"I")
    get_triangle_bounds(pattern, 8, (6, 208))

    pattern = re.compile(r"II")
    get_triangle_bounds(pattern, 208, (208, 295))

    pattern = re.compile(r"III")
    get_triangle_bounds(pattern, 296, (296, 314))

    pattern = re.compile(r"IV")
    get_triangle_bounds(pattern, 314, (314, 354))

    pattern = re.compile(r"V")
    get_triangle_bounds(pattern, 354, (354, 440))

    pattern = re.compile(r"VI")
    get_triangle_bounds(pattern, 440, (440, 472))

    """ Headers """
    for header_name, page_ref, page_skip in zip(
            [r"CHARACTER CREATION", r"PLAYING THE GAME", r"OUTER WORLD", r"GM’S GUIDE", r"ADVERSARIES", r"APPENDIx"],
            [8, 208, 296, 314, 354, 440],
            [10, None, None, None, 355, None]
    ):
        pattern = re.compile(header_name)
        for page_idx, page in tqdm(enumerate(doc)):
            if page_idx < 4:
                continue

            if page_skip is not None:
                if page_idx == page_skip:
                    continue

            # Extract the page text
            text = page.get_text()

            # Iterate over each found match in string, adding the link
            r = pattern.search(text)
            while r:
                # Get all instances of said text match
                text_instance = page.search_for(r.string[r.start():r.end()])

                # For each instance, add a hyperlink box to it
                for inst in text_instance:
                    if not isExactMatch(page, header_name, inst, fullMatch=True, caseSensitive=True):
                        continue

                    link = page.insert_link({
                        "kind": fitz.LINK_GOTO,
                        "page": page_ref,
                        "from": inst,
                        "to": fitz.Point(0.0, 0.0)
                    })

                    # Optional blue color highlighting of the text, just uncomment # the next three lines
                    if BLUE_HIGHLIGHT is True:
                        highlight = page.add_highlight_annot(inst)
                        highlight.set_colors(stroke=[0.5, 1, 1])
                        highlight.update()

                # Update the search for the next
                r = pattern.search(text, r.start() + 1)

    # Save the PDF. Make sure it isn't open somewhere else!
    doc.save(PDF_SAVE_FILE)
