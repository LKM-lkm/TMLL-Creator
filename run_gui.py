#!/usr/bin/env python3
"""
启动TTML歌词生成器GUI
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'ttml_generator'))

from ttml_generator.gui.main_window import MainWindow

if __name__ == "__main__":
    app = MainWindow()
    app.run()