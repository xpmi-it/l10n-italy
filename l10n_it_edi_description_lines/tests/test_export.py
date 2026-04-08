# Copyright 2026 Stefano Savanelli - Xpmi Srls
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from .common import Common


class TestExport(Common):
    def test_export_section_and_note_lines(self):
        invoice = self._create_invoice(
            [
                {"display_type": "line_section", "name": "Consulting services"},
                {
                    "name": "Main service",
                    "price_unit": 100.0,
                    "taxes": [self.default_tax],
                },
                {"display_type": "line_note", "name": "Detailed note\nwith line break"},
                {
                    "name": "Second service",
                    "price_unit": 50.0,
                    "taxes": [self.default_tax],
                },
            ]
        )

        tree = self._render_invoice_tree(invoice)
        detail_lines = [self._get_detail_line_values(line) for line in self._get_detail_lines(tree)]

        self.assertEqual(len(detail_lines), 4)
        self.assertEqual(
            detail_lines[0],
            {
                "numero_linea": "1",
                "descrizione": "Consulting services",
                "prezzo_unitario": "0.00000000",
                "prezzo_totale": "0.00000000",
                "aliquota_iva": "22.00",
                "natura": None,
                "quantita": None,
            },
        )
        self.assertEqual(detail_lines[1]["numero_linea"], "2")
        self.assertEqual(detail_lines[1]["descrizione"], "Main service")
        self.assertEqual(
            detail_lines[2],
            {
                "numero_linea": "3",
                "descrizione": "Detailed note with line break",
                "prezzo_unitario": "0.00000000",
                "prezzo_totale": "0.00000000",
                "aliquota_iva": "22.00",
                "natura": None,
                "quantita": None,
            },
        )
        self.assertEqual(detail_lines[3]["numero_linea"], "4")
        self.assertEqual(detail_lines[3]["descrizione"], "Second service")

        self.assertEqual(
            self._get_summary_values(tree),
            [
                {
                    "aliquota_iva": "22.00",
                    "natura": None,
                    "imponibile_importo": "150.00",
                    "imposta": "33.00",
                }
            ],
        )

    def test_description_lines_use_first_summary_tax(self):
        invoice = self._create_invoice(
            [
                {"display_type": "line_section", "name": "Mixed rates"},
                {
                    "name": "Reduced VAT line",
                    "price_unit": 100.0,
                    "taxes": [self.tax_ten_percent],
                },
                {"display_type": "line_note", "name": "Informational note"},
                {
                    "name": "Standard VAT line",
                    "price_unit": 50.0,
                    "taxes": [self.default_tax],
                },
            ]
        )

        tree = self._render_invoice_tree(invoice)
        detail_lines = [self._get_detail_line_values(line) for line in self._get_detail_lines(tree)]
        summary_values = self._get_summary_values(tree)

        self.assertEqual(summary_values[0]["aliquota_iva"], "10.00")
        self.assertEqual(detail_lines[0]["aliquota_iva"], "10.00")
        self.assertEqual(detail_lines[2]["aliquota_iva"], "10.00")
        self.assertEqual(
            summary_values,
            [
                {
                    "aliquota_iva": "10.00",
                    "natura": None,
                    "imponibile_importo": "100.00",
                    "imposta": "10.00",
                },
                {
                    "aliquota_iva": "22.00",
                    "natura": None,
                    "imponibile_importo": "50.00",
                    "imposta": "11.00",
                },
            ],
        )

    def test_description_lines_do_not_change_tax_summary(self):
        reference_invoice = self._create_invoice(
            [
                {
                    "name": "Main service",
                    "price_unit": 100.0,
                    "taxes": [self.default_tax],
                },
                {
                    "name": "Second service",
                    "price_unit": 50.0,
                    "taxes": [self.default_tax],
                },
            ]
        )
        invoice_with_description_lines = self._create_invoice(
            [
                {"display_type": "line_section", "name": "Consulting services"},
                {
                    "name": "Main service",
                    "price_unit": 100.0,
                    "taxes": [self.default_tax],
                },
                {"display_type": "line_note", "name": "Informational note"},
                {
                    "name": "Second service",
                    "price_unit": 50.0,
                    "taxes": [self.default_tax],
                },
            ]
        )

        reference_summary = self._get_summary_values(self._render_invoice_tree(reference_invoice))
        current_summary = self._get_summary_values(
            self._render_invoice_tree(invoice_with_description_lines)
        )

        self.assertEqual(current_summary, reference_summary)
