import logging
import os
import unittest

import requests
from semantic_version import Version

from src import cw_typist_version
from test.base_test_setup import BaseTestSetup


class VersionTest(BaseTestSetup):
	def test_version_present(self):
		self.assertIsNotNone(cw_typist_version.version)

	def test_version_ci(self):
		if 'CI' not in os.environ.keys():
			return
		self.assertNotEqual(cw_typist_version.version, 'DEVELOPMENT')
		logging.critical(f"Version found: {cw_typist_version.version}")

	def test_version_incremented(self):
		ref = 'DEV'
		headers = {}
		if 'GITHUB_REF' in os.environ.keys():
			ref = os.environ['GITHUB_REF']
		if 'GITHUB_TOKEN' in os.environ.keys():
			headers['Authorization'] = f"Bearer {os.environ['GITHUB_TOKEN']}"
		else:
			logging.critical('GITHUB_TOKEN not set')

		logging.critical(f"Current ref is `{ref}`")
		is_master = ref == 'refs/heads/master'
		if is_master:
			logging.critical("Skipping version increment check on master.")
		endpoint = "https://api.github.com/repos/n2qzshce/cw_typist/tags"
		result = requests.get(endpoint, headers=headers)
		result_json = result.json()
		if len(result_json) == 0:
			return
		latest_version = result_json[0]['name']
		latest = Version.coerce(latest_version)
		current = Version.coerce(cw_typist_version.version)
		self.assertGreater(current, latest, "Version has not been incremented.")
