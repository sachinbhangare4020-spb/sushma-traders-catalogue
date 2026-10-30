# Sushma Traders catalogue: data kit

## Files
- `extract.py` (shared helpers), `extract2.py` (ABRO, Doctor, CUMI Shine Line, Vini), `extract3.py` (CUMI retail pages), `build_data.py` (cleaning, GST rates, video links -> `products.json`)
- `enrich_google.py` optional web enrichment through the Google Custom Search API

## How the PDF parser works (PyMuPDF)
1. `page.get_image_info(xrefs=True)` gives every embedded image with its position on the page.
2. `page.get_text('words')` / `get_text('dict')` gives text with positions and font/colour.
3. A product = a heading (by font size, or white text on a coloured bar) plus the images and text in the same column below it.
   - Drools: each pack image has an "MRP" bubble just above it. Weight + MRP are read from that text and tied to the image.
   - ABRO: headings are white "AIPL ABRO ..." bars. Bullets start with a dot, part numbers with "PART NO.".
   - Raster-only pages (CUMI retail) have no text, so crops are set by hand in `extract3.py`.
4. Images with transparency are rebuilt from their soft-mask (`doc.extract_image(xref)['smask']`) and put on white.

## products.json
`brands[]`: id, name, tag, color, gst (percent). `products[]`: id, brand, cat, name, img, variants[{label, mrp|null, part}], bullets[], page.
- `mrp: null` shows "Price on request". To add a price, set `mrp` on a variant and republish.
- GST per brand: `brands[].gst`. Defaults are 18 for every brand. Confirm the right rate per HSN code with your CA.
- Prices are treated as MRP including GST: taxable = price / (1 + rate).

## index.html settings (top of the script)
- `CONFIG.whatsapp` : distributor number with country code, e.g. `919876543210`. Empty = the cart asks for it.
- `CONFIG.sellerGstin` : printed in the WhatsApp order.
- Replace `logo.svg` with your real logo (same file name).

## Adding a new catalogue
Write a block like those in `extract2.py` (open PDF, find headings, collect images, `save(...)`), append to the list, rerun `build_data.py`, republish the files.
