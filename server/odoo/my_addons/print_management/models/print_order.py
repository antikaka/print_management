
from odoo import fields, models, api

class PrintOrder(models.Model):
    _name = "print.order"
    _description = "Print order model"

    name = fields.Char(string="Order ID", default="Will be assigned once created")
    customer = fields.Many2one("res.partner", string="Customer")
    order_manager = fields.Many2one("res.users", string="Order Manager")
    order_received = fields.Date(string="Order Received", default=fields.Date.today())
    order_due = fields.Date(string="Order Due", default=(fields.Date.add(fields.Date.today(), days=3)))
    order_warning = fields.Boolean(compute="_compute_late_or_warning", default=False, store=True)
    order_late = fields.Boolean(default=False, store=True)
    notes = fields.Text(string="Notes")
    product = fields.Many2one("print.product", string="Product")
    order_status = fields.Selection(selection=[
        ("1", "Unconfirmed"),
        ("2", "In Production"),
        ("3", "Packaging"),
        ("4", "Finished")
    ],
        default="1", store=True)

    operator_status = fields.Text(compute="_compute_operator_status", store=True, precompute=True)

    op_1_allowed = fields.Many2many("print.machine", compute="_compute_available_machines", store=True, relation="print_order_op_1_allowed_rel")
    op_1 = fields.Many2one("print.machine", domain="[('id', 'in', op_1_allowed)]")
    op_1_use = fields.Boolean(default=True)
    op_2_allowed = fields.Many2many("print.machine", relation="print_order_op_2_allowed_rel")
    op_2 = fields.Many2one("print.machine", domain="[('id', 'in', op_2_allowed)]")
    op_2_use = fields.Boolean(default=True)
    op_3_allowed = fields.Many2many("print.machine", relation="print_order_op_3_allowed_rel")
    op_3 = fields.Many2one("print.machine", domain="[('id', 'in', op_3_allowed)]")
    op_3_use = fields.Boolean(default=True)
    op_4_allowed = fields.Many2many("print.machine", relation="print_order_op_4_allowed_rel")
    op_4 = fields.Many2one("print.machine", domain="[('id', 'in', op_4_allowed)]")
    op_4_use = fields.Boolean(default=True)
    op_5_allowed = fields.Many2many("print.machine", relation="print_order_op_5_allowed_rel")
    op_5 = fields.Many2one("print.machine", domain="[('id', 'in', op_5_allowed)]")
    op_5_use = fields.Boolean(default=True)
    op_6_allowed = fields.Many2many("print.machine", relation="print_order_op_6_allowed_rel")
    op_6 = fields.Many2one("print.machine", domain="[('id', 'in', op_6_allowed)]")
    op_6_use = fields.Boolean(default=True)
    op_7_allowed = fields.Many2many("print.machine", relation="print_order_op_7_allowed_rel")
    op_7 = fields.Many2one("print.machine", domain="[('id', 'in', op_7_allowed)]")
    op_7_use = fields.Boolean(default=True)
    op_8_allowed = fields.Many2many("print.machine", relation="print_order_op_8_allowed_rel")
    op_8 = fields.Many2one("print.machine", domain="[('id', 'in', op_8_allowed)]")
    op_8_use = fields.Boolean(default=True)
    op_9_allowed = fields.Many2many("print.machine", relation="print_order_op_9_allowed_rel")
    op_9 = fields.Many2one("print.machine", domain="[('id', 'in', op_9_allowed)]")
    op_9_use = fields.Boolean(default=True)
    op_10_allowed = fields.Many2many("print.machine", relation="print_order_op_10_allowed_rel")
    op_10 = fields.Many2one("print.machine", domain="[('id', 'in', op_10_allowed)]")
    op_10_use = fields.Boolean(default=True)

    op_1_label = fields.Char(compute="_compute_label", store=True)
    op_2_label = fields.Char()
    op_3_label = fields.Char()
    op_4_label = fields.Char()
    op_5_label = fields.Char()
    op_6_label = fields.Char()
    op_7_label = fields.Char()
    op_8_label = fields.Char()
    op_9_label = fields.Char()
    op_10_label = fields.Char()

    @api.depends("order_due")
    def _compute_late_or_warning(self):  #check if the order is near due or late
        for record in self:
            record.order_warning = False
            record.order_late = False
            if record.order_due == (fields.Date.add(fields.Date.today(), days=1)):
                record.order_warning = True
            elif record.order_due <= fields.Date.today():
                record.order_late = True

    # @api.depends("product", "product.product_step", "product.product_step.machine_option_id", "product.product_step.machine_option_id.option", "product.product_step.sequence")
    @api.onchange("product")
    def _compute_number_ops(self):    #check how many steps a product has and thus create lines
        for record in self:
            record.op_1_use = True
            record.op_2_use = True
            record.op_3_use = True
            record.op_4_use = True
            record.op_5_use = True
            record.op_6_use = True
            record.op_7_use = True
            record.op_8_use = True
            record.op_9_use = True
            record.op_10_use = True
            for step in record.product.product_step:

                if step.sequence == 1:
                    record.op_1_use = False
                    record.op_1_label = step.step_name
                if step.sequence == 2:
                    record.op_2_use = False
                    record.op_2_label = step.step_name
                if step.sequence == 3:
                    record.op_3_use = False
                    record.op_3_label = step.step_name
                if step.sequence == 4:
                    record.op_4_use = False
                    record.op_4_label = step.step_name
                if step.sequence == 5:
                    record.op_5_use = False
                    record.op_5_label = step.step_name
                if step.sequence == 6:
                    record.op_6_use = False
                    record.op_6_label = step.step_name
                if step.sequence == 7:
                    record.op_7_use = False
                    record.op_7_label = step.step_name
                if step.sequence == 8:
                    record.op_8_use = False
                    record.op_8_label = step.step_name
                if step.sequence == 9:
                    record.op_9_use = False
                    record.op_9_label = step.step_name
                if step.sequence == 10:
                    record.op_10_use = False
                    record.op_10_label = step.step_name

    @api.depends("product", "product.product_step", "product.product_step.machine_option_id", "product.product_step.machine_option_id.option", "product.product_step.sequence")
    def _compute_label(self):         #label the product step lines in the order
        for record in self:
            for step in record.product.product_step:
                if record.op_1_use == False and step.sequence == 1:
                    record.op_1_label = step.step_name
                if record.op_2_use == False and step.sequence == 2:
                    record.op_2_label = step.step_name
                if record.op_3_use == False and step.sequence == 3:
                    record.op_3_label = step.step_name
                if record.op_4_use == False and step.sequence == 4:
                    record.op_4_label = step.step_name
                if record.op_5_use == False and step.sequence == 5:
                    record.op_5_label = step.step_name
                if record.op_6_use == False and step.sequence == 6:
                    record.op_6_label = step.step_name
                if record.op_7_use == False and step.sequence == 7:
                    record.op_7_label = step.step_name
                if record.op_8_use == False and step.sequence == 8:
                    record.op_8_label = step.step_name
                if record.op_9_use == False and step.sequence == 9:
                    record.op_9_label = step.step_name
                if record.op_10_use == False and step.sequence == 10:
                    record.op_10_label = step.step_name

    @api.depends("product", "product.product_step", "product.product_step.machine_option_id", "product.product_step.machine_option_id.option", "product.product_step.sequence")
    # @api.onchange("product")
    def _compute_available_machines(self): #check which machines have the option to complete the product step
        for record in self:
            allowed_machines = self.env['print.machine']              #initialize empty recordset
            if record.op_1_use == False:
                for step in record.product.product_step:
                    if step.sequence == 1:
                        allowed_machines |= step.machine_option_id.option #merge recordsets

            record.op_1_allowed = allowed_machines.ids

            allowed_machines = self.env["print.machine"]
            if record.op_2_use == False:
                for step in record.product.product_step:
                    if step.sequence == 2:
                        allowed_machines |= step.machine_option_id.option

            record.op_2_allowed = allowed_machines.ids

            allowed_machines = self.env["print.machine"]
            if record.op_3_use == False:
                for step in record.product.product_step:
                    if step.sequence == 3:
                        allowed_machines |= step.machine_option_id.option

            record.op_3_allowed = allowed_machines.ids

            allowed_machines = self.env["print.machine"]
            if record.op_4_use == False:
                for step in record.product.product_step:
                    if step.sequence == 4:
                        allowed_machines |= step.machine_option_id.option

            record.op_4_allowed = allowed_machines.ids

            allowed_machines = self.env["print.machine"]
            if record.op_5_use == False:
                for step in record.product.product_step:
                    if step.sequence == 5:
                        allowed_machines |= step.machine_option_id.option

            record.op_5_allowed = allowed_machines.ids

            allowed_machines = self.env["print.machine"]
            if record.op_6_use == False:
                for step in record.product.product_step:
                    if step.sequence == 6:
                        allowed_machines |= step.machine_option_id.option

            record.op_6_allowed = allowed_machines.ids

            allowed_machines = self.env["print.machine"]
            if record.op_7_use == False:
                for step in record.product.product_step:
                    if step.sequence == 7:
                        allowed_machines |= step.machine_option_id.option

            record.op_7_allowed = allowed_machines.ids

            allowed_machines = self.env["print.machine"]
            if record.op_8_use == False:
                for step in record.product.product_step:
                    if step.sequence == 8:
                        allowed_machines |= step.machine_option_id.option

            record.op_8_allowed = allowed_machines.ids

            allowed_machines = self.env["print.machine"]
            if record.op_9_use == False:
                for step in record.product.product_step:
                    if step.sequence == 9:
                        allowed_machines |= step.machine_option_id.option

            record.op_9_allowed = allowed_machines.ids

            allowed_machines = self.env["print.machine"]
            if record.op_10_use == False:
                for step in record.product.product_step:
                    if step.sequence == 10:
                        allowed_machines |= step.machine_option_id.option

            record.op_10_allowed = allowed_machines.ids

    def _compute_order_id(self):  #create order id
        for order in self:
            date = str(fields.Date.today())
            order.name = date[2:4] + date[5:7] + date[8:10] + str(order.id)

    @api.depends("order_status")
    def _compute_operator_status(self):  #check the production status of order and represent it in order
        for record in self:
            if int(record.order_status) == 2:
                op_record = self.env["print.operator"].search([("name", "ilike", record.name)])
                if op_record.step_max == False:
                    op_record._compute_curr_step()
                record.operator_status = f" Step nr. {op_record.current_step_num} out of {op_record.step_max}.\n{op_record.current_step}\n{op_record.current_step_machine}"
            elif int(record.order_status) == 3:
                record.operator_status = f" Order not in production\nOrder in packaging"
            elif int(record.order_status) == 4:
                record.operator_status = f"Order supposedly finished"
            else:
                record.operator_status = "Order not in production"

    @api.model_create_single
    def create(self, vals):           #for order id creation
        record = super(PrintOrder, self).create(vals)
        record._compute_order_id()
        return record


    def action_status_back(self):  #for button go back
        num = int(self.order_status)
        num -= 1
        if num < 1:
            num = 1
        self.order_status = str(num)
        return True

    def action_status_forward(self): #for button go forward
        num = int(self.order_status)
        num += 1
        if num == 2:
            self.order_status = str(num)
            self.env["order.to.operator"].migrate_record(self.name) #migrates order from order to operator
        if num > 4:
            num = 4
        self.order_status = str(num)
        return True

