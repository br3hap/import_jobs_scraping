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
    


