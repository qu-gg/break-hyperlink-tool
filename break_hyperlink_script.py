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


def apply_index(pages_to_change):
    regex = re.compile(r"\b[0-9]+\b", re.IGNORECASE)

    for page_idx, page in tqdm(enumerate(doc)):
        if page_idx < pages_to_change[0]:
            continue

        if page_idx > pages_to_change[1]:
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
    regex1 = re.compile(r"p[0-9]+", re.IGNORECASE)
    regex2 = re.compile(r"\s[0-9]+", re.IGNORECASE)
    for regex in [regex1, regex2]:
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
    PDF_PATH = "BREAK_BOOK_PDF_RGB.pdf"
    PDF_SAVE_FILE = "BREAK_BOOK_PDF_RGB_HYPERLINKED"

    BLUE_HIGHLIGHT = False
    if BLUE_HIGHLIGHT is True:
        PDF_SAVE_FILE += "_BLUEHIGHLIGHT"

    PDF_SAVE_FILE += ".pdf"

    # Open up the PDF file
    doc = fitz.open(PDF_PATH)

    """ Index/Appendix """
    apply_index((1, 3))
    apply_appendix()
    apply_index((459, 470))

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
    HEADER_BOUNDS = fitz.Rect(0, 0, 500, 25)
    for header_name, page_ref, page_skip in zip(
            [r"CHARACTER CREATION", r"PLAYING THE GAME", r"OUTER WORLD", r"GM’S GUIDE", r"ADVERSARIES", r"APPENDIX"],
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
                text_instance = page.search_for(r.string[r.start():r.end()], clip=HEADER_BOUNDS)

                # For each instance, add a hyperlink box to it
                for inst in text_instance:
                    # if not isExactMatch(page, header_name, inst, fullMatch=True, caseSensitive=True):
                    #     continue

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

    """ Side Margin """
    section_one = [
        ["CREATING A \nCHARACTER", 9],
        ["CALLING", 11],
        ["SPECIES", 79],
        ["HOMELAND \n& HISTORY", 107],
        ["TRAITS", 129],
        ["QUIRK", 131],
        ["FINISHING \nDETAILS", 147],
        ["GEAR", 149],
        ["CHARACTER \nRANK", 203],
    ]

    section_two = [
        ["GAME \nBASICS", 209],
        ["CHECKS \n& CONTESTS", 215],
        ["JOURNEY", 221],
        ["EXPLORE", 229],
        ["NEGOTIATE", 237],
        ["FIGHT", 243],
        ["PERILS", 265],
        ["DOWNTIME", 271],
        ["CRAFT", 279]
    ]

    section_three = [
        ["The Octia \nScroll", 299],
        ["Von Peeble’s \nMap", 301],
        ["Wistful \nDark", 303],
        ["Twilight \nMeridian", 305],
        ["Blazing \nGarden", 307],
        ["Buried \nKingdom", 309],
        ["Further \nExploration", 311]
    ]

    section_four = [
        ["BEING A GM", 315],
        ["Running the \nGame", 315],
        ["Creating an \nAdventure", 317],
        ["Creating a \nGMC", 319],
        ["Creating a \nSettlement", 327],
        ["Creating an \nAdventure \nSite", 331],
        ["Creating an \nAdventure \nMap", 343],
        ["Creating \nEncounters", 347],
        ["Creating a \nSaga", 351]
    ]

    section_five = [
        ["Using \nAdversaries",         355],
        ["Asura, Lajja",                359],
        ["Bizzer \nSwarm",              363],
        ["Blaster Mage",                365],
        ["Chompa",                      367],
        ["Chosen one",                  369],
        ["Demon, \nBlighted",           371],
        ["Drones",                      375],
        ["Goop",                        381],
        ["Giga \nGruun",                383],
        ["Grim Wing",                   385],
        ["Killservants",                387],
        ["Lalka",                       391],
        ["Master \nVillains",           393],
        ["Mundymutts",                  399],
        ["Skelemen",                    403],
        ["Shadow \nBeast",              411],
        ["Tiny \nUnhelpful \nCloud",    415],
        ["Undead \nPeddler",            417],
        ["Unshaped, \nBellzuub",        419],
        ["Urarani",                     425],
        ["Creating \nAdversaries",      429]
    ]

    page_bounds = [
        (9, 209),
        (209, 297),
        (297, 314),
        (314, 355),
        (355, 439)
    ]

    MARGIN_BOUNDS = fitz.Rect(350, 16, 450, 390)
    for section, page_bound in zip([section_one, section_two, section_three, section_four, section_five], page_bounds):
        for (margin_name, ref_page) in section:
            for page_idx, page in tqdm(enumerate(doc)):
                # Stop before Section VI
                if not (page_bound[0] <= page_idx < page_bound[1]):
                    continue

                # Extract the page text
                text = page.get_text()

                # Get all instances of said text match
                text_instance = page.search_for(margin_name, clip=MARGIN_BOUNDS)

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

    """ Lower Margin """
    section_one = [
        ["Quick Start",             12],
        ["Factotum",                15],
        ["Sneak",                   21],
        ["Champion",                27],
        ["Raider",                  33],
        ["Battle \nPrincess",         39],
        ["Murder \nPrincess",         49],
        ["Sage",                    57],
        ["Heretic",                 67],
    ]

    section_two = [
        ["Quick Start", 80],
        ["Human \n(Native)",    83],
        ["Human \n(Dimensional \nStray)",    85],
        ["Chib",    87],
        ["Tenebrate",    89],
        ["Rai-Neko",    91],
        ["Promethean",    93],
        ["Gruun",    95],
        ["Goblin",    97],
        ["Dwarf",    99],
        ["Elf",    101],
        ["Bio", 103],
        ["Mechanoid",    103],
        ["Species \nAbilities",    105],
    ]

    section_three = [
        ["Wistful Dark", 109],
        ["Twilight \nMeridian",    113],
        ["Blazing \nGarden",    117],
        ["Buried \nKingdom",    121],
        ["Other World",    125]
    ]

    section_four = [
        ["Spirit Quirks", 131],
        ["Physiology \nQuirks",    135],
        ["Fate Quirks", 138],
        ["Eldritch \nQuirks",    141],
        ["Robotic \nQuirks",    144]
    ]

    section_five = [
        ["Paying", 150],
        ["Carrying", 150],
        ["Weapon \nTypes",    151],
        ["Armor Types",    162],
        ["Shield Types",    168],
        ["Outfits",    171],
        ["Wearable \nAccessories",    172],
        ["Wayfinding",    173],
        ["Illumination",    174],
        ["Specialist’s \nKits",    175],
        ["Books",    175],
        ["Consumables",  176],
        ["Combustibles \n& Chemicals",    177],
        ["Miscellaneous", 178],
        ["Curiosities, \nArtifacts & \nGadgets", 179],
        ["Other World \nItems",    181],
        ["Companions",    182],
        ["Vehicles",    195],
        ["Property",    199],
        ["Services",    200],
    ]

    section_six = [
        ["Advancing \nin Rank",    204],
        ["Allegiance",    205]
    ]

    section_seven = [
        ["Playing \nthe Game",    210],
        ["General \nPlay",    211],
        ["Managing \nTime",    212],
        ["Rolling Dice",    213],
        ["Focused \nRules",    214]
    ]

    section_eight = [
        ["Aptitudes",     216],
        ["Check \nProcedure",  217],
        ["Contest \nProcedure",  218],
        ["Linked \nContests", 219],
        ["Special \nSuccess", 220]
    ]

    section_nine = [
        ["Journey \nProcedure",    222],
        ["Adventure \nMaps",    223],
        ["Navigating",    225],
        ["Getting Lost",    226],
        ["Map \nEncounters",    227],
        ["A Day’s \nTravel",    228],
    ]

    section_ten = [
        ["Explore \nProcedure",    230],
        ["Adventure \nSites",    231],
        ["PC Positions",    232],
        ["Movement \nTypes",    233],
        ["Location \nActions",    234],
        ["Site \nEncounters",    235],
    ]

    section_eleven = [
        ["Negotiate \nProcedure",    238],
        ["Standard \nNegotiation",    239],
        ["Complex \nNegotiation",    241]
    ]

    section_twelve = [
        ["Fight \nProcedure",    244],
        ["Combat \nValues",    245],
        ["Battlefields",    247],
        ["Area \nConditions", 249],
        ["Conducting \na Fight", 251],
        ["Actions",    253],
        ["Damage",    258],
        ["Injury Table",    259],
        ["Treatment",    261],
        ["Sundering", 262],
        ["Colossal \nCombat",    263]
    ]

    section_thirteen = [
        ["Non-Combat \nInjuries",    266],
        ["Ailments",    267]
    ]

    section_fourteen = [
        ["Downtime \nActivities",    12],
        ["Social Bonds",    15],
        ["Reputations",    21]
    ]

    section_fifteen = [
        ["Craft \nProcedure",    280],
        ["Crafting \nDisciplines",    281],
        ["Repairs",    284],
        ["Imbuing",    285],
        ["Materials",    287],
        ["Additives",    290],
        ["Mishaps",    293]
    ]

    page_bounds = [
        (10, 80),
        (80, 108),
        (108, 129),
        (129, 148),
        (150, 204),
        (204, 208),
        (209, 215),
        (216, 221),
        (222, 229),
        (230, 238),
        (238, 244),
        (244, 266),
        (266, 272),
        (272, 280),
        (280, 296)
    ]

    template = [
        ["",    12],
        ["",    15],
        ["",    21],
        ["",    27],
        ["",    33],
        ["",    39],
        ["",    49],
        ["",    57],
        ["",    67],
    ]

    MARGIN_BOUNDS = fitz.Rect(325, 150, 450, 1000)
    for section, page_bound in zip(
            [section_one, section_two, section_three, section_four, section_five, section_six, section_seven, section_eight,
             section_nine, section_ten, section_eleven, section_twelve, section_thirteen, section_fourteen, section_fifteen],
            page_bounds
    ):
        for (margin_name, ref_page) in section:
            for page_idx, page in tqdm(enumerate(doc)):
                # Stop before Section VI
                if not (page_bound[0] <= page_idx < page_bound[1]):
                    continue

                # Extract the page text
                text = page.get_text()

                # Get all instances of said text match
                text_instance = page.search_for(margin_name, clip=MARGIN_BOUNDS)

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


    """ Custom Index logic """
    section_six = [
        ["CHARACTER \nSHEET", 443],
        ["GEAR LIST", 445],
        ["GAME \nBASICS", 449],
        ["CHECKS \n& CONTESTS", 449],
        ["JOURNEY", 450],
        ["EXPLORE", 451],
        ["NEGOTIATE", 452],
        ["FIGHT", 453],
        ["PERILS", 455],
        ["DOWNTIME", 457],
        ["CRAFT", 458],
        ["INDEX", 459]
    ]

    MARGIN_BOUNDS = fitz.Rect(325, 16, 450, 1000)
    for (margin_name, ref_page) in section_six:
        for page_idx, page in tqdm(enumerate(doc)):
            # Stop before Section VI
            if page_idx < 444:
                continue

            # Extract the page text
            text = page.get_text()

            # Get all instances of said text match
            text_instance = page.search_for(margin_name, clip=MARGIN_BOUNDS)

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

    """ Table-of-Content """
    page1 = doc[1]
    page2 = doc[2]
    page3 = doc[3]
    pages = [doc[1], doc[2], doc[3]]
    TOC_LIST = []

    Headers = ['CHARACTER CREATION', 'PLAYING THE GAME', 'OUTER WORLD', 'GAME MASTER’S GUIDE',
               'APPENDIX']  # 'ADVERSARIES',

    for page in pages:
        text = page.get_text()
        text = text.split("\n")

        new_list = []
        for item in text:
            item = item.rstrip()
            item = item.lstrip()
            item = item.strip('\n')

            # Some lines have messed up parsing in which the title and page number are in it
            # These lines can be caught when them being split by whitespace has over 15 entries
            # Gross and manual but it works(tm)
            if len(item.split(' ')) > 13:
                item_split = item.split(' ')

                # Manual check if it is Step 6, as it has an errant whitespace
                if item_split[0] == 'STEP' and item_split[1] == '6':
                    item_split.pop(3)

                # Loop through to get all the real text
                item_string = ""
                for i in item_split:
                    if i != '':
                        item_string += f"{i} "
                    else:
                        break

                # Append the text and page number to the list
                new_list.append(item_string)
                new_list.append(item_split[-1])
                continue

            if item != '':
                new_list.append(item)

        for x, item in enumerate(new_list):
            if item.isdigit():
                title = new_list[x - 1]
                if title in Headers:
                    lvl = 1
                elif title.isupper():
                    lvl = 1
                else:
                    lvl = 2
                page = int(item)
                TOC_ITEM = [lvl, title, page]

                # Manually breaking apart Adversaries and Character Sheet
                if title == 'Character Sheet':
                    TOC_LIST.append([1, 'CHARACTER SHEET', 442])
                    print(TOC_LIST[-1])

                # Manually denoting Cheat Sheets
                if title == 'Gear List':
                    TOC_LIST.append([1, 'CHEAT SHEETS', 446])
                    print(TOC_LIST[-1])

                # Fixing some small errors here manually
                if title == 'CONTENTS' or title == '294' or title == '460':
                    continue

                # Add content to Table-of-Contents
                TOC_LIST.append(TOC_ITEM)
                print(TOC_ITEM)

                # Manually add a header for Step 3 - Homeland
                if 'STEP 3' in title:
                    TOC_LIST.append([2, 'Homeland Table', 109])
                    print(TOC_LIST[-1])

    print("146: ", TOC_LIST[146])
    doc.set_toc(TOC_LIST)

    # Save the PDF. Make sure it isn't open somewhere else!
    doc.save(PDF_SAVE_FILE)
