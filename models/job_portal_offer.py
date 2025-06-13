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
    remote_id = fields.Char(
        string='ID en portal',
        required=True,
        index=True,
        copy=False
    )
    name = fields.Char(string=_('Título'), required=True)
    company = fields.Char(string=_('Empresa'))
    description = fields.Text(string=_('Descripción'))
    Url = fields.Char(string=_('Url origen'))
    date_published = fields.Datetime(
        string=_('Fecha de publicación')
    )

    _sql_constraints = [
        ("portal_remote_uniq", "unique(portal_id, remote_id)", "La oferta ya existe para esta cabecera."),
    ]


    def _fetch_offers_from_source(self):
        pass

