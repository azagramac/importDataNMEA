# 🛰️ Procesador de datos GPS NMEA `$GPRMC`

Script en **Python** para procesar datos GPS NMEA del tipo `$GPRMC` provenientes del dispositivo **Leadtek 9553D** (o similares), que genera:

- 📄 Un informe en formato **Markdown** con coordenadas, velocidades y enlaces directos a Google Maps.
- 🗺️ Ficheros `.gpx` por cada **año registrado**, con rutas diarias y cálculo de distancia recorrida.

---

## ⚙️ Requisitos

- Python **3.2 o superior**
- 📦 Dependencias:
  - [`tabulate`](https://pypi.org/project/tabulate/)

### 🔧 Instalación de dependencias

```bash
pip install tabulate
```

---

## 📥 Instalación y uso

1. Clona el repositorio:

```bash
git clone https://github.com/azagramac/importDataNMEA.git
cd importDataNMEA
```

2. Ejecuta el script:


```bash
./leadtek-gps.py -i /ruta/al/fichero/DL010825.TXT -o /ruta/al/fichero/informe.md -g rutas_gps
```

## 🧾 Parámetros:
| Opción | Descripción                                                                     |
| ------ | ------------------------------------------------------------------------------- |
| `-i`   | Ruta al fichero de entrada `.txt` con sentencias NMEA `$GPRMC`                  |
| `-o`   | Nombre del archivo de salida en formato Markdown (por defecto: `gps_output.md`) |
| `-g`   | Prefijo para los ficheros `.gpx` (se genera uno por año)                        |

---

## 📄 Salidas generadas

✅ informe.md

Contiene una tabla con los datos más relevantes:

| 📅 Fecha   | ⏰ Hora   | 📍 Latitud   | 📍 Longitud  | 🚗 Velocidad | 🔗 Link                                                                                 |
| ---------- | -------- | ------------ | ------------ | ------------ | --------------------------------------------------------------------------------------- |
| 01/08/2025 | 19:37:22 | 40°24'60.0"N | -3°42'13.7"W | 4.2 km/h     | 🌍 [Ver Mapa](https://www.google.com/maps/place/40%C2%B024'60.0%22N+3%C2%B042'13.7%22W) |

Incluye también un resumen anual de kilómetros recorridos:

📊 Resumen anual de kilómetros recorridos

    📅 2024: 958.78 km
    📅 2025: 14.52 km
    
    🚀 Total acumulado: 973.3 km

---

## 🗺️ rutas_gps_YYYY.gpx

Ficheros .gpx compatibles con aplicaciones GPS como Garmin, OsmAnd, Google Earth, etc.

Incluyen:

  - 📌 Rutas diarias agrupadas por `<trkseg>`
  - 📝 Descripción con fecha y kilómetros: `<desc>01/08/2025 - 14.52 km</desc>`
  - 🕒 Tiempos en formato ISO 8601: `<time>2025-08-01T19:37:22Z</time>`

---

## 🧪 Ejemplo de entrada

```bash
$GPRMC,120000.000,A,4024.9999,N,00342.2283,W,0.05,270.00,010825,,*1A
$GPRMC,120001.000,A,4024.9999,N,00342.2283,W,0.05,270.00,010825,,*1B
$GPRMC,120002.000,A,4024.9999,N,00342.2283,W,0.05,270.00,010825,,*1C
$GPRMC,120003.000,A,4024.9999,N,00342.2283,W,0.05,270.00,010825,,*1D
$GPRMC,120004.000,A,4024.9999,N,00342.2283,W,0.05,270.00,010825,,*1E
...

```

## 🔎 Explicación de los campos $GPRMC

| Campo     | Valor          | Descripción                            |
| --------- | -------------- | -------------------------------------- |
| Hora UTC  | `120000.000`   | Formato `hhmmss.sss` → 12:00:00        |
| Estado    | `A`            | A = Activo (válido), V = Inválido      |
| Latitud   | `4024.9999,N`  | 40°24.9999′ Norte (\~40.4167°)         |
| Longitud  | `00342.2283,W` | 3°42.2283′ Oeste (\~-3.7038°)          |
| Velocidad | `0.05` nudos   | ≈ 0.09 km/h                            |
| Rumbo     | `270.00`       | Dirección respecto al norte            |
| Fecha     | `010825`       | 1 de agosto de 2025                    |
| Checksum  | `*1A` (etc.)   | Verificación de integridad del mensaje |

---

## 🛰️ Leadtek LR9553D - Especificaciones técnicas

Basado en el chipset SiRFstar III LP (Low Power), este dispositivo combina alto rendimiento con bajo consumo energético, ideal como registrador GPS (data-logger Bluetooth y USB)

📦 Hardware y conectividad

- Chipset: SiRFstarIII LP de alta sensibilidad, con mitigación de multi-path y escudo RF metálico
- Canales: 20 canales “All‑In‑View” para rastreo simultáneo de múltiples satélites
- Antena: Patch cerámico integrada (sin conectores externos)
- Memoria interna: 4 MB en formato `FAT16` capaz de registrar hasta 60 000 puntos (fecha, hora, latitud, longitud, velocidad)

🔋 Energía y operación

- Batería: Li‑ion recargable (~750 mAh). Autonomía continúa de aproximadamente 12 horas
- Duración registro contínuo: hasta 240 horas grabando puntos cada ~15s

🕒 Rendimiento

- Time‑to‑First‑Fix (TTFF):
    - Hot start: ~1 s
    - Warm start: ~35 s
    - Cold start: ~42 s
- Re‑adquisición: ~0.1 s

📐 Precisión y alcance

- Precisión posición:
    - ~10 m RMS 2D sin corrección
    - <5 m con WAAS o EGNOS
- Precisión velocidad: ~0.1 m/s
- Precisión temporal: sincronización con GPS en microsegundos (WGS‑84)

🔌 Interfaz y protocolos

- USB Mini‑B para carga y descarga de datos
- Bluetooth 1.2 (Clase 2), con perfil SPP
- Comunicaciones por puerto serie RS‑232 o TTL
- Protocolos NMEA‑0183 (por defecto) o SiRF Binary
- Velocidades típicas: 38400 bps (solo en modo Sirft), en modo NMEA 9600 bps

🌡️ Condiciones operativas

- Consumo medio alrededor de 70 mA
- Funciona en temperaturas desde ‑30 °C a +60 °C
- Diseñado para ambientes con interferencias, gracias al escudo RF y mitigación multipath

⚠️ Limitaciones conocidas

- El borrado del registro se realiza sólo formateando en Windows, en modo `FAT/FAT16`, no compatible con `FAT32`.
- ❌ En Linux no se borra correctamente el fichero `DL010825.TXT`, lo que puede provocar un brick del dispositivo.
- Aunque aparece como dispositivo de almacenamiento USB, no es totalmente compatible con sistemas de archivos estándar en Linux `mkdosfs`, ni tampoco con Windows 10/11

✅ Comparativa rápida

| Característica           | **9553D**                          | **9553X**                       |
| ------------------------ | ---------------------------------- | ------------------------------- |
| Almacenamiento para logs | Sí (4 MB, \~60 000 puntos)         | No (solo función Bluetooth GPS) |
| Chipset                  | SiRFstar III **LP** (bajo consumo) | SiRFstar III (versión estándar) |
| Bluetooth                | Si                                 | Si                              |
| Autonomía                | \~12 h continuas                   | \~6–8 h                         |
| Conector externo antena  | No                                 | No                              |
| Compatible con PocketPC  | Si                                 | Si                              |
| Bateria extraible        | No                                 | Si                              |
