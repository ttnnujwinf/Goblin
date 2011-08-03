import unittest
import logging
from psusys import PSUSys

class TestAll(unittest.TestCase):
	def setUp(self):
		self.psusys = PSUSys()
		logging.config.fileConfig('/vol/goblin/etc/logging.conf')
		log = logging.getLogger('goblin.psusys')
		self.psusys.setLogger(log)

	def test_opt_in_already(self):
		self.assertTrue(self.psusys.opt_in_already('dennis'))
		self.assertFalse(self.psusys.opt_in_already('buono'))
		
	def test_large_emails(self):
		emailen = self.psusys.large_emails('weekse')
		self.assertTrue(len(emailen) == 2)

	def test_routing(self):
		self.psusys.route_to_google('a2sj')
		self.assertTrue(self.psusys.opt_in_already('a2sj'))
		self.psusys.route_to_psu('a2sj')
		self.assertFalse(self.psusys.opt_in_already('a2sj'))

	def test_gmail_enable(self):
		if self.psusys.is_gmail_enabled('paul'):
			self.psusys.disable_gmail('paul')
			self.assertFalse(self.psusys.is_gmail_enabled('paul'))
		else:
			self.psusys.enable_gmail('paul')
			self.assertTrue(self.psusys.is_gmail_enabled('paul'))
			self.psusys.disable_gmail('paul')
			self.assertFalse(self.psusys.is_gmail_enabled('paul'))
			
	def test_google_account_status(self):
		self.assertEqual(
			self.psusys.google_account_status('dennis')
			,{"enabled": True, "exists": True}
		)
		self.assertEqual(
			self.psusys.google_account_status('pdx00800')
			,{"enabled": False, "exists": True}
		)
		self.assertEqual(
			self.psusys.google_account_status('pdx008')
			,{"enabled": False, "exists": False}
		)

	def test_enable_google_account(self):
		if self.psusys.google_account_status('paul') == {"enabled": True, "exists": True}:
			self.psusys.disable_google_account('paul')
			self.assertEqual(
				self.psusys.google_account_status('paul')
				,{"enabled": False, "exists": True}
			)
		else:
			self.psusys.enable_google_account('paul')
			self.assertEqual(
				self.psusys.google_account_status('paul')
				,{"enabled": True, "exists": True}
			)
			self.psusys.disable_google_account('paul')
			self.assertEqual(
				self.psusys.google_account_status('paul')
				,{"enabled": False, "exists": True}
			)

	def test_is_oamed(self):
		self.assertFalse(self.psusys.is_oamed('a2sj'))
		self.assertTrue(self.psusys.is_oamed('staplej'))
		self.assertFalse(self.psusys.is_oamed('askclas'))
		self.assertFalse(self.psusys.is_oamed('pdx00800'))
		self.assertTrue(self.psusys.is_oamed('dennis'))
		
	def test_is_allowed(self):
		self.assertTrue(self.psusys.is_allowed('dennis'))
		self.assertFalse(self.psusys.is_allowed('pdx00800'))
		
if __name__ == '__main__':
	unittest.main()		
