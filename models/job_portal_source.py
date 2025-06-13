# -*- coding: utf-8 -*-
import logging

from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError

_logger = logging.getLogger(__name__)


class JobPortalSource(models.Model):
    _name = 'job.portal.source'
    _description = 'Fuente de portal de empleo'

    code = fields.Char(
        string='Código interno',
        required=True,
        help='Identificador único (ej: computrabajo)'
    )
    name = fields.Char(
        string='Name',
        required=True,
        help='Nombre legible del portal'
        )
    
    _sql_constraints = [
        ('code_uniq', 'unique(code)', 'El código del portal debe ser único.')
    ]
