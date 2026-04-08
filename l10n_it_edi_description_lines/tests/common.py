# Copyright 2026 Stefano Savanelli - Xpmi Srls
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from lxml import etree

from odoo import fields
from odoo.addons.l10n_it_edi.tests.common import TestItEdi
from odoo.tests import Form


class Common(TestItEdi):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.module = "l10n_it_edi_description_lines"
        cls.tax_ten_percent = cls.env["account.tax"].with_company(cls.company).create(
            {
                "name": "10% test",
                "amount": 10.0,
                "amount_type": "percent",
            }
        )

    def _render_invoice_tree(self, invoice):
        return etree.fromstring(invoice._l10n_it_edi_render_xml())

    def _xpath_text(self, element, xpath):
        node = element.xpath(xpath)
        return node[0].text if node else None

    def _get_detail_lines(self, tree):
        return tree.xpath(".//*[local-name()='DettaglioLinee']")

    def _get_summary_lines(self, tree):
        return tree.xpath(".//*[local-name()='DatiRiepilogo']")

    def _get_detail_line_values(self, detail_line):
        return {
            "numero_linea": self._xpath_text(detail_line, "./*[local-name()='NumeroLinea']"),
            "descrizione": self._xpath_text(detail_line, "./*[local-name()='Descrizione']"),
            "prezzo_unitario": self._xpath_text(
                detail_line, "./*[local-name()='PrezzoUnitario']"
            ),
            "prezzo_totale": self._xpath_text(
                detail_line, "./*[local-name()='PrezzoTotale']"
            ),
            "aliquota_iva": self._xpath_text(
                detail_line, "./*[local-name()='AliquotaIVA']"
            ),
            "natura": self._xpath_text(detail_line, "./*[local-name()='Natura']"),
            "quantita": self._xpath_text(detail_line, "./*[local-name()='Quantita']"),
        }

    def _get_summary_values(self, tree):
        return [
            {
                "aliquota_iva": self._xpath_text(
                    summary_line, "./*[local-name()='AliquotaIVA']"
                ),
                "natura": self._xpath_text(summary_line, "./*[local-name()='Natura']"),
                "imponibile_importo": self._xpath_text(
                    summary_line, "./*[local-name()='ImponibileImporto']"
                ),
                "imposta": self._xpath_text(summary_line, "./*[local-name()='Imposta']"),
            }
            for summary_line in self._get_summary_lines(tree)
        ]

    def _create_invoice(self, line_specs):
        invoice_form = Form(
            self.env["account.move"]
            .with_company(self.company)
            .with_context(default_move_type="out_invoice")
        )
        invoice_form.invoice_date = fields.Date.from_string("2024-01-15")
        if not invoice_form._get_modifier("date", "invisible"):
            invoice_form.date = invoice_form.invoice_date
        invoice_form.invoice_date_due = invoice_form.invoice_date
        invoice_form.partner_id = self.italian_partner_a

        for line_spec in line_specs:
            with invoice_form.invoice_line_ids.new() as line_form:
                if line_spec.get("display_type"):
                    line_form.display_type = line_spec["display_type"]
                    line_form.name = line_spec["name"]
                    continue

                line_form.name = line_spec["name"]
                line_form.price_unit = line_spec["price_unit"]
                line_form.quantity = line_spec.get("quantity", 1.0)
                line_form.tax_ids.clear()
                for tax in line_spec["taxes"]:
                    line_form.tax_ids.add(tax)

        invoice = invoice_form.save()
        invoice.action_post()
        return invoice
