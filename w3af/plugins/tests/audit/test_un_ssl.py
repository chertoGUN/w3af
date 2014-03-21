"""
test_unssl.py

Copyright 2012 Andres Riancho

This file is part of w3af, http://w3af.org/ .

w3af is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation version 2 of the License.

w3af is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with w3af; if not, write to the Free Software
Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA
"""
from w3af.plugins.tests.helper import PluginTest, PluginConfig, MockResponse


class TestUnSSL(PluginTest):

    target_url = 'http://httpretty/'

    # This mocked response will be returned for both http and https
    MOCK_RESPONSES = [MockResponse('/', 'foo bar spam',)]

    _run_configs = {
        'cfg': {
            'target': target_url,
            'plugins': {
                'audit': (PluginConfig('un_ssl'),),
            }
        }
    }

    def setUp(self):
        super(TestUnSSL, self).setUp()
        self._register_httpretty_uri('https', 'httpretty', 443)

    def test_found_unssl(self):
        cfg = self._run_configs['cfg']
        self._scan(cfg['target'], cfg['plugins'])

        vulns = self.kb.get('un_ssl', 'un_ssl')
        self.assertEquals(1, len(vulns))

        # Now some tests around specific details of the found vuln
        vuln = vulns[0]
        self.assertEquals(vuln.get_name(), 'Secure content over insecure channel')
        self.assertEquals(vuln.get_url().url_string, 'http://httpretty/')