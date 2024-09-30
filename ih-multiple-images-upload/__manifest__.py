{
    'name': 'Product Multiple Images Upload',
    'author': 'Mina samy',
    'version': '1.0',
    'website': 'https://www.inspirehub.net',
    'category': 'Sales',
    'description': 'Module to upload multiple images for a product',
    'summary': """
        Module to upload multiple images for a product
    """,
    'depends': [
        'web',
        'website_sale',
        'website',
    ],
    'data': [
        'views/view.xml',
    ],
    'images': ['static/description/icon.png'],
    'license': 'LGPL-3',
    'assets': {
        'web.assets_backend': [
            'ih-multiple-images-upload/static/src/views/fields/multi.js',
            # 'product_multiple_images_upload/static/src/views/fields/multi.xml',
            'ih-multiple-images-upload/static/src/views/fields/multi.xml',
        ],
    },
# 'assets': {
#         'web.assets_backend': [
#             'product_multiple_images_upload/static/src/multi.js',
#             'product_multiple_images_upload/static/src/multi.xml',
#         ],
#     },
    'installable': True,
    'auto_install': False,
    'application': True,
}
