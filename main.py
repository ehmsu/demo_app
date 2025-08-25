import sys
import os
import pandas as pd
from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, QLineEdit,
    QPushButton, QTextEdit, QLabel, QStackedWidget, QSizePolicy
)
from PySide6.QtCore import QSize, QTimer
from PySide6.QtGui import QIcon, QPixmap

button_stylesheet = ("""
    QPushButton {
        background-color: #173a57; 
        color: white;
        font-weight: bold;
        border-radius: 10px;
        padding: 10px;
    }
    QPushButton:hover {
        background-color: #45a049;
    }
""")

# def info_button_stylesheet(image_url): 
#     return (f"QPushButton {{border: none; background-repeat: no-repeat;background-image: url(images/{image_url}.png);background-position: center; background-size: cover;}}")

class SquareButton(QPushButton):
    def resizeEvent(self, event):
        side = max(event.size().width(), event.size().height())
        self.setFixedSize(QSize(side, side))
        self.setIconSize(QSize(side, side))
        super().resizeEvent(event)

class AddressLookupApp(QWidget):
    def __init__(self, stacked_widget):
        super().__init__()
        self.stacked_widget = stacked_widget
        self.setWindowTitle("Address Lookup")

        # UI Layout
        layout = QGridLayout()

        """
        SEARCH BAR 
        """
        
        # search_bar_layout = QHBoxLayout()
        self.label = QLabel("Enter address:")
        layout.addWidget(self.label, 0, 0, 1, 1)

        self.address_input = QLineEdit()
        layout.addWidget(self.address_input, 0, 1, 1, 2)

        self.search_button = QPushButton("Search")
        self.search_button.clicked.connect(self.search_address)
        layout.addWidget(self.search_button, 0, 3, 1, 1)

        """
        BUTTONS FOR WARD/NEIGHBOURHOOD 
        """

        self.ward_button = SquareButton("WARD")
        self.ward_button.setStyleSheet(button_stylesheet)
        self.ward_button.clicked.connect(self.go_to_ward_page)
        # self.ward_button.setFixedSize(100, 100)
        layout.addWidget(self.ward_button, 1, 0, 2, 2)

        self.neighbourhood_button = SquareButton("NEIGHBOURHOOD")
        self.neighbourhood_button.setStyleSheet(button_stylesheet)
        self.neighbourhood_button.clicked.connect(self.go_to_neighbourhood_page)
        # self.neighbourhood_button.setFixedSize(100, 100)
        layout.addWidget(self.neighbourhood_button, 1, 2, 2, 2)

        self.setLayout(layout)
    
    def go_to_ward_page(self):
        self.stacked_widget.setCurrentIndex(1)

    def go_to_neighbourhood_page(self):
        self.stacked_widget.setCurrentIndex(2) # neighbourhood page 

    def search_address(self):
        address_query = self.address_input.text().strip().lower()
        if not address_query:
            self.result_area.setText("Please enter an address.")
            return

        data_dir = "data"
        if not os.path.exists(data_dir):
            self.result_area.setText("Data folder not found.")
            return

        matched_rows = []

        for file in os.listdir(data_dir):
            if file.endswith(".csv"):
                filepath = os.path.join(data_dir, file)
                try:
                    df = pd.read_csv(filepath)
                    # Normalize column names
                    df.columns = df.columns.str.lower()

                    if 'address' in df.columns:
                        # Normalize addresses
                        df['address'] = df['address'].astype(str).str.lower()
                        matches = df[df['address'].str.contains(address_query, na=False)]
                        if not matches.empty:
                            matched_rows.append(f"Matches in {file}:\n{matches.to_string(index=False)}\n")
                except Exception as e:
                    matched_rows.append(f"Error reading {file}: {e}")

        if matched_rows:
            self.result_area.setText("\n".join(matched_rows))
        else:
            self.result_area.setText("No matches found.")


class WardPage(QWidget):
    def __init__(self, stacked_widget):
        super().__init__()
        layout = QGridLayout()
        self.stacked_widget = stacked_widget
        # layout.addWidget(QLabel("This is the WARD page."))

        self.wards_in_need_btn = SquareButton() 
        image_path = r"images\ward\TopTenWard.png"
        self.wards_in_need_btn.setIcon(QIcon(QPixmap(image_path)))
        self.wards_in_need_btn.clicked.connect(lambda: stacked_widget.setCurrentIndex(3)) 
        layout.addWidget(self.wards_in_need_btn, 0, 0, 1, 1)

        self.aff_rgi_control_btn = SquareButton() 
        image_path = r"images\ward\Approved_Houses.png"
        self.aff_rgi_control_btn.setIcon(QIcon(QPixmap(image_path)))
        self.aff_rgi_control_btn.clicked.connect(lambda: stacked_widget.setCurrentIndex(4))
        layout.addWidget(self.aff_rgi_control_btn, 0, 1, 1, 1)

        self.ehon_btn = SquareButton()
        image_path = r"images\ward\EHON.png"
        self.ehon_btn.setIcon(QIcon(QPixmap(image_path))) 
        self.ehon_btn.clicked.connect(lambda: stacked_widget.setCurrentIndex(5))
        layout.addWidget(self.ehon_btn, 0, 2, 1, 1)

        self.income_btn = SquareButton() 
        image_path = r"images\ward\LowIncomePerWard.png"
        self.income_btn.setIcon(QIcon(QPixmap(image_path)))
        self.income_btn.clicked.connect(lambda: stacked_widget.setCurrentIndex(6))
        layout.addWidget(self.income_btn, 1, 0, 1, 1)

        self.renter_btn = SquareButton() 
        image_path = r"images\ward\number_of_renters.png"
        self.renter_btn.setIcon(QIcon(QPixmap(image_path)))
        self.renter_btn.clicked.connect(lambda: stacked_widget.setCurrentIndex(7))
        layout.addWidget(self.renter_btn, 1, 1, 1, 1)

        self.fun_statistics = QTextEdit() 
        self.fun_statistics.setPlainText("To improve housing equity, planning should prioritize areas with both high demand and capacity for growth,"
                                 " ensuring affordable housing projects align with community needs. \nFocusing on wards like"
                                " Toronto Centre (Ward 13) and Humber River–Black Creek (Ward 7) could help reduce"
                                " disparities and support vulnerable residents effectively."
                                    )
        self.fun_statistics.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        layout.addWidget(self.fun_statistics, 1, 2, 1, 1)
        
        back_button = QPushButton("Back")
        back_button.clicked.connect(lambda: stacked_widget.setCurrentIndex(0))
        layout.addWidget(back_button, 2, 0, 1, 3)

        self.setLayout(layout)

    def go_to_button_page(self, index):
        self.stacked_widget.setCurrentIndex(index)

class NeighbourhoodPage(QWidget):
    def __init__(self, stacked_widget):
        super().__init__()
        layout = QGridLayout()
        # layout.addWidget(QLabel("This is the NEIGHBOURHOOD page."))

        self.top_ten_neighbourhoods_btn = SquareButton() 
        image_path = r"images\neighbourhoods\top_ten_neighbourhoods.png"
        self.top_ten_neighbourhoods_btn.setIcon(QIcon(QPixmap(image_path)))
        self.top_ten_neighbourhoods_btn.clicked.connect(lambda: stacked_widget.setCurrentIndex(8))
        layout.addWidget(self.top_ten_neighbourhoods_btn, 0, 0, 1, 1)

        self.percent_rgi_btn = SquareButton() 
        image_path = r"images\neighbourhoods\percentage_of_rgi_units_by_year_built.png"
        self.percent_rgi_btn.setIcon(QIcon(QPixmap(image_path)))
        self.percent_rgi_btn.clicked.connect(lambda: stacked_widget.setCurrentIndex(9))
        layout.addWidget(self.percent_rgi_btn, 0, 1, 1, 1)

        self.short_summary_btn = SquareButton() 
        image_path = r"images\neighbourhoods\short_summary.png"
        self.short_summary_btn.setIcon(QIcon(QPixmap(image_path)))
        self.short_summary_btn.clicked.connect(lambda: stacked_widget.setCurrentIndex(10))
        layout.addWidget(self.short_summary_btn, 0, 2, 1, 1)

        self.build_by_decade_btn = SquareButton() 
        image_path = r"images\neighbourhoods\total_buildings_built_per_decade.png"
        self.build_by_decade_btn.setIcon(QIcon(QPixmap(image_path)))
        self.build_by_decade_btn.clicked.connect(lambda: stacked_widget.setCurrentIndex(11))
        layout.addWidget(self.build_by_decade_btn, 1, 0, 1, 1)

        self.unit_by_decade_btn = SquareButton() 
        image_path = r"images\neighbourhoods\total_units_built_per_decade.png"
        self.unit_by_decade_btn.setIcon(QIcon(QPixmap(image_path)))
        self.unit_by_decade_btn.clicked.connect(lambda: stacked_widget.setCurrentIndex(12))
        layout.addWidget(self.unit_by_decade_btn, 1, 1, 1, 1)

        self.fun_statistics = QTextEdit() 
        self.fun_statistics.setPlainText("Pre-1970 housing developments often had RGI shares close to 100%, reflecting a strong focus on deeply affordable housing.\n\nBy 2010+, RGI units made up a significantly smaller share, often below 30% in new builds, indicating a shift toward market-rate or mixed-income housing.")
        self.fun_statistics.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        layout.addWidget(self.fun_statistics, 1, 2, 1, 1)

        back_button = QPushButton("Back")
        back_button.clicked.connect(lambda: stacked_widget.setCurrentIndex(0))
        layout.addWidget(back_button, 2, 0, 1, 3)

        self.setLayout(layout)
#-------------------------------------------------
# EXAMPLE PAGE 
class ExamplePage(QWidget):
    def __init__(self, stacked_widget):
        super().__init__()
        layout = QVBoxLayout()
        layout.addWidget(QLabel("This is the EXAMPLE page."))

        back_button = QPushButton("Back")
        back_button.clicked.connect(lambda: stacked_widget.setCurrentIndex(0))
        layout.addWidget(back_button)

        self.setLayout(layout)
#-------------------------------------------------

class WardPageTemplate(QWidget):
    def __init__(self, stacked_widget, page_type):
        super().__init__()
        layout = QVBoxLayout()
        layout.addWidget(QLabel(f"This is the {page_type}"))

# add stats - to be fixed
        try:
            import os
            print("Looking for:", os.path.abspath(f"statistics/{page_type}.txt"))

            text = pd.read_csv(f"statistics/{page_type}.txt", delimiter="\t", dtype=str).to_string(index=False)
            text_box = QTextEdit()
            text_box.setPlainText(text)
            text_box.setReadOnly(True)
            layout.addWidget(text_box)

        except FileNotFoundError:
            layout.addWidget(QLabel("Statistics file not found."))

        back_button = QPushButton("Back")
        back_button.clicked.connect(lambda: stacked_widget.setCurrentIndex(1))
        layout.addWidget(back_button)

        self.setLayout(layout)

class NeighbourhoodPageTemplate(QWidget):
    def __init__(self, stacked_widget, page_type):
        super().__init__()
        layout = QVBoxLayout()
        layout.addWidget(QLabel(f"This is the {page_type}"))
      #  layout.addWidget(QLabel(f"Statistics: {page_stats}"))


        try:
            import os
            print("Looking for:", os.path.abspath(f"statistics/{page_type}.txt"))

            text = pd.read_csv(f"statistics/{page_type}.txt", delimiter="\t", dtype=str).to_string(index=False)
            text_box = QTextEdit()
            text_box.setPlainText(text)
            text_box.setReadOnly(True)
            layout.addWidget(text_box)

        except FileNotFoundError:
            layout.addWidget(QLabel("Statistics file not found."))

        back_button = QPushButton("Back")
        back_button.clicked.connect(lambda: stacked_widget.setCurrentIndex(2))
        layout.addWidget(back_button)

        self.setLayout(layout)

def createPages(stacked_widget, page_type):
    match page_type:
        case 1:
            return WardPageTemplate(stacked_widget, "wards_in_need")
        case 2:
            return WardPageTemplate(stacked_widget, "aff_rgi_control")
        case 3:
             return WardPageTemplate(stacked_widget, "ehon")
        case 4:
             return WardPageTemplate(stacked_widget, "income")
        case 5:
             return WardPageTemplate(stacked_widget, "renter")
        case 6:
            return NeighbourhoodPageTemplate(stacked_widget, "top_ten_neighbourhoods")
        case 7:
            return NeighbourhoodPageTemplate(stacked_widget, "percent_rgi")
        case 8:
            return NeighbourhoodPageTemplate(stacked_widget, "short_summary") 
        case 9:
            return NeighbourhoodPageTemplate(stacked_widget, "build_by_decade")
        case 10:
            return NeighbourhoodPageTemplate(stacked_widget, "unit_by_decade")


if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Create a stacked widget
    stacked_widget = QStackedWidget()

    # Create pages
    main_page = AddressLookupApp(stacked_widget)
    ward_page = WardPage(stacked_widget)
    neighbourhood_page = NeighbourhoodPage(stacked_widget)
    wards_in_need = createPages(stacked_widget, 1)
    aff_rgi_control = createPages(stacked_widget, 2)
    ehon = createPages(stacked_widget, 3)
    income = createPages(stacked_widget, 4)
    renter = createPages(stacked_widget, 5)
    
    top_ten_neighbourhoods = createPages(stacked_widget, 6)
    percent_rgi = createPages(stacked_widget, 7)
    short_summary = createPages(stacked_widget, 8) 
    build_by_decade = createPages(stacked_widget, 9)
    unit_by_decade = createPages(stacked_widget, 10)  
      

    # Add pages to the stack
    stacked_widget.addWidget(main_page)           # index 0
    stacked_widget.addWidget(ward_page)           # index 1
    stacked_widget.addWidget(neighbourhood_page)  # index 2

    stacked_widget.addWidget(wards_in_need)       # index 3
    stacked_widget.addWidget(aff_rgi_control)     # index 4
    stacked_widget.addWidget(ehon)                # index 5
    stacked_widget.addWidget(income)              # index 6
    stacked_widget.addWidget(renter)              # index 7
    stacked_widget.addWidget(top_ten_neighbourhoods) # index 8
    stacked_widget.addWidget(percent_rgi)            # index 9
    stacked_widget.addWidget(short_summary)                # index 10 
    stacked_widget.addWidget(build_by_decade)        # index 11
    stacked_widget.addWidget(unit_by_decade)         # index 12

    
    # Show main window
    stacked_widget.resize(800, 600)
    stacked_widget.show()

    sys.exit(app.exec())
