#!/usr/bin/env python3
# Usage:
#   ./run_tests.py -h http://example.com/ tests/**/*.py
#   SELENIUM_BROWSER=Firefox SELENIUM_HOST=http://example.com python3 run_tests.py tests/**/*.py

import sys
import unittest
import argparse
import inspect
import logging

if __name__ == '__main__':
    # Parse arguments.
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument("-?", "--help",     action="help",                        help="show this help message and exit" )
    parser.add_argument("-v", "--verbose",  action="store_true", dest="verbose",  help="increase output verbosity" )
    parser.add_argument("-d", "--debug",    action="store_true", dest="debug",    help="show debug messages" )
    parser.add_argument("-h", "--host",     action="store",      dest="host",     help="Destination host" )
    parser.add_argument("-b", "--browser",  action="store",      dest="browser",  help="Browser driver.", choices=["Firefox", "Chrome", "IE", "Opera", "PhantomJS"] )
    parser.add_argument("-r", "--reports-dir", action="store",   dest="dir",      help="Directory to save screenshots.", default="reports")
    #parser.add_argument("-u", "--user",     action="store",      dest="user",     help="Username for basic authentication." )
    #parser.add_argument("-p", "--password", action="store",      dest="password", help="Password for basic authentication." )
    parser.add_argument('files', nargs='*')
    args = parser.parse_args()

    # Load files from the arguments.
    for filename in args.files:
        exec(open(filename).read())

    def make_suite(tc_class):
        testloader = unittest.TestLoader()
        testnames = testloader.getTestCaseNames(tc_class)
        suite = unittest.TestSuite()
        for name in testnames:
            suite.addTest(tc_class(name, cargs=args))
        return suite

    # Add all tests.
    alltests = unittest.TestSuite()
    for name, obj in inspect.getmembers(sys.modules[__name__]):
        if inspect.isclass(obj) and name.startswith("AdsTest"):
            alltests.addTest(make_suite(obj))

    # Set-up logger
    verbose = bool(os.environ.get('VERBOSE', args.verbose))
    debug   = bool(os.environ.get('DEBUG', args.debug))
    if verbose or debug:
        logging.basicConfig( stream=sys.stdout )
        root = logging.getLogger()
        root.setLevel(logging.INFO if verbose else logging.DEBUG)
        ch = logging.StreamHandler(sys.stdout)
        ch.setLevel(logging.INFO if verbose else logging.DEBUG)
        ch.setFormatter(logging.Formatter('%(asctime)s %(levelname)s: %(name)s: %(message)s'))
        root.addHandler(ch)
    else:
        logging.basicConfig(stream=sys.stderr)

    # Run tests.
    result = unittest.TextTestRunner(verbosity=2).run(alltests)
    sys.exit(not result.wasSuccessful())
