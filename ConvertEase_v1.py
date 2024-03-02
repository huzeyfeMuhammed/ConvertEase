import sys
import locale
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QLabel, QPushButton, QComboBox, QTabWidget, QGridLayout
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPalette



class ConverterApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Converter App")

        self.tab_widget = QTabWidget()
        self.converter_tab = ConverterTab()
        self.airport_tab = AirportTab()

        self.tab_widget.addTab(self.converter_tab, "Fuel Converter")
        self.tab_widget.addTab(self.airport_tab, "Airport Database")

        layout = QVBoxLayout()
        layout.addWidget(self.tab_widget)
        self.setLayout(layout)

class ConverterTab(QWidget):
    def __init__(self):
        super().__init__()
        self.setGeometry(100, 100, 400, 300)

        locale.setlocale(locale.LC_NUMERIC, '')
        self.decimal_point = locale.localeconv()['decimal_point']
        self.init_input_fields()
        self.input_quantity.setFocus()
        self.init_result_labels()
        self.init_buttons()
        self.init_labels()
        self.setup_layout()
        self.connect_signals()


    def text_to_number(self, text):
        try:
            text = text.replace(",", "")
            number = float(text)
            return number
        except ValueError:
            return 0.0
        

    def init_input_fields(self):
        self.input_quantity = self.create_input_field("Quantity")
        self.density_input = self.create_input_field("Density")
        self.price_input = self.create_input_field("Price")

        self.unit_combobox = QComboBox()
        self.unit_combobox.addItems(["Lt to USG", "USG to Lt"])
        self.unit_combobox.setCurrentText("Lt to USG")

    def create_input_field(self, placeholder):
        input_field = QLineEdit()
        input_field.setPlaceholderText(placeholder)
        input_field.setAlignment(Qt.AlignCenter)
        return input_field

    def init_result_labels(self):
        self.result_label = self.create_result_label("")
        self.metric_ton_label = self.create_result_label("")
        self.total_value_label = self.create_result_label("")

    def init_labels(self):
        self.r_label = self.create_result_label("Gallons:")
        self.m_ton_label = self.create_result_label("Metric Tons:")
        self.t_value_label = self.create_result_label("Total Value:")

    def create_result_label(self, text=""):
        result_label = QLabel(text)
        result_label.setAlignment(Qt.AlignCenter)
        return result_label

    def init_buttons(self):
        self.copy_gallon_button = self.create_button("Copy", self.copy_gallon_result)
        self.copy_metric_ton_button = self.create_button("Copy", self.copy_metric_ton_result)
        self.copy_total_value_button = self.create_button("Copy", self.copy_total_value_result)
        self.clear_button = self.create_button("Clear", self.clear_quantity)

    def create_button(self, text, command):
        button = QPushButton(text)
        button.clicked.connect(command)
        return button

    def setup_layout(self):
        main_layout = QVBoxLayout()

        input_layout = QVBoxLayout()
        input_layout.addWidget(self.unit_combobox)
        input_layout.addWidget(self.input_quantity)
        input_layout.addWidget(self.price_input)
        input_layout.addWidget(self.density_input)

        button_layout = QVBoxLayout()
        button_layout.addWidget(self.clear_button)

        result_layout = QVBoxLayout()
        result_layout.addWidget(self.r_label)
        result_layout.addWidget(self.result_label)
        result_layout.addWidget(self.t_value_label)
        result_layout.addWidget(self.total_value_label)
        result_layout.addWidget(self.m_ton_label)
        result_layout.addWidget(self.metric_ton_label)

        button_result_layout = QVBoxLayout()
        button_result_layout.addWidget(self.copy_gallon_button)
        button_result_layout.addWidget(self.copy_total_value_button)
        button_result_layout.addWidget(self.copy_metric_ton_button)

        main_layout.addLayout(input_layout)

        # Create a horizontal layout to hold result labels and buttons
        result_button_layout = QHBoxLayout()
        result_button_layout.addLayout(result_layout)
        result_button_layout.addLayout(button_result_layout)

        main_layout.addLayout(result_button_layout)
        main_layout.addLayout(button_layout)

        self.setLayout(main_layout)


    def connect_signals(self):
        self.input_quantity.textChanged.connect(self.convert_units)
        self.density_input.textChanged.connect(self.convert_units)
        self.price_input.textChanged.connect(self.convert_units)
        self.unit_combobox.currentIndexChanged.connect(self.convert_units)

    def convert_units(self):
        try:
            input_text = self.input_quantity.text()

            if not input_text:
                self.clear_result_labels()
                return


            result =  self.text_to_number(input_text)

            density_text = self.density_input.text()
            if not density_text:
                density_text = "0.8" 
            density = self.text_to_number(density_text)

            price_text = self.price_input.text()
            price = self.text_to_number(price_text)

            selected_unit = self.unit_combobox.currentText()

            gallons = 0

            if "Lt to USG" in selected_unit:
                self.r_label.setText("Gallons")
                self.copy_gallon_button.setText("Copy")
                gallons = result / 3.785
            elif "USG to Lt" in selected_unit:
                self.r_label.setText("Liters")
                self.copy_gallon_button.setText("Copy")

                gallons = result * 3.785
                

            metric_ton_temp = (result / 1000) * density

            formatted_gallons = "{:,.2f}".format(gallons)
            formatted_metric_ton = "{:,.4f}".format(metric_ton_temp)

            self.result_label.setText(formatted_gallons)
            self.metric_ton_label.setText(formatted_metric_ton)

            total_value = gallons * price
            formatted_total_value = "{:,.2f}".format(total_value)
            self.total_value_label.setText(formatted_total_value)

            self.update_label_colors_size()

        except ValueError:
            self.clear_result_labels()

    def update_label_colors_size(self):
        font = self.result_label.font()
        font.setBold(True)  
        self.result_label.setFont(font)
        
        font = self.metric_ton_label.font()
        font.setBold(True)
        self.metric_ton_label.setFont(font)
        
        font = self.total_value_label.font()
        font.setBold(True)
        self.total_value_label.setFont(font)
        

    def clear_result_labels(self):
        self.result_label.setText("")
        self.metric_ton_label.setText("")
        self.total_value_label.setText("")


    def clear_quantity(self):
        self.input_quantity.clear()
        self.input_quantity.setPlaceholderText("Quantity")

        self.price_input.clear()
        self.price_input.setPlaceholderText("Price")

        self.density_input.clear()
        self.density_input.setPlaceholderText("Density")

        self.clear_result_labels()

    def copy_gallon_result(self):
        self.copy_to_clipboard(self.result_label.text(), remove_thousands_separator=True)

    def copy_metric_ton_result(self):
        self.copy_to_clipboard(self.metric_ton_label.text(), remove_thousands_separator=True)

    def copy_total_value_result(self):
        self.copy_to_clipboard(self.total_value_label.text(), remove_thousands_separator=True)

    def copy_to_clipboard(self, text, remove_thousands_separator=False):
        if remove_thousands_separator:
            text = text.replace(",", "")
        QApplication.clipboard().setText(text)

class AirportTab(QWidget):
    def __init__(self):
        super().__init__()
        self.setGeometry(100, 100, 1000, 200)

        layout = QGridLayout()

        # Adding ComboBox for selecting conversion direction for origin airport
        self.comboBox_origin = QComboBox()
        self.comboBox_origin.addItem("IATA to ICAO")
        self.comboBox_origin.addItem("ICAO to IATA")
        self.comboBox_origin.currentIndexChanged.connect(self.on_combobox_changed)
        layout.addWidget(self.comboBox_origin, 0, 0, 1, 2)

        self.line_edit_input_origin = QLineEdit()
        self.line_edit_input_origin.setPlaceholderText("Enter IATA")
        self.line_edit_input_origin.textChanged.connect(self.show_info_origin)
        layout.addWidget(self.line_edit_input_origin, 1, 0, 1, 2)

        # Adding ComboBox for selecting conversion direction for destination airport
        self.comboBox_destination = QComboBox()
        self.comboBox_destination.addItem("IATA to ICAO")
        self.comboBox_destination.addItem("ICAO to IATA")
        self.comboBox_destination.currentIndexChanged.connect(self.on_combobox_changed)
        layout.addWidget(self.comboBox_destination, 0, 2, 1, 2)

        self.line_edit_input_destination = QLineEdit()
        self.line_edit_input_destination.setPlaceholderText("Enter IATA")
        self.line_edit_input_destination.textChanged.connect(self.show_info_destination)
        layout.addWidget(self.line_edit_input_destination, 1, 2, 1, 2)

        # Initially set the label to ICAO for origin airport
        self.label_output_origin = QLabel("ICAO:")
        layout.addWidget(self.label_output_origin, 2, 0)
        self.label_output_value_origin = QLabel()
        layout.addWidget(self.label_output_value_origin, 2, 1)

        # Initially set the label to ICAO for destination airport
        self.label_output_destination = QLabel("ICAO:")
        layout.addWidget(self.label_output_destination, 2, 2)
        self.label_output_value_destination = QLabel()
        layout.addWidget(self.label_output_value_destination, 2, 3)

        self.label_airport_name_origin = QLabel("Airport Name:")
        layout.addWidget(self.label_airport_name_origin, 3, 0)
        self.label_airport_name_value_origin = QLabel()
        layout.addWidget(self.label_airport_name_value_origin, 3, 1)

        self.label_airport_name_destination = QLabel("Airport Name:")
        layout.addWidget(self.label_airport_name_destination, 3, 2)
        self.label_airport_name_value_destination = QLabel()
        layout.addWidget(self.label_airport_name_value_destination, 3, 3)

        self.label_country_origin = QLabel("Country:")
        layout.addWidget(self.label_country_origin, 4, 0)
        self.label_country_value_origin = QLabel()
        layout.addWidget(self.label_country_value_origin, 4, 1)

        self.label_country_destination = QLabel("Country:")
        layout.addWidget(self.label_country_destination, 4, 2)
        self.label_country_value_destination = QLabel()
        layout.addWidget(self.label_country_value_destination, 4, 3)

        self.label_city_origin = QLabel("City:")
        layout.addWidget(self.label_city_origin, 5, 0)
        self.label_city_value_origin = QLabel()
        layout.addWidget(self.label_city_value_origin, 5, 1)

        self.label_city_destination = QLabel("City:")
        layout.addWidget(self.label_city_destination, 5, 2)
        self.label_city_value_destination = QLabel()
        layout.addWidget(self.label_city_value_destination, 5, 3)

        self.copy_button_origin = QPushButton("Copy")
        self.copy_button_origin.clicked.connect(self.copy_value_origin)
        layout.addWidget(self.copy_button_origin, 6, 0, 1, 2)

        self.copy_button_destination = QPushButton("Copy")
        self.copy_button_destination.clicked.connect(self.copy_value_destination)
        layout.addWidget(self.copy_button_destination, 6, 2, 1, 2)

        self.setLayout(layout)

        self.airports_iata = {}
        self.airports_icao = {}
        self.load_airports()

    def load_airports(self):
        with open("Airports Database - Sheet1.csv", "r", encoding="utf-8") as file:
            headers = file.readline().strip().split(",")
            for line in file:
                values = line.strip().split(",")
                airport_info = dict(zip(headers, values))
                self.airports_iata[airport_info['IATA']] = airport_info
                self.airports_icao[airport_info['ICAO']] = airport_info

    def show_info_origin(self, text):
        if self.comboBox_origin.currentIndex() == 0:  # IATA to ICAO
            iata = text.upper()
            airport_info = self.airports_iata.get(iata, {})
            self.label_output_origin.setText("ICAO:")
            self.label_output_value_origin.setText(airport_info.get('ICAO', ''))
        else:  # ICAO to IATA
            icao = text.upper()
            airport_info = self.airports_icao.get(icao, {})
            self.label_output_origin.setText("IATA:")
            self.label_output_value_origin.setText(airport_info.get('IATA', ''))

        self.label_airport_name_value_origin.setText(airport_info.get('Airport Name', ''))
        self.label_country_value_origin.setText(airport_info.get('Country', ''))
        self.label_city_value_origin.setText(airport_info.get('City', ''))

    def show_info_destination(self, text):
        if self.comboBox_destination.currentIndex() == 0:  # IATA to ICAO
            iata = text.upper()
            airport_info = self.airports_iata.get(iata, {})
            self.label_output_destination.setText("ICAO:")
            self.label_output_value_destination.setText(airport_info.get('ICAO', ''))
        else:  # ICAO to IATA
            icao = text.upper()
            airport_info = self.airports_icao.get(icao, {})
            self.label_output_destination.setText("IATA:")
            self.label_output_value_destination.setText(airport_info.get('IATA', ''))

        self.label_airport_name_value_destination.setText(airport_info.get('Airport Name', ''))
        self.label_country_value_destination.setText(airport_info.get('Country', ''))
        self.label_city_value_destination.setText(airport_info.get('City', ''))

    def copy_value_origin(self):
        value = self.label_output_value_origin.text()
        QApplication.clipboard().setText(value)

    def copy_value_destination(self):
        value = self.label_output_value_destination.text()
        QApplication.clipboard().setText(value)

    def on_combobox_changed(self, index):
        if index == 0:  # IATA to ICAO
            self.line_edit_input_origin.setPlaceholderText("Enter IATA")
            self.line_edit_input_destination.setPlaceholderText("Enter IATA")

            if self.comboBox_origin.currentIndex() == 0:  # IATA to ICAO
                self.line_edit_input_origin.setPlaceholderText("Enter IATA")
            else:  # ICAO to IATA
                self.line_edit_input_origin.setPlaceholderText("Enter ICAO")

        else:  # ICAO to IATA
            self.line_edit_input_origin.setPlaceholderText("Enter ICAO")
            self.line_edit_input_destination.setPlaceholderText("Enter ICAO")

            if self.comboBox_destination.currentIndex() == 0:  # IATA to ICAO
                self.line_edit_input_destination.setPlaceholderText("Enter IATA")
            else:  # ICAO to IATA
                self.line_edit_input_destination.setPlaceholderText("Enter ICAO")

        self.show_info_origin(self.line_edit_input_origin.text())
        self.show_info_destination(self.line_edit_input_destination.text())
        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    converter_app = ConverterApp()
    converter_app.show()
    sys.exit(app.exec_())
