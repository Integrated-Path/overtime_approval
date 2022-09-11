import datetime
from odoo.addons.overtime_approval.tests.common import TestOvertimeApprovalBase


class TestRegualrPlayslipGenerate(TestOvertimeApprovalBase):

	@classmethod
	def setUpClass(cls):
		super(TestRegualrPlayslipGenerate, cls).setUpClass()
		def create_approval_request(kwargs={}):
			values = {
				"name": cls.hours_overtime_category.name,
				"request_owner_id": cls.richard_user.id,
				"category_id": cls.hours_overtime_category.id,
				"date_start": datetime.datetime(2022, 5, 1, 0, 0, 0),
				"date_end": datetime.datetime(2022, 5, 1, 6, 0, 0),
			}
			values.update(kwargs)
			return cls.env["approval.request"].create(values)

		def create_approval_hours_requests():
			approved_request_1 = create_approval_request() # 6 hours
			approved_request_1.action_confirm()
			approved_request_1.with_user(cls.admin_user.id).action_approve()

			approved_request_2 = create_approval_request({ # 4 hours
				"date_start": datetime.datetime(2022, 5, 2, 22, 0, 0),
				"date_end": datetime.datetime(2022, 5, 3, 2, 0, 0),
			})
			approved_request_2.action_confirm()
			approved_request_2.with_user(cls.admin_user.id).action_approve()

			approved_request_3 = create_approval_request({ # 10 hours
				"date_start": datetime.datetime(2022, 5, 30, 13, 59, 59),
				"date_end": datetime.datetime(2022, 5, 30, 23, 59, 59),
			})
			approved_request_3.action_confirm()
			approved_request_3.with_user(cls.admin_user.id).action_approve()

			approved_request_4 = create_approval_request({ # 0.5 hours
				"date_start": datetime.datetime(2022, 5, 10, 10, 0, 0),
				"date_end": datetime.datetime(2022, 5, 10, 10, 30, 0),
			})
			approved_request_4.action_confirm()
			approved_request_4.with_user(cls.admin_user.id).action_approve()

			submited_request_1 = create_approval_request({ # 5 hours
				"date_start": datetime.datetime(2022, 5, 30, 10, 59, 59),
				"date_end": datetime.datetime(2022, 5, 30, 15, 59, 59),
			})
			submited_request_1.action_confirm()

			draft_request_1 = create_approval_request({ # 10 hours
				"date_start": datetime.datetime(2022, 5, 15, 10, 59, 59),
				"date_end": datetime.datetime(2022, 5, 15, 20, 59, 59),
			})
		create_approval_hours_requests()

		def create_approval_days_requests():
			approved_request_1 = create_approval_request({ # 16 hours
				"date_start": datetime.datetime(2022, 5, 1, 1, 0, 0),
				"date_end": datetime.datetime(2022, 5, 3, 1, 0, 0),
				"category_id": cls.days_overtime_category.id,
			})
			approved_request_1.action_confirm()
			approved_request_1.with_user(cls.admin_user.id).action_approve()

			approved_request_2 = create_approval_request({ # 40 hours
				"date_start": datetime.datetime(2022, 5, 15, 1, 0, 0),
				"date_end": datetime.datetime(2022, 5, 20, 1, 0, 0),
				"category_id": cls.days_overtime_category.id,
			})
			approved_request_2.action_confirm()
			approved_request_2.with_user(cls.admin_user.id).action_approve()

			draft_approved_request_3 = create_approval_request({ # 40 hours
				"date_start": datetime.datetime(2022, 5, 21, 1, 0, 0),
				"date_end": datetime.datetime(2022, 5, 24, 1, 0, 0),
				"category_id": cls.days_overtime_category.id,
			})
			draft_approved_request_3.action_confirm()
		create_approval_days_requests()


	def test_calculate_employe_overtime_hours_type_function(self):
		result = self.env["approval.request"].calculate_employe_overtime_hours_type(
			employee_id=self.richard_emp,
			start_date=datetime.datetime(2022, 5, 1, 0, 0, 0),
			end_date=datetime.datetime(2022, 5, 30, 23, 59, 59)
		)
		self.assertEqual(result, 20.5)

	def test_calculate_employe_overtime_days_type_function(self):
		result = self.env["approval.request"].calculate_employe_overtime_days_type(
			employee_id=self.richard_emp,
			start_date=datetime.datetime(2022, 5, 1, 0, 0, 0),
			end_date=datetime.datetime(2022, 5, 30, 23, 59, 59)
		)
		self.assertEqual(result, 56)