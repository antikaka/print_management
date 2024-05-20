from odoo import fields, models, api


class PrintMachine(models.Model):
    _name = "print.machine"
    _description = "Print machine model"

    name = fields.Char(string="Name", required=True)
    name_readonly = fields.Boolean(compute="_compute_name_readonly")
    machine_maxspeed = fields.Char(string="Max speed")
    machine_maxwidth = fields.Char(string="Width of media")
    machine_maxlength = fields.Char(string="Max length of media")
    machine_notes = fields.Text(string="Notes")
    machine_options = fields.Many2many("print.machine.option")
    machine_option_instruction = fields.One2many("print.machine.instruction", "machine_id")
    instruction_text = fields.Text(compute="_compute_instruction_text")


    @api.depends("machine_options", "machine_options.option_instruction", "machine_option_instruction.instruction_text")
    def _compute_instruction_text(self):
        # reikia option
        # reikia instruction id (viskas per id vis tiek)
        # reikia machine? = record
        for record in self:
            text_lines = []
            for option in record.machine_options:
                for instruction in option.option_instruction:
                    if instruction.machine_id == record:
                        instructions = instruction.mapped('instruction_text')
                        name = instruction.option_id.name
                        instructions.insert(0, name)
                        text_lines.append(instructions)
            record.instruction_text = text_lines

    @api.depends("name")
    def _compute_name_readonly(self):    #after creation of machine entry, name becomes readonly
        for record in self:
            if not record.id:
                record.name_readonly = False
            else:
                record.name_readonly = True


class PrintMachineOption(models.Model):
    _name = "print.machine.option"

    name = fields.Char(string="Name")
    option = fields.Many2many("print.machine", string="Machine")
    option_instruction = fields.One2many("print.machine.instruction", "option_id")
    product_step = fields.Many2one("print.product.step", "machine_option_id")

class PrintMachineInstruction(models.Model):
    _name = "print.machine.instruction"

    option_id = fields.Many2one("print.machine.option")
    machine_id = fields.Many2one("print.machine")
    machine_n_option_name = fields.Char(compute="_get_machine_n_option_name", string="Instructions")
    instruction_text = fields.Text(string="Instructions")

    @api.depends("option_id", "machine_id")
    def _get_machine_n_option_name(self):     #name for machine options is: machine + option
        for record in self:
            option = record.option_id.name
            machine = record.machine_id.name
            name = str(machine) + " " + option

            record.machine_n_option_name = name


