
import json
import errno
import logging

logger = logging.getLogger(__name__)

class CacheHandler():
    """
    An abstraction layer for handling the caching
    """

    def get_cached_timeout(self):
        """ get cache timeout """
        raise NotImplementedError()

    def save_response_to_cache(self, response):
        """
        Save a response of request dictionary object to the cache and return None.
        """
        raise NotImplementedError()
        return None


class CacheFileHandler(CacheHandler):
    """
    Handles reading and writing cached Spotify authorization tokens
    as json files on disk.
    """

    def __init__(self, cache_path=None, username=None):
        if cache_path:
            self.cache_path = cache_path
        else:
            cache_path = ".cache_response"
            if username is None: username='anonymous'
            username = username 
            if username: cache_path += "-" + str(username)
            self.cache_path = cache_path

    def get_cached_timeout(self):
        timeout_info = None
        try:
            f = open(self.cache_path)
            timeout_info_string = f.read()
            f.close()
            timeout_info = json.loads(timeout_info_string)

        except IOError as error:
            if error.errno == errno.ENOENT:
                logger.debug("cache does not exist at: %s", self.cache_path)
            else:
                logger.warning("Couldn't read cache at: %s", self.cache_path)

        return timeout_info

    def save_response_to_cache(self, response):
        try:
            f = open(self.cache_path, "w")
            f.write(json.dumps(response))
            f.close()
        except IOError:
            logger.warning(
                'Couldn\'t write response to cache at: %s',
                self.cache_path
            )