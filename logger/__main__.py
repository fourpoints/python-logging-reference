import logging
import argparse
from .foo import logger as foo_logger
from . import logger as init_logger

parser = argparse.ArgumentParser()

# https://stackoverflow.com/questions/14097061/easier-way-to-enable-verbose-logging
parser.add_argument(
    '-d', '--debug',
    help="Print lots of debugging statements",
    action="store_const", dest="loglevel", const=logging.DEBUG,
    default=logging.WARNING,
)
parser.add_argument(
    "-v", "--verbose",
    help="Be verbose",
    action="store_const", dest="loglevel", const=logging.INFO,
)

args = parser.parse_args()


if __name__ == "__main__":
    logger = logging.getLogger(__name__)

    # Logging hierarchy:
    # root
    # +-- __main__
    # +-- __init__
    #   +-- foo

    # basicConfig configures root logger
    # and initializes a StreamHandler (if none are specified)
    # default loglevel with no key word input is WARNING
    logging.basicConfig(level=args.loglevel)

    logger.info("main")  # displayed with --debug or --verbose
    foo_logger.debug("foo")  # displayed with --debug

    # logger.foo.logger is a child of logger.logger
    # and so will be affected by this setting
    # __main__ is only a child of the root, and
    # will not be affected
    init_logger.setLevel(logging.WARNING)

    logger.info("main")  # displayed with --debug or --verbose
    foo_logger.debug("foo")  # never displayed
    init_logger.warning("init")  # always displayed
    logging.root.debug("root")  # displayed with --debug

    # logger.foo.logger can override its parent by setting a level
    foo_logger.setLevel(logging.DEBUG)
    init_logger.setLevel(logging.INFO)
    foo_logger.debug("foo")  # always displayed

    # logger.foo.logger will revert to its parent level if unset again
    foo_logger.setLevel(logging.NOTSET)
    foo_logger.debug("foo")  # never displayed
    foo_logger.info("bar")  # always displayed
