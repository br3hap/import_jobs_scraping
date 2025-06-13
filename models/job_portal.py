# -*- coding: utf-8 -*-
import logging

from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError

_logger = logging.getLogger(__name__)


class JobPortal(models.Model):
    _name = 'job.portal'
    _description = 'Portal de empleo'

    source_id = fields.Many2one(
        comodel_name = 'job.portal.source', 
        string='portal',
        required=True,
        ondelete='cascade'
        )
    
    offer_ids = fields.One2many(
        comodel_name='job.portal.offer', 
        inverse_name='portal_id', 
        string='Ofertas')
    
    _sql_constraints = [
        ('source_uniq',
         'unique(source_id)',
         'Ya existe una cabecera para este portal.'
         )
    ]


    def get_or_created(self, source_code):
        source = self.env['job.portal.source'].search([('code','=',source_code)], limit=1)
        if not source:
            raise ValueError(f"No existe fuente de portal con code `{source_code}`.")
        
        portal = self.search([('source_id','=',source.id)], limit=1)
        if portal:
            return portal
        return self.create({'source_id': source.id})
    

    def action_open_search_wizard(self):
        pass