{
    'name': 'Hospital Management System',
    'depends': ['base', 'contacts'],
    'data': [
        'security/groups.xml',
        'security/record_rules.xml',
        'security/ir.model.access.csv',
        'views/patient_views.xml',
        'views/department_views.xml',
        'views/doctor_views.xml',
        'views/res_partner_views.xml',
        'reports/patient_report.xml',
    ],
    'installable': True,
    'application': True,
}
