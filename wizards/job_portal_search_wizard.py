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
        portal_ids = []
        # Iterar sobre cada portal seleccionado
        for source in self.source_ids:
            portal = Portal.get_or_created(source.code)
            portal_ids.append(portal.id)
            page = 1
            # Raspar todas las páginas
            while True:
                more = Offer._fetch_offers_from_source(
                    portal, page=page, keywords=self.keywords
                )
                if not more:
                    break
                page += 1

        # Abrir vista con todas las ofertas de los portales elegidos
        return {
            'name': 'Ofertas Encontradas',
            'view_mode': 'tree,form',
            'res_model': 'job.portal.offer',
            'type': 'ir.actions.act_window',
            'domain': [('portal_id', 'in', portal_ids)],
        }