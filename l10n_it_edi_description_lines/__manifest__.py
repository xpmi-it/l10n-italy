# Copyright 2026 Stefano Savanelli - Xpmi Srls
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    "name": "Italy - E-invoicing - Description Lines",
    "version": "19.0.1.0.0",
    "category": "Accounting/Localizations/EDI",
    "development_status": "Beta",
    "summary": "Export section and note lines in Italian electronic invoices",
    "author": "Stefano Savanelli, Xpmi Srls, Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/l10n-italy",
    "license": "AGPL-3",
    "depends": [
        "l10n_it_edi",
    ],
    "data": [
        "data/invoice_it_template.xml",
    ],
    "images": ["static/description/icon.png"],
    "installable": True,
}
