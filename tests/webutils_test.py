"""Unit test for webutils.
"""

import unittest

import flask

from treadmill import webutils


class WebUtilsTest(unittest.TestCase):
    """Tests for teadmill.webutils."""

    def test_cors(self):
        """Tests cors decorator."""
        app = flask.Flask(__name__)
        app.testing = True

        @app.route('/xxx')
        @webutils.cors(origin='*', content_type='application/json')
        def handler_unused():
            """Name does not matter, flask will route the request."""
            return flask.jsonify({'apps': 1})

        resp = app.test_client().get('/xxx')
        self.assertEqual(resp.mimetype, 'application/json')
        self.assertEqual({'apps': 1}, flask.json.loads(resp.data))

        self.assertIn('Access-Control-Allow-Origin', resp.headers)
        self.assertEqual('*', resp.headers['Access-Control-Allow-Origin'])

    def test_wants_json_resp(self):
        """Tests the accept header evaluation."""
        app = flask.Flask(__name__)
        app.testing = True

        with app.test_request_context(headers=[('Accept', 'application/json, '
                                                          'text/plain')]):
            self.assertTrue(webutils.wants_json_resp(flask.request))

        with app.test_request_context(headers=[('Accept', 'text/html; q=1.0, '
                                                'text/*; q=0.8, image/gif; '
                                                'q=0.6, image/jpeg;')]):
            self.assertFalse(webutils.wants_json_resp(flask.request))


if __name__ == '__main__':
    unittest.main()
