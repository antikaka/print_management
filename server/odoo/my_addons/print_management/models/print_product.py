
from odoo import fields, models, api

class PrintProduct(models.Model):
    _name = "print.product"
    _description = "Print product model"

    name = fields.Char(string="Name", required=True)
    product_step = fields.One2many("print.product.step", "product_id")
    order_id = fields.One2many("print.order", "product")

class PrintProductStep(models.Model):
    _name = "print.product.step"
    _description = "Print product step model"

    product_id = fields.Many2one("print.product")
    machine_option_id = fields.Many2one("print.machine.option")
    sequence = fields.Integer(string="Sequence", default=1)
    step_name = fields.Char(compute="_compute_step_name", precompute=True, store=True)


    @api.depends("machine_option_id")
    def _compute_step_name(self):                      #product step name is basically the machine option name
        for step in self:
            if step.machine_option_id:
                step.step_name = step.machine_option_id.name
            else:
                pass

    @api.model_create_multi
    def create(self, vals_list):  #this is basically for creating/keeping the sequence of the product steps
        product_steps = super(PrintProductStep, self).create(vals_list)
        for steps in product_steps:
            steps._update_step_sequence()
        return steps

    @api.depends("product_id", "machine_option_id")
    def _update_step_sequence(self):  #the product step sequence itself
        for product in self:
            sequence = 1
            for step in product.product_id.product_step:
                step.sequence = sequence
                sequence += 1

