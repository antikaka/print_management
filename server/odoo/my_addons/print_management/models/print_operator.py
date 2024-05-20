from odoo import fields, models, api
from odoo.exceptions import UserError
from odoo import http


class OrdertoOperator(models.TransientModel):
    _name = "order.to.operator"

    def migrate_record(self, order_name):         #creates a copy of order in operator
        source = self.env["print.order"].search([("order_status", "=", "2")])
        for record in source:
            name = record.name
            if self.env["print.operator"].search_count(
                    ["&", "|", "&", ("name", "=", f"{name}"), ("active", "=", True), ("active", "=", False),
                     ("name", "=", f"{name}")]) > 0:
                print(self.env["print.operator"].search_count(
                    ["&", "|", "&", ("name", "=", f"{name}"), ("active", "=", True), ("active", "=", False),
                     ("name", "=", f"{name}")]), "double")
                continue
            else:
                steps = []
                step_machine = []
                op_machine = {}
                for x in range(10):
                    x = x + 1
                    op_machine[x] = getattr(record, f"op_{x}")
                for step in record.product.product_step:
                    steps.append((step.sequence, step.step_name))
                    step_machine.append((step.sequence, op_machine[step.sequence].name))
                fields = {
                    "name": record.name,
                    "op_customer": record.customer.complete_name,
                    "op_order_manager": record.order_manager.name,
                    "order_received": record.order_received,
                    "order_due": record.order_due,
                    "order_notes": record.notes,
                    "operator_product": record.product.name,
                    "op_product_steps": steps,
                    "op_product_machines": step_machine,
                    "op_product": record.product.id,
                }
                self.env["print.operator"].create(fields)
                print(fields)


class PrintOperator(models.Model):
    _name = "print.operator"
    _description = "Print operator model"

    name = fields.Char(string="Order ID", readonly=True)
    op_customer = fields.Char(string="Customer", readonly=True)
    op_order_manager = fields.Char(string="Order Manager", readonly=True)
    order_received = fields.Date(string="Order Received", readonly=True)
    order_due = fields.Date(string="Order Due", readonly=True)
    order_notes = fields.Text(string="Order notes", readonly=True)
    operator_product = fields.Char(string="Product", readonly=True)
    op_product_steps = fields.Char(readonly=True)
    op_product_machines = fields.Text(readonly=True)
    op_product = fields.Many2one("print.product")
    step_number_statusbar = fields.Selection(selection=[
        ("1", "1"),
        ("2", "2"),
        ("3", "3"),
        ("4", "4"),
        ("5", "5"),
        ("6", "6"),
        ("7", "7"),
        ("8", "8"),
        ("9", "9"),
        ("10", "10")

    ], default="1")
    operator_notes = fields.Text(string="Operator Notes")

    current_step_num = fields.Char(default="1", string="Current step")
    step_max = fields.Char(store=True)
    step_max_list = fields.Char(store=True)
    current_step = fields.Char(compute="_compute_curr_step", store=True)
    current_step_machine = fields.Char(store=True)
    current_instructions = fields.Text(compute="_compute_instructions")
    active = fields.Boolean(default=True, string="Active")

    @api.depends("op_product_steps", "op_product_machines", "operator_product")
    # @api.onchange("current_step_num")
    def _compute_curr_step(self):  #checking which step it is now and thus populating the machine and step names
        for record in self:
            steps = record.op_product_steps
            steps = steps[1:-2].split(",")
            step_names = []

            mach = record.op_product_machines
            mach = mach[1:-2].split(",")
            mach_name = []
            for num, step in enumerate(steps):
                if num % 2 == 0:
                    continue
                else:
                    step = step.replace("'", "")
                    step = step.replace(")", "")
                    step_names.append(step)

            for num, stepmach in enumerate(mach):
                if num % 2 == 0:
                    continue
                else:
                    stepmach = stepmach.replace("'", "")
                    stepmach = stepmach.replace(")", "")
                    mach_name.append(stepmach)

            record.current_step_machine = "N/A"
            record.current_step = "N/A"
            record.step_max = len(step_names)
            max_list = "1"

            order_record = self.env["print.order"].search([("name", "ilike", record.name)])
            order_record._compute_operator_status()
            for x in range(int(record.step_max)):
                if x > 0:
                    max_list += "," + str(x + 1)
            record.step_max_list = max_list
            for num, step in enumerate(step_names, 1):
                # print(len(step_names), step, record.current_step_num)
                if record.current_step_num == str(num):
                    # print("yes")
                    print(mach_name)
                    print(step_names)
                    record.current_step_machine = mach_name[num - 1]
                    record.current_step = step
                    order_record = self.env["print.order"].search([("name", "ilike", record.name)])
                    order_record._compute_operator_status()
                    record._compute_instructions()
                    break

    def _compute_instructions(self): #product step instructions
        step_name = self.current_step[1:]
        step_machine = self.current_step_machine[1:]
        instruction_record = self.env["print.machine.instruction"].search(
            [("option_id.name", "ilike", step_name), ("machine_id.name", "ilike", step_machine)])
        self.current_instructions = instruction_record.instruction_text

    def action_step_back(self): #button to go back
        num = int(self.current_step_num)
        num -= 1
        delete = False
        if num < 1:
            delete = True
            num = 1

        self.current_step_num = str(num)
        self.step_number_statusbar = str(num)
        self._compute_curr_step()
        if num == 1 and delete:
            order_record = self.env["print.order"].search([("name", "ilike", self.name)])
            order_record.order_status = "1"
            self.ensure_one()
            self.unlink()
            action = {
                'type': 'ir.actions.act_window',
                'name': ("Inventory List"),
                'res_model': 'print.operator',
                'view_mode': 'tree',
            }
            return action
        return True

    def action_step_forward(self): #button to go forward
        num = int(self.current_step_num)
        num += 1
        if num > int(self.step_max):
            order_record = self.env["print.order"].search([("name", "ilike", self.name)])
            order_record.order_status = "3"
            self.active = False
            num = int(self.step_max) + 1

        self.current_step_num = str(num)

        if num > int(self.step_max):
            self.current_step_num = "Order out of production"
        self.step_number_statusbar = str(num)
        self._compute_curr_step()
        return True
