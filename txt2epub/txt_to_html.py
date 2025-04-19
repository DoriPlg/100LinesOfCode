import sys
import os
import zipfile
def header(file_name: str, title: str) -> None:
    with open(file_name, 'w', encoding='utf-8') as f:
        f.write(f'''<?xml version="1.0" encoding="UTF-8"?>
    <!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN"
    "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
    <html xmlns="http://www.w3.org/1999/xhtml">
    <head>
    <title>{title}</title>
    <meta http-equiv="Content-Type" content="text/html; charset=UTF-8" /> </head> <body>''')
def footer(file_name: str) -> None:
    with open(file_name, 'a', encoding='utf-8') as f:
        f.write('''</body></html>''')
def write_paragraph(file_name: str, paragraph: str) -> None:
    with open(file_name, 'a', encoding='utf-8') as f:
        f.write(f'''<p>{paragraph}</p>''')
def get_paragraphs(file_name: str) -> list[str]:
    with open(file_name, 'r', encoding='utf-8') as f:
        return f.readlines()
def write_container(out_file: str) -> None:
    os.mkdir(f"{out_file}/META-INF")
    with open(f"{out_file}/META-INF/container.xml", 'w', encoding='utf-8') as f:
        f.write(f'''<?xml version="1.0" encoding="UTF-8"?>
    <container version="1.0"
    xmlns="urn:oasis:names:tc:opendocument:xmlns:container">
    <rootfiles>
        <rootfile full-path="OEBPS/{out_file}.opf"
        media-type="application/oebps-package+xml"/> </rootfiles> </container> ''')
def write_xhtml(out_file: str, in_file: str, title:str) -> None:
    header(f"{out_file}/OEBPS/{out_file}.xhtml", title)
    for paragraph in get_paragraphs(in_file):
        write_paragraph(f"{out_file}/OEBPS/{out_file}.xhtml", paragraph)
    footer(f"{out_file}/OEBPS/{out_file}.xhtml")
def write_mime(out_file: str) -> None:
    with open(f"{out_file}/mimetype", 'w', encoding='utf-8') as f:
        f.write('application/epub+zip')
def write_opf(out_file: str) -> None:
    with open(f"{out_file}/OEBPS/{out_file}.opf", 'w', encoding='utf-8') as f:
        f.write(f'''<?xml version="1.0" encoding="UTF-8"?>
    <package xmlns="http://www.idpf.org/2007/opf" version="2.0"
    unique-identifier="BookId">
    <metadata xmlns:dc="http://purl.org/dc/elements/1.1/">
        <dc:title>My Book</dc:title>
        <dc:language>en</dc:language>
        <dc:identifier id="BookId">book-id-123</dc:identifier>
    </metadata>
    <manifest>
        <item id="{out_file}" href="{out_file}.xhtml" media-type="application/xhtml+xml"/>
        <item id="ncx" href="toc.ncx" media-type="application/x-dtbncx+xml"/>
    </manifest>
    <spine toc="ncx">
        <itemref idref="{out_file}"/> </spine> </package>''')
def write_toc(out_file: str) -> None:
    with open(f"{out_file}/OEBPS/toc.ncx", 'w', encoding='utf-8') as f:
        f.write(f'''<?xml version="1.0" encoding="UTF-8"?>
    <ncx xmlns="http://www.daisy.org/z3986/2005/ncx/" version="2005-1">
    <head>
        <meta name="dtb:uid" content="book-id-123"/>
        <meta name="dtb:depth" content="1"/>
        <meta name="dtb:totalPageCount" content="0"/>
        <meta name="dtb:maxPageNumber" content="0"/>
    </head>
    <docTitle><text>{out_file.capitalize()}</text></docTitle>
    <navMap>
        <navPoint id="navPoint-1" playOrder="1">
        <navLabel><text>Start</text></navLabel>
        <content src="{out_file}.xhtml"/>
        </navPoint> </navMap> </ncx> ''')
def create_epub(epub_name, base_dir='.'):
    base_dir = os.path.abspath(base_dir)
    epub_path = os.path.join(base_dir, epub_name)
    with zipfile.ZipFile(epub_path, 'w') as epub:
        mimetype_path = os.path.join(base_dir, 'mimetype')
        epub.write(mimetype_path, 'mimetype', compress_type=zipfile.ZIP_STORED)
        for folder in ['META-INF', 'OEBPS']:
            folder_path = os.path.join(base_dir, folder)
            for root, _, files in os.walk(folder_path):
                for file in files:
                    full_path = os.path.join(root, file)
                    arcname = os.path.relpath(full_path, base_dir)
                    epub.write(full_path, arcname, compress_type=zipfile.ZIP_DEFLATED)
if __name__ == '__main__' and len(sys.argv) == 3:
    _, in_file, title = sys.argv
    out_file = in_file.split('.')[0]
    os.mkdir(out_file)
    os.mkdir(f"{out_file}/OEBPS")
    write_mime(out_file)
    write_container(out_file)
    write_xhtml(out_file, in_file, title)
    write_opf(out_file)
    write_toc(out_file)
    create_epub(f"{out_file}.epub", out_file)
else:
    print('Usage: python txt_to_html.py <in_file> <title>')
