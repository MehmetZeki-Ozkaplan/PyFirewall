DARK_THEME =  """
QMainWindow {
    background-color: #1e1e2f;
    color: #dcdcdc;
}

QWidget {
    background-color: #1e1e2f;
    color: #dcdcdc;
    font-family: Consolas, 'Segoe UI';
    font-size: 10.5pt;
}

QPushButton {
    background-color: #2d2d40;
    color: #00ffaa;
    border: 1px solid #00ffaa;
    padding: 6px;
    border-radius: 4px;
}

QPushButton:hover {
    background-color: #3c3c50;
}

QPushButton:pressed {
    background-color: #44475a;
}

QLineEdit, QTextEdit, QTableWidget, QListWidget {
    background-color: #2b2b3c;
    color: #dcdcdc;
    border: 1px solid #00ffaa;
    border-radius: 3px;
}

QHeaderView::section {
    background-color: #2d2d40;
    color: #00ffaa;
    padding: 4px;
    border: 1px solid #00ffaa;
}

QLabel {
    color: #dcdcdc;
}

QTableWidget::item:selected,
QListWidget::item:selected {
    background-color: #00ffaa;
    color: #1e1e2f;
}
"""
