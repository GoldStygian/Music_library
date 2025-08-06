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


  isExpanded = false;
  maxLength = 250;

  get showReadMore(): boolean {
    const desc = this.artist?.description;
    return !!desc && desc.length > this.maxLength;
  }

  get descriptionText(): string {
    if (!this.artist?.description) return '';
    return this.isExpanded
      ? this.artist.description
      : this.artist.description.slice(0, this.maxLength) + (this.showReadMore ? '...' : '');
  }

  toggleDescription(): void {
    this.isExpanded = !this.isExpanded;
  }

}
