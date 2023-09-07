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
- [Swagger](https://app.swaggerhub.com/apis-docs/bagusindrayana/perompak7samudra/1.0.0)
- [Postman](https://documenter.getpostman.com/view/7785980/2s9Y5cug6A)



Endpoint | Method | Parameter | Keterangan
--- | --- | --- | ---
`api/search?query={judul_film_yang_dicari}&providers[]={optional:jika ingin mencari di provider tertentu (dan agar lebih cepat)}` | GET | `query`,`providers[]`,`page` | Mencari data film berdasarkan judul
`api/get?link={link_film}&provider={provider_film/website_bajakannya}` | GET | `link`,`provider` | Menampilkan title, link stream dan link download


## Contoh
### Mencari film one piece dari provider PusatFilm
```bash
$ curl -s -H "Accept: application/json" "http://127.0.0.1:5001/api/search?query=one%20piece&providers[]=PusatFilm"
```

## Provider
provider yang tersedia saat ini, **Note : ** jika mencari menggunakan semua provider, maka akan memakan waktu yang cukup lama.

Nama | Status | Speed | Rekomendasi Stream
--- | --- | --- | ---
[PusatFilm](https://51.79.193.133) | ✔️ | Medium | GDP
[Muvi](http://128.199.130.38) | ✔️ | Slow | -
[OppaDrama](http://185.217.95.34) | ✔️ | Medium | FileLions

## Kontribusi
Silahkan buat pull request jika ingin berkontribusi, atau bisa juga dengan mengirimkan saran website yang ingin di scraping.

## Support
- silahkan berikan bintang jika kalian suka dengan project ini
- kalau mau bisa donasi buat beli kuota

<a href="https://trakteer.id/bagood/tip" target="_blank"><img id="wse-buttons-preview" src="https://cdn.trakteer.id/images/embed/trbtn-red-1.png" height="40" style="border:0px;height:40px;" alt="Trakteer Saya"></a>