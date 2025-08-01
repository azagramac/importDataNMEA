#!/usr/bin/env python3

import sys
import argparse
from datetime import datetime
from tabulate import tabulate

def dec_to_dms(dec):
    sign = 1 if dec >= 0 else -1
    dec = abs(dec)
    d = int(dec)
    m = int((dec - d) * 60)
    s = (dec - d - m/60) * 3600
    return d, m, round(s, 1), sign

def get_cardinal(value, coord_type):
    if coord_type == 'lat':
        return 'N' if value >= 0 else 'S'
    else:
        return 'E' if value >= 0 else 'W'

def url_encode_dms(d, m, s, c):
    return f"{d}%C2%B0{m}'{s}%22{c}"

def parse_gprmc(line):
    parts = line.strip().split(',')
    if parts[0] != '$GPRMC' or parts[2] != 'A':
        return None

    time_str = parts[1]
    lat_str = parts[3]
    lat_dir = parts[4]
    lon_str = parts[5]
    lon_dir = parts[6]
    speed_str = parts[7]
    date_str = parts[9]
    alt_str = None

    day = date_str[0:2]
    month = date_str[2:4]
    year = "20" + date_str[4:6]
    date_fmt = f"{day}/{month}/{year}"

    hh = time_str[0:2]
    mm = time_str[2:4]
    ss = time_str[4:6]
    time_fmt = f"{hh}:{mm}:{ss}"
  
    lat_deg = int(lat_str[0:2])
    lat_min = float(lat_str[2:])
    lat_dec = lat_deg + lat_min / 60.0
    if lat_dir == 'S':
        lat_dec = -lat_dec

    lon_deg = int(lon_str[0:3])
    lon_min = float(lon_str[3:])
    lon_dec = lon_deg + lon_min / 60.0
    if lon_dir == 'W':
        lon_dec = -lon_dec

    lat_d, lat_m, lat_s, _ = dec_to_dms(lat_dec)
    lon_d, lon_m, lon_s, _ = dec_to_dms(lon_dec)

    lat_c = get_cardinal(lat_dec, 'lat')
    lon_c = get_cardinal(lon_dec, 'lon')

    lat_fmt = f"{'-' if lat_dec < 0 else ''}{lat_d}°{lat_m}'{lat_s}\"{lat_c}"
    lon_fmt = f"{'-' if lon_dec < 0 else ''}{lon_d}°{lon_m}'{lon_s}\"{lon_c}"

    lat_enc = url_encode_dms(lat_d, lat_m, lat_s, lat_c)
    lon_enc = url_encode_dms(lon_d, lon_m, lon_s, lon_c)
    link = f"https://www.google.com/maps/place/{lat_enc}+{lon_enc}"

    speed_kmh = None
    if speed_str and speed_str != '':
        try:
            speed_kmh = round(float(speed_str) * 1.852, 1)
        except ValueError:
            speed_kmh = None

    try:
        timestamp = datetime.strptime(f"{year}-{month}-{day}T{hh}:{mm}:{ss}Z")
        timestamp_iso = timestamp.isoformat()
    except Exception:
        timestamp_iso = None

    return {
        "date_fmt": date_fmt,
        "time_fmt": time_fmt,
        "lat_fmt": lat_fmt,
        "lon_fmt": lon_fmt,
        "lat_dec": lat_dec,
        "lon_dec": lon_dec,
        "speed_kmh": speed_kmh,
        "link": f"[🌍 Ver Mapa]({link})",
        "altitude": alt_str,
        "timestamp_iso": timestamp_iso,
        "year": int(year),
        "date": date_fmt
    }

def calculate_km(points):
    from math import radians, cos, sin, asin, sqrt
    def haversine(lat1, lon1, lat2, lon2):
        R = 6371.0  # km
        dlat = radians(lat2 - lat1)
        dlon = radians(lon2 - lon1)
        a = sin(dlat/2)**2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon/2)**2
        c = 2 * asin(sqrt(a))
        return R * c
    dist = 0.0
    for i in range(1, len(points)):
        dist += haversine(points[i-1]['lat_dec'], points[i-1]['lon_dec'], points[i]['lat_dec'], points[i]['lon_dec'])
    return round(dist, 2)

def generate_gpx_for_year(year, points, filename, author, desc, creation_date):
    header = f'''<?xml version="1.0" encoding="UTF-8" standalone="no" ?>
<gpx version="1.1" creator="leadtek-gps.py" xmlns="http://www.topografix.com/GPX/1/1">
  <metadata>
    <author>{author}</author>
    <desc>{desc}</desc>
    <time>{creation_date}</time>
  </metadata>
  <trk>
    <name>Ruta GPS Leadtek {year}</name>
'''

    routes = {}
    for pt in points:
        routes.setdefault(pt['date'], []).append(pt)

    body = ""
    for date_key, pts in sorted(routes.items()):
        km = calculate_km(pts)
        body += f'    <trkseg>\n'
        body += f'      <desc>{date_key} - {km} km</desc>\n'
        for pt in pts:
            alt = f"<ele>{pt['altitude']}</ele>" if pt['altitude'] is not None else ""
            time_tag = f"<time>{pt['timestamp_iso']}</time>" if pt['timestamp_iso'] else ""
            body += f'      <trkpt lat="{pt["lat_dec"]}" lon="{pt["lon_dec"]}">\n        {alt}\n        {time_tag}\n      </trkpt>\n'
        body += f'    </trkseg>\n'

    footer = '''  </trk>
</gpx>
'''

    with open(filename, 'w') as f:
        f.write(header)
        f.write(body)
        f.write(footer)

def main():
    parser = argparse.ArgumentParser(description="Procesar fichero NMEA GPRMC y generar tabla Markdown y ficheros GPX por año.")
    parser.add_argument('-i', '--input', required=True, help="Fichero de entrada .txt con datos NMEA")
    parser.add_argument('-o', '--output', default="gps_output.md", help="Fichero de salida Markdown")
    parser.add_argument('-g', '--gpx', default="gps_output", help="Prefijo fichero de salida GPX (se añadirá _YYYY.gpx)")
    args = parser.parse_args()

    table = []
    points_by_year = {}

    try:
        with open(args.input, 'r') as f:
            for line in f:
                if line.startswith('$GPRMC'):
                    parsed = parse_gprmc(line)
                    if parsed:
                        row = [
                            parsed["date_fmt"],
                            parsed["time_fmt"],
                            parsed["lat_fmt"],
                            parsed["lon_fmt"],
                        ]
                        if parsed["speed_kmh"] is not None:
                            row.append(str(parsed["speed_kmh"]) + " km/h")
                        else:
                            row.append("")
                        row.append(parsed["link"])
                        table.append(row)

                        points_by_year.setdefault(parsed['year'], []).append(parsed)

        yearly_summary = {}
        total_km = 0.0
        for year, pts in points_by_year.items():
            km = calculate_km(pts)
            yearly_summary[year] = km
            total_km += km

        resumen_md = "## 📊 Resumen anual de kilómetros recorridos\n\n"
        for year in sorted(yearly_summary.keys()):
            resumen_md += f"- 📅 **{year}**: {yearly_summary[year]} km\n"
        resumen_md += f"\n**🚀 Total acumulado: {round(total_km,2)} km**\n\n"

        headers = ["📅 Fecha", "⏰ Hora", "📍 Latitud", "📍 Longitud", "🚗 Velocidad", "🔗 Link"]
        md_table = tabulate(table, headers=headers, tablefmt="github")

        now_str = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        with open(args.output, 'w') as f_md:
            f_md.write(f"# 🛰️ Datos GPS Leadtek 9535D\n\n")
            f_md.write(f"**🕒 Fecha de generación:** {now_str}\n\n")
            f_md.write(resumen_md)
            f_md.write(md_table)
            f_md.write("\n\n---\n\n")
            f_md.write("⚠️ *Datos extraídos de mensajes NMEA GPRMC*\n")

        author = "Jose l. Azagra"
        desc = "GPS Leadtek 9553D"
        creation_date = datetime.now().isoformat()

        for year, pts in points_by_year.items():
            filename = f"{args.gpx}_{year}.gpx"
            generate_gpx_for_year(year, pts, filename, author, desc, creation_date)
            print(f"✅ Archivo GPX generado: {filename}")

        print(f"✅ Archivo Markdown generado: {args.output}")

    except Exception as e:
        print(f"❌ Error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()

