#!/usr/bin/env python3
"""Quiet static server for local preview.

Plain `python3 -m http.server` spams BrokenPipeError tracebacks when the
browser cancels video range-requests (normal during scroll/seek/loop).
This subclass silences those benign disconnects and supports range
requests so video seeking works smoothly.

Usage:  python3 serve.py [port]   # default 8000
"""
import sys
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer


class QuietHandler(SimpleHTTPRequestHandler):
    def handle_one_request(self):
        try:
            super().handle_one_request()
        except (BrokenPipeError, ConnectionResetError):
            self.close_connection = True

    def copyfile(self, source, outputfile):
        try:
            super().copyfile(source, outputfile)
        except (BrokenPipeError, ConnectionResetError):
            pass

    def log_message(self, fmt, *args):
        pass  # comment out this line if you want request logs


if __name__ == "__main__":
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8000
    handler = partial(QuietHandler, directory=".")
    print(f"Serving http://localhost:{port}  (Ctrl-C to stop)")
    try:
        ThreadingHTTPServer(("", port), handler).serve_forever()
    except KeyboardInterrupt:
        print("\nstopped")
