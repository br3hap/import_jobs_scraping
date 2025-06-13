# -*- coding: utf-8 -*-
import logging

from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError

_logger = logging.getLogger(__name__)


class JobPortalSearchWizard(models.TransientModel):
    _name = 'job.portal.search.wizard'
    _description = _('Asistente búsqueda ofertas por palabra clave')


    source_ids = fields.Many2many(
        comodel_name='job.portal.source', 
        string='Portales',
        required=True
        )
    keywords = fields.Char(
        string=_('Palabras clave'),
        required=True,
        help="Palabras separadas por coma"
        )