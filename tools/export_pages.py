"""Export every page/slide supported by LibreOffice Draw/Impress to PNG."""

from __future__ import annotations

import sys
from pathlib import Path

import uno
from com.sun.star.beans import PropertyValue


def prop(name, value):
    item = PropertyValue()
    item.Name = name
    item.Value = value
    return item


def export(source: Path, output: Path):
    output.mkdir(parents=True, exist_ok=True)
    local = uno.getComponentContext()
    resolver = local.ServiceManager.createInstanceWithContext("com.sun.star.bridge.UnoUrlResolver", local)
    context = resolver.resolve("uno:socket,host=localhost,port=2002;urp;StarOffice.ComponentContext")
    desktop = context.ServiceManager.createInstanceWithContext("com.sun.star.frame.Desktop", context)
    document = desktop.loadComponentFromURL(uno.systemPathToFileUrl(str(source.resolve())), "_blank", 0, (prop("Hidden", True),))
    pages = document.getDrawPages()
    exporter = context.ServiceManager.createInstanceWithContext("com.sun.star.drawing.GraphicExportFilter", context)
    page_count = pages.getCount()
    for index in range(page_count):
        exporter.setSourceDocument(pages.getByIndex(index))
        target = output / f"page-{index + 1:02d}.png"
        exporter.filter((prop("URL", uno.systemPathToFileUrl(str(target.resolve()))), prop("MediaType", "image/png"), prop("PixelWidth", 1600), prop("PixelHeight", 1000)))
    document.close(True)
    print(f"pages={page_count}")


if __name__ == "__main__":
    export(Path(sys.argv[1]), Path(sys.argv[2]))

