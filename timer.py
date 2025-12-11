import sys
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                             QHBoxLayout, QLabel, QPushButton, QTabWidget,
                             QListWidget, QSpinBox, QMessageBox)
from PyQt6.QtCore import QTimer, Qt
from PyQt6.QtGui import QAction, QFont


BTN_BASE = "border-radius: 40px; font-size: 16px; font-weight: bold; padding: 10px;"
BTN_GREEN = f"{BTN_BASE} background-color: #34C759; color: #FFFFFF;"
BTN_RED = f"{BTN_BASE} background-color: #FF3B30; color: #FFFFFF;"

DARK_THEME = {
    "bg": "#000000",
    "fg": "#FFFFFF",
    "tab_bg": "#1C1C1E",
    "tab_sel": "#2C2C2E",
    "btn_lap": "#3A3A3C",
    "btn_lap_text": "#FFFFFF",
    "input_bg": "#1C1C1E"
}

LIGHT_THEME = {
    "bg": "#F2F2F7",
    "fg": "#000000",
    "tab_bg": "#E5E5EA",
    "tab_sel": "#FFFFFF",
    "btn_lap": "#D1D1D6",
    "btn_lap_text": "#000000",
    "input_bg": "#FFFFFF"
}


class IPhoneClockApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("iClock Lab (PyQt)")
        self.setGeometry(100, 100, 400, 700)
        self.setMinimumSize(350, 500)
        self.is_dark = True
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.main_layout = QVBoxLayout(self.central_widget)
        self.create_menu()
        self.tabs = QTabWidget()
        self.main_layout.addWidget(self.tabs)
        self.init_stopwatch_tab()
        self.init_timer_tab()
        self.init_footer()
        self.apply_theme()

    def create_menu(self):
        menu_bar = self.menuBar()
        file_menu = menu_bar.addMenu("Файл")
        exit_action = QAction("Выход", self)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

        help_menu = menu_bar.addMenu("Помощь")
        about_action = QAction("О программе", self)
        about_action.triggered.connect(lambda: QMessageBox.information(self, "Info", "Clock App v2.0"))
        help_menu.addAction(about_action)

    def init_footer(self):
        footer_layout = QHBoxLayout()
        footer_layout.addStretch()

        self.btn_theme = QPushButton("☀️/🌙")
        self.btn_theme.setFixedSize(60, 40)
        self.btn_theme.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_theme.setStyleSheet("border-radius: 10px; font-size: 20px;")
        self.btn_theme.clicked.connect(self.toggle_theme)

        footer_layout.addWidget(self.btn_theme)
        self.main_layout.addLayout(footer_layout)

    def toggle_theme(self):
        self.is_dark = not self.is_dark
        self.apply_theme()

    def apply_theme(self):
        t = DARK_THEME if self.is_dark else LIGHT_THEME

        qss = f"""
        QMainWindow, QWidget {{ background-color: {t['bg']}; color: {t['fg']}; }}
        QLabel {{ color: {t['fg']}; }}
        QTabWidget::pane {{ border: 0; }}
        QTabBar::tab {{
            background: {t['tab_bg']}; color: #888888;
            padding: 10px 20px;
            border-top-left-radius: 6px; border-top-right-radius: 6px;
        }}
        QTabBar::tab:selected {{ background: {t['tab_sel']}; color: {t['fg']}; }}
        QListWidget {{ background-color: {t['bg']}; color: {t['fg']}; border: none; font-size: 16px; }}
        QSpinBox {{ 
            background-color: {t['input_bg']}; color: {t['fg']}; 
            font-size: 20px; padding: 10px; border-radius: 5px; 
        }}
        QMenuBar {{ background-color: {t['tab_bg']}; color: {t['fg']}; }}
        QMenuBar::item:selected {{ background-color: {t['tab_sel']}; }}
        QMenu {{ background-color: {t['tab_bg']}; color: {t['fg']}; }}
        """
        self.setStyleSheet(qss)

        lap_style = f"{BTN_BASE} background-color: {t['btn_lap']}; color: {t['btn_lap_text']};"
        self.sw_lap_btn.setStyleSheet(lap_style)

        btn_theme_bg = "#333333" if not self.is_dark else "#DDDDDD"
        self.btn_theme.setStyleSheet(f"background-color: {btn_theme_bg}; border-radius: 10px; font-size: 16px")

    def init_stopwatch_tab(self):
        self.sw_tab = QWidget()
        layout = QVBoxLayout()

        self.sw_label = QLabel("00:00.00")
        self.sw_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.sw_label.setFont(QFont("Helvetica", 60))
        layout.addWidget(self.sw_label)

        btn_layout = QHBoxLayout()

        self.sw_lap_btn = QPushButton("Круг")
        self.sw_lap_btn.setFixedSize(80, 80)
        self.sw_lap_btn.clicked.connect(self.sw_lap_action)

        self.sw_start_btn = QPushButton("Старт")
        self.sw_start_btn.setFixedSize(80, 80)
        self.sw_start_btn.setStyleSheet(BTN_GREEN)
        self.sw_start_btn.clicked.connect(self.sw_toggle)

        btn_layout.addWidget(self.sw_lap_btn)
        btn_layout.addStretch()
        btn_layout.addWidget(self.sw_start_btn)
        layout.addLayout(btn_layout)

        self.sw_list = QListWidget()
        layout.addWidget(self.sw_list)

        self.sw_tab.setLayout(layout)
        self.tabs.addTab(self.sw_tab, "Секундомер")

        self.sw_timer = QTimer()
        self.sw_timer.timeout.connect(self.sw_update)
        self.sw_time_ms = 0
        self.sw_running = False

    def sw_toggle(self):
        if not self.sw_running:
            self.sw_running = True
            self.sw_timer.start(10)
            self.sw_start_btn.setText("Стоп")
            self.sw_start_btn.setStyleSheet(BTN_RED)
            self.sw_lap_btn.setText("Круг")
        else:
            self.sw_running = False
            self.sw_timer.stop()
            self.sw_start_btn.setText("Старт")
            self.sw_start_btn.setStyleSheet(BTN_GREEN)
            self.sw_lap_btn.setText("Сброс")

    def sw_update(self):
        self.sw_time_ms += 10
        self.sw_label.setText(self.format_time(self.sw_time_ms, include_ms=True))

    def sw_lap_action(self):
        if self.sw_running:
            cur = self.format_time(self.sw_time_ms, include_ms=True)
            self.sw_list.insertItem(0, f"Круг {self.sw_list.count() + 1}: {cur}")
        else:
            self.sw_time_ms = 0
            self.sw_label.setText("00:00.00")
            self.sw_list.clear()
            self.sw_lap_btn.setText("Круг")

    def init_timer_tab(self):
        self.tm_tab = QWidget()
        layout = QVBoxLayout()

        input_layout = QHBoxLayout()
        self.spin_h = QSpinBox()
        self.spin_h.setSuffix(" ч")
        self.spin_m = QSpinBox()
        self.spin_m.setSuffix(" м")
        self.spin_s = QSpinBox()
        self.spin_s.setSuffix(" с")

        for s in [self.spin_h, self.spin_m, self.spin_s]:
            s.setRange(0, 59)
            s.setFixedSize(90, 50)
            input_layout.addWidget(s)
        self.spin_h.setRange(0, 23)

        layout.addLayout(input_layout)

        self.tm_label = QLabel("00:00:00")
        self.tm_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.tm_label.setFont(QFont("Helvetica", 50))
        layout.addWidget(self.tm_label)

        self.tm_start_btn = QPushButton("Начать")
        self.tm_start_btn.setFixedSize(200, 60)
        self.tm_start_btn.setStyleSheet(BTN_GREEN)
        self.tm_start_btn.clicked.connect(self.tm_toggle)

        cont = QHBoxLayout()
        cont.addStretch()
        cont.addWidget(self.tm_start_btn)
        cont.addStretch()
        layout.addLayout(cont)
        layout.addStretch()

        self.tm_tab.setLayout(layout)
        self.tabs.addTab(self.tm_tab, "Таймер")

        self.tm_timer = QTimer()
        self.tm_timer.timeout.connect(self.tm_update)
        self.tm_total = 0
        self.tm_running = False

    def tm_toggle(self):
        try:
            if not self.tm_running:
                total = self.spin_h.value() * 3600 + self.spin_m.value() * 60 + self.spin_s.value()
                if total <= 0: raise ValueError("Установите время!")
                self.tm_total = total
                self.tm_running = True
                self.tm_start_btn.setText("Отмена")
                self.tm_start_btn.setStyleSheet(BTN_RED)
                self.set_inputs(False)
                self.tm_update_lbl()
                self.tm_timer.start(1000)
            else:
                self.tm_reset()
        except Exception as e:
            QMessageBox.warning(self, "Ошибка", str(e))

    def tm_update(self):
        if self.tm_total > 0:
            self.tm_total -= 1
            self.tm_update_lbl()
        else:
            self.tm_reset()
            QMessageBox.information(self, "Таймер", "Время вышло!")

    def tm_reset(self):
        self.tm_running = False
        self.tm_timer.stop()
        self.tm_start_btn.setText("Начать")
        self.tm_start_btn.setStyleSheet(BTN_GREEN)
        self.set_inputs(True)
        self.tm_label.setText("00:00:00")

    def tm_update_lbl(self):
        self.tm_label.setText(self.format_time(self.tm_total * 1000))

    def set_inputs(self, val):
        self.spin_h.setEnabled(val)
        self.spin_m.setEnabled(val)
        self.spin_s.setEnabled(val)

    def format_time(self, total_ms, include_ms=False):
        seconds = (total_ms // 1000) % 60
        minutes = (total_ms // 60000) % 60
        hours = (total_ms // 3600000)

        if include_ms:
            millis = (total_ms % 1000) // 10
            return f"{minutes:02}:{seconds:02}.{millis:02}"
        else:
            return f"{hours:02}:{minutes:02}:{seconds:02}"


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = IPhoneClockApp()
    win.show()
    sys.exit(app.exec())