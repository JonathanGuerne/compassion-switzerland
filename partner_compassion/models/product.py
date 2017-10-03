# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2014 Compassion CH (http://www.compassion.ch)
#    Releasing children from poverty in Jesus' name
#    @author: Emanuel Cino <ecino@compassion.ch>
#
#    The licence is in the file __openerp__.py
#
##############################################################################
from odoo.tools import mod10r

from odoo import api, models, fields


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    fund_id = fields.Integer(size=4)


class Product(models.Model):
    _inherit = 'product.product'

    fund_id = fields.Integer(related='product_tmpl_id.fund_id')

    @api.multi
    def generate_bvr_reference(self, partner):
        """
        Generates a BVR reference for the product.
        :param partner:
        :return: string: the BVR reference
        """
        self.ensure_one()
        ref = partner.ref
        bvr_reference = '0' * (9 + (7 - len(ref))) + ref
        commitment_number = '0'
        bvr_reference += '0' * (5 - len(commitment_number)) + commitment_number
        # Type for Funds => 6
        bvr_reference += '6'
        # Fund id
        fund_id = str(self.fund_id)
        bvr_reference += '0' * (4 - len(fund_id)) + fund_id

        if len(bvr_reference) == 26:
            return self.env['l10n_ch.payment_slip']._space(mod10r(
                bvr_reference).lstrip('0'))
