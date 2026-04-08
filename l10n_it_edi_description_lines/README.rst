.. image:: https://odoo-community.org/readme-banner-image
   :target: https://odoo-community.org/get-involved?utm_source=readme
   :alt: Odoo Community Association

=======================================
Italy - E-invoicing - Description Lines
=======================================

.. |badge1| image:: https://img.shields.io/badge/maturity-Beta-yellow.png
    :target: https://odoo-community.org/page/development-status
    :alt: Beta
.. |badge2| image:: https://img.shields.io/badge/license-AGPL--3-blue.png
    :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
    :alt: License: AGPL-3
.. |badge3| image:: https://img.shields.io/badge/github-OCA%2Fl10n--italy-lightgray.png?logo=github
    :target: https://github.com/OCA/l10n-italy/tree/19.0/l10n_it_edi_description_lines
    :alt: OCA/l10n-italy

|badge1| |badge2| |badge3|

**Italiano**

Questo modulo esporta nella fattura elettronica italiana le righe descrittive
presenti nella fattura Odoo e normalmente visibili nel PDF ma assenti dal file XML.

In particolare gestisce le righe con ``display_type``:

- ``line_section``
- ``line_subsection``
- ``line_note``

Le righe vengono esportate come ``DettaglioLinee`` a importo zero, mantenendo
l'ordine originale del documento e senza modificare i ``DatiRiepilogo`` gia'
calcolati dal modulo base ``l10n_it_edi``.

Per rendere valide le righe descrittive nel tracciato FatturaPA, il modulo
assegna loro l'aliquota IVA del primo riepilogo fiscale disponibile.

**English**

This module exports Odoo descriptive invoice lines into the Italian electronic
invoice XML, covering lines that are usually visible in the PDF but missing from
the generated XML file.

It handles invoice lines with the following ``display_type`` values:

- ``line_section``
- ``line_subsection``
- ``line_note``

These lines are exported as zero-amount ``DettaglioLinee`` entries, keeping the
original document order without changing the ``DatiRiepilogo`` values already
computed by the base ``l10n_it_edi`` module.

To keep descriptive lines valid in the FatturaPA schema, the module assigns them
the VAT rate from the first available tax summary.

Contributors
~~~~~~~~~~~~

- Stefano Savanelli <ssavanelli@xpmi.it>
- Xpmi Srls
