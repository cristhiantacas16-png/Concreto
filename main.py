"""ConcretoLab Professional Suite - punto de entrada.

Ejecutar:  python main.py
"""
from __future__ import annotations

import logging
import sys

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication, QMessageBox

from app.core import config
from app.core.logging_setup import setup_logging


def main() -> int:
    config.ensure_directories()
    setup_logging()
    log = logging.getLogger("concretolab")
    log.info("Iniciando %s v%s", config.APP_FULL_NAME, config.APP_VERSION)

    QApplication.setHighDpiScaleFactorRoundingPolicy(Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)
    app = QApplication(sys.argv)
    app.setApplicationName(config.APP_NAME)
    app.setOrganizationName(config.ORGANIZATION)

    try:
        from app.database.session import init_db
        from app.services import project_service as ps
        from app.core.state import AppState
        from app.ui.theme import body_font, build_qss_full
        from app.ui.main_window import MainWindow

        init_db()
        ps.ensure_defaults()
        app.setFont(body_font(13))
        app.setStyleSheet(build_qss_full())
        window = MainWindow(AppState())
        window.show()
    except Exception as exc:  # noqa: BLE001 - se informa al usuario y se registra
        log.exception("Error fatal al iniciar")
        QMessageBox.critical(None, "ConcretoLab", f"No se pudo iniciar la aplicación:\n{exc}")
        return 1
    return app.exec()


if __name__ == "__main__":
    sys.exit(main())
