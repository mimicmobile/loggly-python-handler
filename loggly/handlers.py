import logging
import logging.handlers

import socket
import traceback

from requests_futures.sessions import FuturesSession

session = FuturesSession()


def bg_cb(sess, resp):
    """ Don't do anything with the response """
    pass


class HTTPSHandler(logging.Handler):
    def __init__(self, url, verify=True, level=logging.DEBUG, fqdn=False, localname=None, facility=None):
        logging.Handler.__init__(self, level=level)
        self.url = url
        self.verify = verify
        self.fqdn = fqdn
        self.localname = localname
        self.facility = facility

    def get_full_message(self, record):
        if record.exc_info:
            return '\n'.join(traceback.format_exception(*record.exc_info))
        else:
            return record.getMessage()

    def emit(self, record):
        try:
            payload = self.format(record)
            session.post(self.url, data=payload, verify=self.verify,
                         background_callback=bg_cb)
        except (KeyboardInterrupt, SystemExit):
            raise
        except:
            self.handleError(record)

