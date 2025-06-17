import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders, HttpEvent, HttpRequest } from '@angular/common/http';
import { Artist } from './artist.type';
import { Track } from './track.type';
import { Observable } from 'rxjs';


@Injectable({
  providedIn: 'root'
})
export class RestBackendService {

  url = "http://localhost:8000/api";
  media_url = "http://localhost:8000/media"
  constructor(private http: HttpClient) {}

  httpOptions = {
    headers: new HttpHeaders({
      'Content-Type': 'application/json'
    })
  };

  getArtists() {
    const url = `${this.url}/artists`; 
    return this.http.get<Artist[]>(url, this.httpOptions);
  }

  getArtist(uuid: string) {
    const url = `${this.url}/artists/${uuid}`; 
    return this.http.get<Artist>(url, this.httpOptions);
  }

  getTracks(){
    const url = `${this.url}/tracks`; 
    return this.http.get<Track[]>(url, this.httpOptions);
  }

  uploadTracks(files: File[], variant: boolean): Observable<HttpEvent<any>> {
    const url = `${this.url}/tracks/`; 
    const formData = new FormData();
    // Aggiungo ogni file con chiave 'files'
    files.forEach(file => formData.append('files', file, file.name));
    // Aggiungo il parametro variant
    formData.append('variant', variant ? 'true' : 'false');

    const req = new HttpRequest('POST', url, formData, {
      reportProgress: true,
    });
    return this.http.request(req);
  }

}