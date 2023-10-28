import re
import sys
import fitz

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QApplication, QMainWindow, QLabel, QGroupBox, QGridLayout,
                             QLineEdit, QFileDialog, QPushButton, QCheckBox)


class Window(QMainWindow):
    def __init__(self, basedir):
        super(Window, self).__init__()

        # Load classes
        self.basedir = basedir

        # Window Title
        self.setWindowTitle("BREAK!! Hyperlinking Tool")

        # Base Groupbox to hold the lines
        base_stats_group = QGroupBox("")
        base_stats_layout = QGridLayout()
        base_stats_layout.setAlignment(Qt.AlignTop)

        # Filepath display for custom art
        self.art_filepath = QLineEdit("")

        # Buttons and file dialog associated with selecting local files
        art_gridlayout = QGridLayout()
        self.art_filedialog = QFileDialog()
        self.art_select = QPushButton("Open")
        self.art_select.clicked.connect(self.open_file)
        art_gridlayout.addWidget(self.art_filepath, 0, 1)
        art_gridlayout.addWidget(self.art_select, 0, 2)

        base_stats_layout.addWidget(QLabel("Base PDF Path:"), 0, 0)
        base_stats_layout.addLayout(art_gridlayout, 0, 1)

        # Display the output path and name of the hyperlinked PDF
        self.output_path = QLineEdit("")
        base_stats_layout.addWidget(QLabel("Output PDF Path:"), 1, 0)
        base_stats_layout.addWidget(self.output_path, 1, 1)

        # Whether to use a blue highlighting box
        form_fill_label = QLabel("Blue Highlight Box:")
        base_stats_layout.addWidget(form_fill_label, 2, 0)
        self.highlight_check = QCheckBox()
        base_stats_layout.addWidget(self.highlight_check, 2, 1)
        base_stats_layout.addWidget(QLabel(""), 3, 0, 1, -1)

        # Make the execute button
        self.button = QPushButton("Execute")
        self.button.clicked.connect(lambda: self.hyperlink_file())
        base_stats_layout.addWidget(self.button, 4, 0, 1, -1)

        # Grid layout
        base_stats_group.setFixedWidth(600)
        base_stats_group.setFixedHeight(150)
        base_stats_group.setLayout(base_stats_layout)
        self.setCentralWidget(base_stats_group)

    def open_file(self):
        """ Handles opening a file for the art path images; if an invalid image then show a message to the statusbar """
        self.pdf_path = self.art_filedialog.getOpenFileName(self, 'Load File', self.basedir + '/')[0]

        # Error handling for image paths
        if '.pdf' not in self.pdf_path:
            self.statusbar.showMessage("Filename invalid, select again!", 3000)
        else:
            self.art_filepath.setText(self.pdf_path)

        # Build the saving path
        self.pdf_save_path = f"{self.pdf_path.strip('.pdf')}_HYPERLINKED.pdf"
        self.output_path.setText(self.pdf_save_path)

    def hyperlink_file(self):
        """ Handles hyperlinking the PDF file """
        # Open up the PDF file
        doc = fitz.open(self.pdf_path)

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
                    page.insert_link({
                        "kind": fitz.LINK_GOTO,
                        "page": int(r.string[r.start():r.end()].replace("p", "")) - 1,
                        "from": inst,
                        "to": fitz.Point(0.0, 0.0)
                    })

                    # Optional blue color highlighting of the text
                    if self.highlight_check.isChecked():
                        highlight = page.add_highlight_annot(inst)
                        highlight.set_colors(stroke=[0.5, 1, 1])
                        highlight.update()

                # Update the search for the next
                r = pattern.search(text, r.start() + 1)

        # Save the PDF. Make sure it isn't open somewhere else!
        try:
            doc.save(self.pdf_save_path)
            self.button.setText("Success!")

        # If it fails from the PDF being open
        except Exception as e:
            self.button.setText("Error in saving. Make sure the PDF is closed!")

        # Update with the result
        self.update()


if __name__ == '__main__':
    # Specify whether this is local development or application compilation
    basedir = ""
    application = True

    # If application compilation, get the folder from which the executable is being executed
    if application:
        # First split depending on OS to get the current application name (in case users have modified it)
        if '/' in sys.executable:
            current_app_name = sys.executable.split('/')[-1]
        elif '\\' in sys.executable:
            current_app_name = sys.executable.split('\\')[-1]
        else:
            raise NotADirectoryError("Pathing not found for {}. Please move to another path!".format(sys.executable))

        # Then replace the application name with nothing to get the path
        basedir = sys.executable.replace(current_app_name, '')

    # Define the application
    app = QApplication(sys.argv)
    window = Window(basedir)

    # Different checking needed depending on local build or executable run
    window.show()
    sys.exit(app.exec_())
