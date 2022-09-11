source .env
/odoo15/.odoo-env/bin/python /odoo15/odoo/odoo-bin \
	--stop-after-init \
	--test-tags /overtime_approval \
	--database $DB_NAME \
	--http-port $ODOO_PORT \
	--addons-path=$ADDONS_PATH \
	--log-level error