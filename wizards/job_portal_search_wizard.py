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
    

    def action_search(self):
        Offer = self.env['job.portal.offer'].sudo()
        Portal = self.env['job.portal'].sudo()
        for source in self.source_ids:
            portal_rec = Portal.get_or_created(source.code)
            page = 1
            while True:
                more = Offer._fetch_offers_from_source(
                    portal_rec,
                    page=page,
                    keywords=self.keywords
                )
                if not more:
                    break
                page += 1

        return {
            'name': 'Ofertas encontradas',
            'view_mode': 'tree, form',
            'res_model': 'job.portal.offer',
            'type': 'ir.actions.act_window',
            'domain':[('portal_id.source_id', 'in', self.source_ids.ids)],
        }