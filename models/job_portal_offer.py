# -*- coding: utf-8 -*-
import logging
import requests
from bs4 import BeautifulSoup
from datetime import datetime
from urllib.parse import urlparse, urlunparse, parse_qs, urlencode

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
    url = fields.Char(string=_('Url origen'))
    date_published = fields.Datetime(
        string=_('Fecha de publicación')
    )

    _sql_constraints = [
        ("portal_remote_uniq", "unique(portal_id, remote_id)", "La oferta ya existe para esta cabecera."),
    ]


    def _create_or_update(self, portal_rec, remote_id, vals):
        filt = [('portal_id','=',portal_rec.id), ('remote_id','=',remote_id)]
        offer = self.search(filt, limit=1)
        vals.update({'portal_id': portal_rec.id, 'remote_id': remote_id})
        if offer:
            offer.sudo().write(vals)
        else:
            self.create(vals)


    def _build_paged_url(self, base, page):
        parsed = urlparse(base)
        qs = parse_qs(parsed.query)
        if page > 1:
            qs['p'] = [str(page)]
        else:
            qs.pop('p', None)
        return urlunparse(parsed._replace(query=urlencode(qs, doseq=True)))
    


    def _fetch_offers_from_source(self, portal_rec, page=1, keywords=None):
        base = portal_rec.source_id.list_url.strip()
        url = self._build_paged_url(base, page)
        _logger.info("Scraping URL %s", url)
        resp = requests.get(url, headers={'User-Agent':'Mozilla/5.0'}, timeout=10)
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, 'html.parser')

        # Selector de cada “tarjeta” de oferta
        offers = soup.select('article.box_offer') or soup.select('div.oferItem') or []
        if not offers:
            _logger.info("  → No encontré ofertas en %s", url)
            return False

        # Keywords dinámicas
        if keywords:
            kws = [k.strip().lower() for k in keywords.split(',') if k.strip()]
        else:
            kws = [k.strip().lower() for k in (portal_rec.source_id.keywords or '').split(',') if k.strip()]

        for offer in offers:
            remote_id = (
                offer.get('data-jobid')
                or offer.get('data-id')
                or offer.get('data-offer-id')
            )
            if not remote_id:
                _logger.warning("  → Oferta sin ID, la salto.")
                continue

            # Buscamos el <a> que lleve al detalle. Probamos varios selectores:
            a = (
                offer.select_one('a.icl-OfferLink')
                or offer.select_one('a.js-o-link')
                or offer.select_one('h2 a[href]')
                or offer.find('a', href=True)
            )
            if not a:
                _logger.warning("  → No hallé ningún <a> para remote_id %s; salto.", remote_id)
                continue
            title = a.get_text(strip=True)
            link = a['href']

            # Compañía
            comp = offer.select_one('span.icl-OfferCompanyName') or offer.select_one('.offer-company')
            company = comp.get_text(strip=True) if comp else False

            # Descripción
            desc = offer.select_one('p.icl-OfferDescription') or offer.select_one('.offer-snippet')
            description = desc.get_text(strip=True) if desc else False

            # Fecha si existe
            date_tag = offer.select_one('time')
            try:
                date_pub = datetime.fromisoformat(date_tag['datetime']) if date_tag and date_tag.has_attr('datetime') else False
            except Exception:
                date_pub = False

            # Filtrado por keywords
            text = (title + ' ' + (description or '')).lower()
            if kws and not any(kw in text for kw in kws):
                _logger.debug("  → Oferta %s no cumple filters %s; salto.", remote_id, kws)
                continue

            vals = {
                'name': title,
                'company': company,
                'description': description,
                'url': link,
                'date_published': date_pub,
            }
            self.env['job.portal.offer'].sudo()._create_or_update(portal_rec, remote_id, vals)

        return True
