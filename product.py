# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
from trytond.model import fields, Unique
from trytond.pool import PoolMeta

from slug import slug

__all__ = ['Brand']


class Brand:
    __metaclass__ = PoolMeta
    __name__ = 'product.brand'
    url = fields.Char('URL', translate=True)
    slug = fields.Char('Slug', translate=True)
    metadescription = fields.Char('Meta Description', translate=True,
        help=('Almost all search engines recommend it to be shorter than 155 '
            'characters of plain text'))
    metakeywords = fields.Char('Meta Keywords', translate=True)
    metatitle = fields.Char('Meta Title', translate=True)

    @classmethod
    def __setup__(cls):
        super(Brand, cls).__setup__()
        t = cls.__table__()
        cls._sql_constraints += [
            ('slug_uniq', Unique(t, t.active, t.slug),
                ('There is another brand with the same slug. The slug of the '
                    'active brands must be unique!')),
            ]

    @fields.depends('name', 'slug', 'active')
    def on_change_with_slug(self):
        if self.name and not self.slug and self.active:
            return slug(self.name)
        else:
            return self.slug
