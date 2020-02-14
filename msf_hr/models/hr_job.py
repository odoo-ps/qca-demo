# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class HrJob(models.Model):
    _inherit = "hr.job"

    applicant_tag_ids = fields.Many2many("hr.applicant.category", string="Tags")
    matching_applicant_count = fields.Integer(compute="_compute_matching_applicant")
    matching_applicant_ids = fields.Many2many('hr.applicant',compute="_compute_matching_applicant")

    def _get_domain_matching_applicant(self):
        self.ensure_one()
        domain = []
        for tag_id in self.applicant_tag_ids.ids:
            domain.append(('categ_ids','in',tag_id))
        return domain

    @api.depends('applicant_tag_ids')
    def _compute_matching_applicant(self):
        for rec in self:
            matching_applicants = self.env['hr.applicant'].search(self._get_domain_matching_applicant())
            rec.matching_applicant_ids = matching_applicants
            rec.matching_applicant_count = len(rec.matching_applicant_ids)

    def action_matching_applicant(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': _('Applications'),
            'res_model': "hr.applicant",
            'view_mode': 'kanban,tree,form',
            'domain': [('id', 'in', self.matching_applicant_ids.ids)],
        }
        