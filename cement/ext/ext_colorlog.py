"""
Cement colorlog extension module.
"""

import os
import sys
import logging
from colorlog import ColoredFormatter
from ..ext.ext_logging import LoggingLogHandler
from ..utils.misc import is_true


class ColorLogHandler(LoggingLogHandler):

    """
    This class implements the Log Handler interface.  It is
    a sub-class of :class:`cement.ext.ext_logging.LoggingLogHandler` which is
    based on the standard :py:class:`logging` library, and adds colorized
    console output using the
    `ColorLog <https://pypi.python.org/pypi/colorlog>`_ library.

    **Note** This extension has an external dependency on ``colorlog``.  You
    must include ``colorlog`` in your applications dependencies as Cement
    explicitly does **not** include external dependencies for optional
    extensions.

    """
    class Meta:

        """Handler meta-data."""

        #: The string identifier of the handler.
        label = "colorlog"

        #: The config_section identifiying the config key.
        config_section = 'log.colorlog'

        #: Color mapping for each log level
        colors = {
            'DEBUG':    'cyan',
            'INFO':     'green',
            'WARNING':  'yellow',
            'ERROR':    'red',
            'CRITICAL': 'red,bg_white',
        }

        #: Default configuration settings.  Will be overridden by the same
        #: settings in any application configuration file under a
        #: ``[log.colorlog]`` block.
        config_defaults = dict(
            file=None,
            level='INFO',
            to_console=True,
            rotate=False,
            max_bytes=512000,
            max_files=4,
            colorize_file_log=False,
            colorize_console_log=True,
        )

        #: Formatter class to use for non-colorized logging (non-tty, file,
        #: etc)
        formatter_class_without_color = logging.Formatter

        #: Formatter class to use for colorized logging
        formatter_class = ColoredFormatter

    def _get_console_format(self):
        format = super(ColorLogHandler, self)._get_console_format()
        colorize = self.app.config.get(self.Meta.config_section,
                                       'colorize_console_log')
        if sys.stdout.isatty() or 'CEMENT_TEST' in os.environ:
            if is_true(colorize):
                format = "%(log_color)s" + format
        return format

    def _get_file_format(self):
        format = super(ColorLogHandler, self)._get_file_format()
        colorize = self.app.config.get(self.Meta.config_section,
                                       'colorize_file_log')
        if is_true(colorize):
            format = "%(log_color)s" + format
        return format

    def _get_console_formatter(self, format):
        colorize = self.app.config.get(self.Meta.config_section,
                                       'colorize_console_log')
        if sys.stdout.isatty() or 'CEMENT_TEST' in os.environ:
            if is_true(colorize):
                formatter = self._meta.formatter_class(
                    format,
                    log_colors=self._meta.colors
                )
            else:
                formatter = self._meta.formatter_class_without_color(
                    format
                )
        else:
            klass = self._meta.formatter_class_without_color  # pragma: nocover
            formatter = klass(format)                        # pragma: nocover

        return formatter

    def _get_file_formatter(self, format):
        colorize = self.app.config.get(self.Meta.config_section,
                                       'colorize_file_log')
        if is_true(colorize):
            formatter = self._meta.formatter_class(
                format,
                log_colors=self._meta.colors
            )
        else:
            formatter = self._meta.formatter_class_without_color(format)

        return formatter


def load(app):
    app.handler.register(ColorLogHandler)
