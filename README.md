## Perompak Film
scraping data film beserta link stream dan downloadnya, **Note:** data diambil dari situs-situs bajakan pihak ketiga, saya tidak bertanggung jawab atas segala bentuk penyalahgunaan data ini.

## Instalasi
```bash
$ git clone https://github.com/bagusindrayana/perompak7samudra.git
$ cd perompak7samudra
$ pip install -r requirements.txt
$ python main.py
```

## API
Endpoint | Method | Keterangan
--- | --- | ---
`api/search?query={judul_film_yang_dicari}&providers[]={optional:jika ingin mencari di provider tertentu (dan agar lebih cepat)}` | GET | Mencari data film berdasarkan judul
`api/get?link={link_film}&provider={provider_film/website_bajakannya}` | GET | Menampilkan title, link stream dan link download
--- | --- | ---

## Contoh
### Mencari film one piece dari provider PusatFilm
```bash
$ curl -s -H "Accept: application/json" "http://127.0.0.1:5001/api/search?query=one%20piece&providers[]=PusatFilm"
```

## Provider
Nama | Status
--- | ---
[PusatFilm](https://51.79.193.133) | ✔️
[Muvi](http://128.199.130.38) | ✔️

## Kontribusi
Silahkan buat pull request jika ingin berkontribusi, atau bisa juga dengan mengirimkan saran website yang ingin di scraping.