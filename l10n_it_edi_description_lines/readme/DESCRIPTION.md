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

### Compatibilita' futura con `l10n_it_edi_extension`

La PR OCA [#5196](https://github.com/OCA/l10n-italy/pull/5196), al momento
destinata alla versione 18.0, introduce in `l10n_it_edi_extension` una diversa
gestione configurabile delle note e delle sezioni nella fattura elettronica.
Le due implementazioni intervengono sullo stesso flusso di esportazione e non
devono essere utilizzate insieme: potrebbero produrre righe duplicate oppure
ignorare la configurazione di inclusione/esclusione.

La PR #5196 non e' comunque un sostituto diretto di questo modulo nella versione
19.0: non gestisce `line_subsection` e usa le strutture fiscali della versione
18.0. Prima di rimuovere questo modulo sara' necessario verificare il relativo
forward-port 19.0, inclusi ordinamento, aliquota IVA, Natura, righe con ID
`_vat` e fatture semplificate.

La suite contiene un test di guardia che cerca nel sorgente disponibile di
`l10n_it_edi_extension` i simboli introdotti dalla PR #5196. Il test fallisce
intenzionalmente quando rileva quella implementazione, anche se il modulo non e'
installato nel database di test, per richiedere una revisione esplicita.

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

### Future compatibility with `l10n_it_edi_extension`

OCA PR [#5196](https://github.com/OCA/l10n-italy/pull/5196), currently targeting
version 18.0, introduces a different configurable implementation for exporting
invoice notes and sections in `l10n_it_edi_extension`. Both implementations
alter the same export flow and must not be used together, as they may duplicate
lines or bypass the include/exclude configuration.

PR #5196 is not a direct replacement for this module on version 19.0: it does
not handle `line_subsection` and relies on version 18.0 tax structures. Before
removing this module, its 19.0 forward-port must be checked for ordering, VAT
rate, tax exemption reason, `_vat` line identifiers and simplified invoices.

The test suite includes a compatibility guard that searches the available
`l10n_it_edi_extension` source for symbols introduced by PR #5196. It fails
intentionally when that implementation is detected, even if the extension is
not installed in the test database, so that the overlap is reviewed explicitly.
