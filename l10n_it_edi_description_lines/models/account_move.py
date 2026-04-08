# Copyright 2026 Stefano Savanelli - Xpmi Srls
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import models


class AccountMove(models.Model):
    _inherit = "account.move"

    def _l10n_it_edi_get_values(self, pdf_values=None):
        res = super()._l10n_it_edi_get_values(pdf_values=pdf_values)
        base_lines = res.get("base_lines", [])
        tax_lines = res.get("tax_lines", [])

        description_tax_values = self._l10n_it_edi_get_description_line_tax_values(
            tax_lines, base_lines
        )
        res["export_lines"] = self._l10n_it_edi_get_export_lines(
            base_lines, description_tax_values
        )
        return res

    def _l10n_it_edi_get_description_line_tax_values(self, tax_lines, base_lines):
        self.ensure_one()
        if tax_lines:
            return {
                "aliquota_iva": tax_lines[0].get("aliquota_iva", 0.0),
                "natura": tax_lines[0].get("natura"),
            }

        for base_line in base_lines:
            it_values = base_line.get("it_values", {})
            aliquote_iva = it_values.get("aliquota_iva_list") or []
            if aliquote_iva:
                return {
                    "aliquota_iva": aliquote_iva[0],
                    "natura": it_values.get("natura"),
                }

        return {
            "aliquota_iva": 0.0,
            "natura": None,
        }

    def _l10n_it_edi_get_export_lines(self, base_lines, description_tax_values):
        self.ensure_one()
        remaining_base_lines = {}
        unmatched_base_lines = []
        for base_line in base_lines:
            source_line_id = self._l10n_it_edi_get_export_source_line_id(base_line)
            if source_line_id:
                remaining_base_lines.setdefault(source_line_id, []).append(base_line)
            else:
                unmatched_base_lines.append(base_line)

        export_lines = []
        numero_linea = 1
        for line in self.invoice_line_ids.sorted(lambda move_line: (move_line.sequence, move_line.id)):
            if line.display_type in ("line_section", "line_subsection", "line_note"):
                export_lines.append(
                    {
                        "line_type": "description",
                        "it_values": {
                            "numero_linea": numero_linea,
                            "descrizione": self._l10n_it_edi_get_description_line_text(
                                line
                            ),
                            "aliquota_iva": description_tax_values["aliquota_iva"],
                            "natura": description_tax_values["natura"],
                        },
                    }
                )
                numero_linea += 1
                continue

            for base_line in remaining_base_lines.pop(line.id, []):
                base_line["it_values"]["numero_linea"] = numero_linea
                export_lines.append({"line_type": "base", "base_line": base_line})
                numero_linea += 1

        for base_line in unmatched_base_lines:
            base_line["it_values"]["numero_linea"] = numero_linea
            export_lines.append({"line_type": "base", "base_line": base_line})
            numero_linea += 1

        for source_line_id in sorted(remaining_base_lines):
            for base_line in remaining_base_lines[source_line_id]:
                base_line["it_values"]["numero_linea"] = numero_linea
                export_lines.append({"line_type": "base", "base_line": base_line})
                numero_linea += 1

        return export_lines

    def _l10n_it_edi_get_export_source_line_id(self, base_line):
        base_line_id = base_line.get("id")
        if isinstance(base_line_id, int):
            return base_line_id
        if isinstance(base_line_id, str) and base_line_id.endswith("_vat"):
            source_line_id = base_line_id.removesuffix("_vat")
            if source_line_id.isdigit():
                return int(source_line_id)

        record = base_line.get("record")
        if record and record.id:
            return record.id
        if record and record._origin and record._origin.id:
            return record._origin.id
        return None

    def _l10n_it_edi_get_description_line_text(self, line):
        self.ensure_one()
        return line.name and " ".join(line.name.replace("\n", " ").split()) or "NO NAME"
