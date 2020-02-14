# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class HrJob(models.Model):
    _inherit = "hr.applicant"

    def grant_portal_access(self):
        #create contacts for each applicant
        for rec in self.filtered(lambda x: not x.partner_id):
            rec.partner_id = self.env["res.partner"].create({
                "name": rec.partner_name,
                "email": rec.email_from
            })
        #pop up portal access wizard
        linked_partner_ids = self.mapped("partner_id").ids
        context = dict(self._context or {})
        context.update({
            'active_id': linked_partner_ids[:1],
            'active_ids': linked_partner_ids,
            'active_model': 'res.partner'
            })
        return {
            "name": _("Grant Portal Access"),
            "type": "ir.actions.act_window",
            "view_mode": "form",
            "res_model": "portal.wizard",
            "target": "new",
            "context": context
        }

