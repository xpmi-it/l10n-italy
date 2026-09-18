# Copyright 2026 Stefano Savanelli - Xpmi Srls
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from pathlib import Path

from odoo.modules.module import get_module_path
from odoo.tests.common import TransactionCase


class TestCompatibility(TransactionCase):
    def test_l10n_it_edi_extension_does_not_export_description_lines(self):
        """Fail when the conflicting implementation from OCA PR 5196 appears."""
        extension_path = get_module_path("l10n_it_edi_extension", display_warning=False)
        if not extension_path:
            return

        source = "\n".join(
            path.read_text(encoding="utf-8")
            for path in Path(extension_path, "models").glob("*.py")
        )
        conflict_markers = {
            "l10n_it_edi_hide_line_type",
            "_l10n_it_edi_get_descriptive_base_line",
            "_l10n_it_edi_hide_base_lines",
        }
        detected_markers = sorted(
            marker for marker in conflict_markers if marker in source
        )
        detected_markers_text = ", ".join(detected_markers)

        self.assertFalse(
            detected_markers,
            f"Potential conflict with OCA/l10n-italy PR #5196 detected in "
            f"l10n_it_edi_extension: {detected_markers_text}. "
            "Do not install both implementations; "
            "review whether this module must be removed or reconciled with the "
            "OCA implementation.",
        )
