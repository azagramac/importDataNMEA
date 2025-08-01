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

