import { Component, inject } from '@angular/core';
import { RestBackendService } from '../_services/rest-backend/rest-backend';
import { Artist } from '../_services/rest-backend/artist.type';
import { Router } from '@angular/router';

@Component({
  selector: 'app-artist-detail',
  standalone: true,
  imports: [],
  templateUrl: './artist-detail.html',
  styleUrl: './artist-detail.scss'
})
export class ArtistDetail {
  restService = inject(RestBackendService);
  router = inject(Router);

  artist?: Artist;
  uuid!: string; // dall'url

  ngOnInit() {
    this.artist = history.state.artist;
    if (!this.artist) {
      this.restService.getArtist(this.uuid).subscribe({
        next: (data) => {
          console.log(data);
          this.artist = data;
        },
        error: (err) => {
          console.log(err);
        }
      });
    }
  }


}
