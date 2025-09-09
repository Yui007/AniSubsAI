def get_dark_theme():
    return """
        QWidget {
            background-color: #1a1a1a;
            color: #e0e0e0;
            font-family: "Segoe UI", "Roboto", "Helvetica Neue", "Arial", sans-serif;
        }
        QMainWindow {
            background-color: #1a1a1a;
        }
        QTextEdit {
            background-color: #2a2a2a;
            border: 1px solid #3a3a3a;
            border-radius: 8px;
            padding: 8px;
            font-size: 14px;
        }
        QPushButton {
            background-color: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #8e2de2, stop:1 #4a00e0);
            color: white;
            border: none;
            border-radius: 12px;
            padding: 12px 24px;
            font-size: 16px;
            font-weight: bold;
        }
        QPushButton:hover {
            background-color: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #9a4dff, stop:1 #5a1aff);
        }
        QPushButton:pressed {
            background-color: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #8e2de2, stop:1 #4a00e0);
        }
        QComboBox {
            background-color: #2a2a2a;
            border: 1px solid #3a3a3a;
            border-radius: 8px;
            padding: 8px;
            font-size: 14px;
        }
        QComboBox::drop-down {
            border: none;
        }
        QLabel {
            font-size: 14px;
        }
        QStatusBar {
            background-color: #2a2a2a;
            color: #e0e0e0;
        }
    """