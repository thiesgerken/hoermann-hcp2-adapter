# ESP32-C3 Super Mini

Originalangebot: <https://de.aliexpress.com/item/1005005967641936.html>

AliExpress-Artikel `1005005967641936` verkauft ein TENSTAR ROBOT ESP32-C3 SuperMini Entwicklungsboard mit WLAN, Bluetooth und USB-C. Das im Projekt verwendete Board besitzt 16 Anschlüsse in zwei Reihen mit 2,54-mm-Raster. Die verbreitete Referenzbauform misst ungefähr 22,52 × 18 mm.

## Verwendung im Projekt

U1 führt ESPHome aus. GPIO21 ist als UART-TX und GPIO20 als UART-RX vorgesehen. Das Board wird über seinen 5-V-Pin versorgt und versorgt das RS485-Modul vorläufig mit 3,3 V. Externe 5-V-Versorgung und USB dürfen nicht gleichzeitig verbunden sein, weshalb die Platine den Jumper `BUS_PWR` besitzt.

## Archivinhalt

- `product-description.txt`: lesbarer Seitentext mit Originalquelle und Abrufdatum
- `product-page-raw.html` und `product-page-rendered.html`: rohe und gerenderte Produktseite
- `gallery-01.webp` bis `gallery-06.webp`: Händlerbilder des Boards
- `rendered-image-urls.txt`: Bildquellen aus der gerenderten Seite

Archiviert am 2026-09-05. Offensichtlich fehlerhafte automatisch erzeugte Händlerangaben, beispielsweise eine Versorgungsspannung von 1 V, werden nicht als technische Spezifikation übernommen.
