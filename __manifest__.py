{
    'name': 'Crm Dashboard',
    'description': 'Crm dashboard',
    'installable': True,
    'version': '16.0.1.0.0',
    'depends': ['base', 'crm', 'sale'],
    'data': ['views/sales_team_inherit_view.xml',
             'views/crm_dashboard_view.xml', ],
    'assets': {
        'web.assets_backend': [
            '/crm_dashboard/static/src/js/crm_dashboard.js',
            '/crm_dashboard/static/src/xml/dashboard_view.xml',
            '/crm_dashboard/static/src/scss/style.scss',
            'https://cdn.jsdelivr.net/npm/chart.js',
        ]}
}
