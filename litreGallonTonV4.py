import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QLineEdit, QVBoxLayout, QWidget, QComboBox
from PyQt5.QtCore import Qt

class ConverterApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.total_value_text = "أدخل رقماً"  # قيمة افتراضية
        self.selected_unit = "من لتر إلى جالون أميركي"  # تحديد القيمة الافتراضية
        self.initUI()

    def initUI(self):
        self.setGeometry(100, 100, 500, 300)
        self.setWindowTitle("تحويل بين لتر وجالون وحساب الطن المتري")

        self.input_quantity = QLineEdit(self)
        self.input_quantity.setPlaceholderText("الكمية")
        font = self.input_quantity.font()
        font.setPointSize(18)

        self.density_input = QLineEdit(self)
        self.density_input.setPlaceholderText("الكثافة")
        self.density_input.setText("0.8")  # تعيين قيمة افتراضية للكثافة
        font = self.density_input.font()
        font.setPointSize(18)

        self.price_input = QLineEdit(self)
        self.price_input.setPlaceholderText("السعر")
        font = self.price_input.font()
        font.setPointSize(18)

        self.unit_combobox = QComboBox(self)
        self.unit_combobox.addItems(["من لتر إلى جالون أميركي", "من جالون أميركي إلى لتر"])
        font = self.unit_combobox.font()

        self.result_label = QLabel(self)
        self.result_label.setAlignment(Qt.AlignCenter)
        font = self.result_label.font()
        font.setPointSize(18)

        self.metric_ton_label = QLabel(self)
        self.metric_ton_label.setAlignment(Qt.AlignCenter)

        self.total_value_label = QLabel(self)
        self.total_value_label.setAlignment(Qt.AlignCenter)
        total_value_font = self.total_value_label.font()
        total_value_font.setPointSize(18)

        self.result_label_text = QLabel(self)
        self.result_label_text.setText("نتيجة التحويل: ")
        self.result_label_text.setAlignment(Qt.AlignCenter)

        self.metric_ton_label_text = QLabel(self)
        self.metric_ton_label_text.setText("نتيجة الطن المتري: ")
        self.metric_ton_label_text.setAlignment(Qt.AlignCenter)

        self.total_value_label_text = QLabel(self)
        self.total_value_label_text.setText("القيمة: ")
        self.total_value_label_text.setAlignment(Qt.AlignCenter)

        button_height = 55
        button_font_size = 16
        clear_button_height = 30
        clear_button_font_size = 10
        result_font_size = 18
        font_size = 14

        self.copy_gallon_button = QPushButton("نسخ نتيجة التحويل", self)
        self.copy_gallon_button.setFixedHeight(button_height)
        font = self.copy_gallon_button.font()
        font.setPointSize(button_font_size)

        self.copy_metric_ton_button = QPushButton("نسخ نتيجة الطن المتري", self)
        self.copy_metric_ton_button.setFixedHeight(button_height)
        font = self.copy_metric_ton_button.font()
        font.setPointSize(button_font_size)

        self.clear_button = QPushButton("مسح", self)
        self.clear_button.setFixedHeight(clear_button_height)

        self.copy_total_value_button = QPushButton("نسخ القيمة", self)
        self.copy_total_value_button.setFixedHeight(button_height)
        font = self.copy_total_value_button.font()
        font.setPointSize(button_font_size)

        self.copy_gallon_button.setStyleSheet("font-size: {}pt;".format(button_font_size))
        self.copy_metric_ton_button.setStyleSheet("font-size: {}pt;".format(button_font_size))
        self.clear_button.setStyleSheet("font-size: {}pt;".format(clear_button_font_size))
        self.copy_total_value_button.setStyleSheet("font-size: {}pt;".format(button_font_size))

        self.result_label_text.setStyleSheet("font-size: {}pt;".format(result_font_size))
        self.metric_ton_label_text.setStyleSheet("font-size: {}pt;".format(result_font_size))
        self.total_value_label_text.setStyleSheet("font-size: {}pt;".format(result_font_size))

        self.clear_button.clicked.connect(self.clear_quantity)
        self.copy_gallon_button.clicked.connect(self.copy_gallon_result)
        self.copy_metric_ton_button.clicked.connect(self.copy_metric_ton_result)
        self.copy_total_value_button.clicked.connect(self.copy_total_value_result)

        button_layout = QVBoxLayout()
        button_layout.addWidget(self.clear_button)
        button_layout.addWidget(self.result_label_text)
        button_layout.addWidget(self.result_label)
        button_layout.addWidget(self.copy_gallon_button)
        button_layout.addWidget(self.metric_ton_label_text)
        button_layout.addWidget(self.metric_ton_label)
        button_layout.addWidget(self.copy_metric_ton_button)
        button_layout.addWidget(self.total_value_label_text)
        button_layout.addWidget(self.total_value_label)
        button_layout.addWidget(self.copy_total_value_button)

        layout = QVBoxLayout()
        layout.addWidget(self.input_quantity)
        layout.addWidget(self.density_input)
        layout.addWidget(self.price_input)
        layout.addWidget(self.unit_combobox)
        layout.addLayout(button_layout)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        self.input_quantity.textChanged.connect(self.convert_units)
        self.density_input.textChanged.connect(self.convert_units)
        self.price_input.textChanged.connect(self.convert_units)
        self.unit_combobox.currentIndexChanged.connect(self.convert_units)

    def convert_units(self):
        print(f"Selected Unit: {selected_unit}")  # إضافة هذا السطر لفحص القيمة المسترجعة

        try:
            quantity_text = self.input_quantity.text()

            if not quantity_text:
                self.clear_result_labels()
                return

            # تحديد إذا كانت هناك فاصلة واحدة فقط
            if ',' in quantity_text and '.' not in quantity_text:
                # استبدال الفاصلة بالنقطة العشرية إذا كان هناك فاصلة واحدة فقط
                quantity_text = quantity_text.replace(',', '.')
            else:
                # استبدال الفواصل بفارغة والنقاط بالنقطة العشرية في حالة وجودها
                quantity_text = quantity_text.replace(',', '').replace('.', '.')

            quantity = float(quantity_text)

            density_text = self.density_input.text() or '0.8'
            density = float(density_text.replace(',', '').replace('.', '.'))

            price_text = self.price_input.text() or '0.0'
            price = float(price_text.replace(',', '').replace('.', '.'))

            selected_unit = self.unit_combobox.currentText()

            if "من لتر إلى جالون أميركي" in selected_unit:
                gallons = quantity / 3.785
                metric_ton_temp = (quantity / 1000) * density
            elif "من جالون أميركي إلى لتر" in selected_unit:
                gallons = quantity * 3.785
                metric_ton_temp = (quantity / 1000) * density

            formatted_gallons = "{:,.2f}".format(gallons)
            formatted_metric_ton = "{:,.4f}".format(metric_ton_temp)

            self.result_label.setText(formatted_gallons)
            self.metric_ton_label.setText(formatted_metric_ton)

            total_value = metric_ton_temp * price
            formatted_total_value = "{:,.4f}".format(total_value)
            self.total_value_label.setText(formatted_total_value)

            self.update_label_colors_size()

        except ValueError:
            self.clear_result_labels()

    def update_label_colors_size(self):
        self.result_label.setStyleSheet("color: blue; font-size: 18pt")
        self.metric_ton_label.setStyleSheet("color: red;font-size: 18pt")
        self.total_value_label.setStyleSheet("color: green;font-size: 18pt")

    def clear_result_labels(self):
        self.result_label.clear()
        self.metric_ton_label.clear()
        self.total_value_label.setText(self.total_value_text)

    def clear_quantity(self):
        self.input_quantity.clear()
        self.density_input.clear()
        self.price_input.clear()
        self.clear_result_labels()

    def copy_gallon_result(self):
        self.copy_to_clipboard(self.result_label.text())

    def copy_metric_ton_result(self):
        self.copy_to_clipboard(self.metric_ton_label.text())

    def copy_total_value_result(self):
        self.copy_to_clipboard(self.total_value_label.text())

    def copy_to_clipboard(self, text):
        clipboard = QApplication.clipboard()
        clipboard.setText(text)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ConverterApp()
    window.show()
    sys.exit(app.exec_())