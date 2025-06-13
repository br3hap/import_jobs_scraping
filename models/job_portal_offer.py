# -*- coding: utf-8 -*-
import logging

from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError

_logger = logging.getLogger(__name__)


class JobPortalOffer(models.Model):
    _name = 'job.portal.offer'
    _description = 'Oferta de empleo importada'

    portal_id = fields.Many2one(
        comodel_name='job.portal',
        string='Cabecera Portal',
        required=True,
        ondelete='cascade'
    )
