# -*- coding: utf-8 -*-
import logging

from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError

_logger = logging.getLogger(__name__)


class JobPortal(models.Model):
    _name = 'job.portal'
    _description = 'Portal de empleo'

    
