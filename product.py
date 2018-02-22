# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
from trytond.model import ModelView, ModelSQL, fields, Unique
from trytond.pool import PoolMeta

from trytond.modules.product.product import STATES, DEPENDS
from slug import slug

__all__ = ['Brand', 'Template']


class Brand(ModelSQL, ModelView):
    '''Brand'''
    __name__ = 'product.brand'
    name = fields.Char('Name', required=True, translate=True)
    active = fields.Boolean('Active')
    url = fields.Char('URL', translate=True)
    slug = fields.Char('Slug', translate=True)
    products = fields.One2Many('product.template', 'brand', 'Products')

    @classmethod
    def __setup__(cls):
        super(Brand, cls).__setup__()
        t = cls.__table__()
        cls._sql_constraints += [
            ('slug_uniq', Unique(t, t.active, t.slug),
                'There is another brand with the same slug.\n'
                'The slug of the active brands must be unique!'),
            ]

    @staticmethod
    def default_active():
        return True

    @fields.depends('name', 'slug', 'active')
    def on_change_with_slug(self):
        if self.name and not self.slug and self.active:
            return slug(self.name)
        else:
            return self.slug


class Template:
    __name__ = 'product.template'
    __metaclass__ = PoolMeta
    brand = fields.Many2One('product.brand', 'Brand', states=STATES,
        depends=DEPENDS)
