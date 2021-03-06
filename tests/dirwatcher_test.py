"""Unit test for directory watcher.
"""

import errno
import os
import shutil
import sys
import tempfile
import unittest

import mock

from treadmill import dirwatch

if os.name != 'nt':
    import select


class DirWatcherTest(unittest.TestCase):
    """Tests for teadmill.dirwatch."""

    def setUp(self):
        self.root = tempfile.mkdtemp()

    def tearDown(self):
        if self.root and os.path.isdir(self.root):
            shutil.rmtree(self.root)

    def test_watcher(self):
        """Tests created/deleted callbackes."""
        created = []
        modified = []
        deleted = []
        test_file = os.path.join(self.root, 'a')

        watcher = dirwatch.DirWatcher(self.root)
        watcher.on_created = lambda x: created.append(x) or 'one'
        watcher.on_modified = lambda x: modified.append(x) or 'two'
        watcher.on_deleted = lambda x: deleted.append(x) or 'three'

        with open(test_file, 'w') as f:
            f.write('hello')
        with open(test_file, 'a') as f:
            f.write(' world!')
        os.unlink(test_file)
        with open(test_file, 'w') as f:
            f.write('hello again')

        res = watcher.process_events(max_events=3)

        self.assertEqual([test_file], created)
        self.assertEqual([test_file], modified)
        self.assertEqual([test_file], deleted)
        self.assertEqual(
            [
                (dirwatch.DirWatcherEvent.CREATED, test_file, 'one'),
                (dirwatch.DirWatcherEvent.MODIFIED, test_file, 'two'),
                (dirwatch.DirWatcherEvent.DELETED, test_file, 'three'),
                (dirwatch.DirWatcherEvent.MORE_PENDING, None, None),
            ],
            res,
        )

    @unittest.skipUnless(sys.platform == 'linux2', 'Requires Linux')
    @mock.patch('select.poll', mock.Mock())
    def test_signal(self):
        """Tests behavior when signalled during wait."""
        watcher = dirwatch.DirWatcher(self.root)

        mocked_pollobj = select.poll.return_value
        mocked_pollobj.poll.side_effect = select.error(errno.EINTR, '')

        self.assertFalse(watcher.wait_for_events())


if __name__ == '__main__':
    unittest.main()
