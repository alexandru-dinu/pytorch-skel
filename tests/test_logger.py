import io
import os
import random
import logging
import string
import unittest
import uuid
from threading import Thread

from bagoftools.logger import Logger, LOG_LEVELS


class TestLogger(unittest.TestCase):
    def setUp(self) -> None:
        self.logger = Logger(name='testing', colorize=True)

        # Remove handler that outputs to STDERR.
        self.logger.inner_logger.removeHandler(self.logger.inner_stream_handler)
        self.log_capture = io.StringIO()
        handler = logging.StreamHandler(self.log_capture)
        handler.setFormatter(self.logger.inner_formatter)
        self.logger.inner_logger.addHandler(handler)
        self.logger.setLevel(logging.DEBUG)

    def tearDown(self):
        pass

    def last_line(self):
        log = self.log_capture.getvalue().splitlines()
        if len(log) == 0:
            return []
        return log[-1]

    def last_n_lines(self, n):
        log = self.log_capture.getvalue().splitlines()
        return log[-n:]

    def num_lines(self):
        return len(self.log_capture.getvalue().splitlines())

    def one_shot(self, _logger):
        _logger.debug('D')
        self.assertIn("DEBUG", self.last_line())
        _logger.info('I')
        self.assertIn("INFO", self.last_line())
        _logger.warning('W')
        self.assertIn("WARNING", self.last_line())
        _logger.error('E')
        self.assertIn("ERROR", self.last_line())
        _logger.critical('C')
        self.assertIn("CRITICAL", self.last_line())

    def test_properties(self):
        self.assertEqual(self.logger.name, 'testing')

    def test_level_change(self):
        il = self.logger.inner_logger
        self.assertEqual(il.level, logging.DEBUG)

        levels = ['debug',    'DEBUG',    logging.DEBUG,
                  'info',     'INFO',     logging.INFO,
                  'warning',  'WARNING',  logging.WARNING,
                  'error',    'ERROR',    logging.ERROR,
                  'critical', 'CRITICAL', logging.CRITICAL]
        random.shuffle(levels)

        for l in levels:
            self.logger.setLevel(l)
            if isinstance(l, int):
                self.assertEqual(il.level, l)
            else:
                self.assertEqual(il.level, LOG_LEVELS[l.lower()])

        il.setLevel(logging.DEBUG)

    def test_logging_to_file(self):
        tmp = f'/tmp/{uuid.uuid4().hex}.txt'

        with open(tmp, 'wt') as fh:
            file_logger = Logger(name='file-logger', stream=fh)
            file_logger.debug('logging')
            file_logger.info('to')
            file_logger.warning('a')
            file_logger.error('txt')
            file_logger.critical('file')

        with open(tmp, 'rt') as fh:
            content = '\n'.join([x.strip() for x in fh.readlines()])
            for k in ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']:
                self.assertIn(k, content)

        os.remove(tmp)
        self.assertFalse(os.path.exists(tmp))

    def test_multiple_handlers(self):
        tmp = f'/tmp/{uuid.uuid4().hex}.txt'

        fh = open(tmp, 'wt')

        self.logger.add_handler(fh)
        self.assertEqual(len(self.logger.get_handlers()), 2)

        # test that output goes to both streams
        self.one_shot(self.logger)

        rc = self.logger.remove_handler(fh)
        self.assertTrue(rc)

        # remove once again
        rc = self.logger.remove_handler(fh)
        self.assertFalse(rc)

        self.assertEqual(len(self.logger.get_handlers()), 1)
        fh.close()

        # test that removing a non-existent handler does nothing
        fh2 = open('/dev/null', 'wt')
        rc = self.logger.remove_handler(fh2)
        self.assertFalse(rc)
        self.assertEqual(len(self.logger.get_handlers()), 1)
        fh2.close()

        with open(tmp, 'rt') as fh:
            content = '\n'.join([x.strip() for x in fh.readlines()])
            for k in ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']:
                self.assertIn(k, content)

        os.remove(tmp)
        self.assertFalse(os.path.exists(tmp))

        # test that output to main stream is still ok
        self.one_shot(self.logger)

        # test that clearing handlers work
        self.logger.clear_handlers()
        self.assertEqual(len(self.logger.get_handlers()), 0)
        self.logger.debug('nothing')
        self.assertNotIn('nothing', self.last_line())

    def test_level_is_logged(self):
        self.logger.debug("message 1")
        self.assertIn("DEBUG", self.last_line())
        self.logger.info("message 2")
        self.assertIn("INFO", self.last_line())
        self.logger.warning("message 3")
        self.assertIn("WARNING", self.last_line())
        self.logger.error("message 4")
        self.assertIn("ERROR", self.last_line())
        self.logger.critical("message 5")
        self.assertIn("CRITICAL", self.last_line())

    def test_function_is_logged(self):
        self.logger.debug("message 1")
        self.assertIn(" test_function_is_logged", self.last_line())
        self.logger.info("message 2")
        self.assertIn(" test_function_is_logged", self.last_line())
        self.logger.warning("message 3")
        self.assertIn(" test_function_is_logged", self.last_line())
        self.logger.error("message 4")
        self.assertIn(" test_function_is_logged", self.last_line())
        self.logger.critical("message 5")
        self.assertIn(" test_function_is_logged", self.last_line())

    def test_message_is_logged(self):
        self.logger.debug("message 1")
        self.assertIn("message 1", self.last_line())
        self.logger.info("message 2")
        self.assertIn("message 2", self.last_line())
        self.logger.warning("message 3")
        self.assertIn("message 3", self.last_line())
        self.logger.error("message 4")
        self.assertIn("message 4", self.last_line())
        self.logger.critical("message 5")
        self.assertIn("message 5", self.last_line())

    def test_levels(self):
        def log_all():
            self.logger.debug("message 1")
            self.logger.info("message 2")
            self.logger.warning("message 3")
            self.logger.error("message 4")
            self.logger.critical("message 5")

        def test_last(expected):
            self.assertIsInstance(expected, list)
            last_n = self.last_n_lines(len(expected))
            self.assertEqual(len(last_n), len(expected))
            for output, exp in zip(last_n, expected):
                self.assertIn(exp, output)

        expected_logs = [
            "DEBUG: message 1",
            "INFO: message 2",
            "WARNING: message 3",
            "ERROR: message 4",
            "CRITICAL: message 5"
        ]

        # Debug.
        self.logger.setLevel(logging.DEBUG)
        log_all()
        self.assertEqual(self.num_lines(), 5)
        test_last(expected_logs)

        # Info.
        self.logger.setLevel(logging.INFO)
        log_all()
        self.assertEqual(self.num_lines(), 5 + 4)
        test_last(expected_logs[1:])

        # Warning.
        self.logger.setLevel(logging.WARNING)
        log_all()
        self.assertEqual(self.num_lines(), 5 + 4 + 3)
        test_last(expected_logs[2:])

        # Error.
        self.logger.setLevel(logging.ERROR)
        log_all()
        self.assertEqual(self.num_lines(), 5 + 4 + 3 + 2)
        test_last(expected_logs[3:])

        # Critical.
        self.logger.setLevel(logging.CRITICAL)
        log_all()
        self.assertEqual(self.num_lines(), 5 + 4 + 3 + 2 + 1)
        test_last(expected_logs[4:])

    def test_multithreading(self):
        num_threads = 75

        def log_all(msg):
            for _ in range(11):
                self.logger.debug(msg)
                self.logger.info(msg)
                self.logger.warning(msg)
                self.logger.error(msg)
                self.logger.critical(msg)

        # Generate a random long message for each thread.
        messages = []
        for _ in range(0, num_threads):
            msg = []
            length = random.randint(500, 2000)
            alphabet = string.punctuation + string.ascii_letters + string.digits  # noqa: E501
            for _ in range(length):
                msg.append(random.choice(list(alphabet)))
            messages.append(''.join(msg))
            self.assertNotIn('\n', messages[-1])
        self.assertEqual(len(messages), num_threads)

        # Create, start and stop threads.
        threads = [Thread(target=log_all, args=(messages[i],)) for i in range(num_threads)]
        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join()

        # Check the output.
        self.assertEqual(self.num_lines(), num_threads * 11 * 5)
        log = self.log_capture.getvalue().splitlines()
        for line in log:
            self.assertEqual(line[0], '[')
            self.assertGreater(len(line), 500)

        # Counts in how many elements of @array, @substr can be found.
        def count_in(array, substr):
            return sum((substr in el for el in array))

        for msg in messages:
            self.assertEqual(count_in(log, msg), 11 * 5)
            for level in ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]:
                self.assertEqual(count_in(log, level + ": " + msg), 11)

    def test_terminal_logging(self):
        self.logger.info("message to terminal device")
        self.assertIn("INFO", self.last_line())
        # 80 (the length without colors) + 2 coloring characters.
        self.assertGreaterEqual(len(self.last_line()), 80 + 2)

        self.logger.warning("message to terminal device")
        self.assertIn("WARNING", self.last_line())
        # 83 (the length without colors) + 4 coloring characters.
        self.assertGreaterEqual(len(self.last_line()), 83 + 4)

    def test_non_str_logging(self):
        self.logger.info(10)
        self.assertIn("10", self.last_line())

        # Those should not throw any error.
        self.logger.debug([10, 20, 30])
        self.logger.critical({})
        self.logger.warning({-1, 4})

    def test_function_wrapping(self):

        @self.logger.log_function()
        def _test(a, b, x, delta):
            return a * b + x / delta

        a, b, x, delta = [random.uniform(-1, 1) for _ in range(4)]
        _test(a, b, x=x, delta=delta)
        out = self.last_n_lines(3)
        self.assertTrue(any([f'args: ({a}, {b})' in o for o in out]))
        self.assertTrue(any(['kwargs: {}'.format(str({'x': x, 'delta': delta})) in o for o in out]))


if __name__ == '__main__':
    unittest.main()
